"""
Smart Handwritten Text Extractor - Main Application
FastAPI web server for image text extraction (NO PDF - Images only!)
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import shutil
import uuid
import time
from datetime import datetime
from pathlib import Path
import logging
from PIL import Image

# Import our utility modules
from utils.preprocess import ImagePreprocessor
from utils.ocr_engine import OCREngine
from utils.postprocess import TextPostprocessor, create_output_file
from utils.answer_evaluator import AnswerEvaluator

# Import configuration
import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    version=config.VERSION,
    description="Extract clean text from handwritten PDF files"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Global processing status storage (in production, use Redis or database)
processing_status = {}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "app_name": config.APP_NAME,
        "version": config.VERSION
    })


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), ocr_engine: str = Form(default=config.OCR_ENGINE)):
    """
    Upload and process an image file
    
    Args:
        file: Image file upload (JPG, PNG, etc.)
        ocr_engine: OCR engine to use ('trocr', 'easyocr', 'google_vision')
        
    Returns:
        JSON response with processing status
    """
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in config.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed: {', '.join(config.ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > config.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum limit of {config.MAX_FILE_SIZE / (1024*1024):.0f} MB"
        )
    
    # Generate unique ID for this processing job
    job_id = str(uuid.uuid4())
    
    # Create job-specific folders
    job_folder = os.path.join(config.UPLOAD_FOLDER, job_id)
    output_folder = os.path.join(config.OUTPUT_FOLDER, job_id)
    os.makedirs(job_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    
    # Save uploaded file
    image_path = os.path.join(job_folder, file.filename)
    with open(image_path, "wb") as f:
        f.write(file_content)
    
    logger.info(f"Image uploaded: {file.filename} (Job ID: {job_id})")
    
    # Initialize processing status
    processing_status[job_id] = {
        "status": "processing",
        "filename": file.filename,
        "progress": 0,
        "message": "Starting processing...",
        "start_time": datetime.now().isoformat()
    }
    
    # Process in background (in production, use background tasks or Celery)
    try:
        result = await process_image(
            image_path=image_path,
            job_id=job_id,
            output_folder=output_folder,
            ocr_engine=ocr_engine
        )
        
        processing_status[job_id].update({
            "status": "completed",
            "progress": 100,
            "message": "Processing completed successfully",
            "result": result
        })
        
    except Exception as e:
        logger.error(f"Processing failed for job {job_id}: {str(e)}")
        processing_status[job_id].update({
            "status": "failed",
            "message": f"Processing failed: {str(e)}"
        })
    
    return JSONResponse({
        "job_id": job_id,
        "status": "processing",
        "message": "File uploaded successfully, processing started"
    })


async def process_image(image_path: str, job_id: str, output_folder: str, ocr_engine: str):
    """
    Process an image file through the complete pipeline
    
    Args:
        image_path: Path to image file
        job_id: Unique job identifier
        output_folder: Folder to save outputs
        ocr_engine: OCR engine to use
        
    Returns:
        Processing results dictionary
    """
    start_time = time.time()
    
    logger.info(f"Starting image processing (Job: {job_id})")
    
    # Update status
    processing_status[job_id]["message"] = "Loading image..."
    processing_status[job_id]["progress"] = 10
    
    # Step 1: Load image
    try:
        image = Image.open(image_path)
        logger.info(f"Loaded image: {image.size} pixels, mode: {image.mode}")
    except Exception as e:
        raise Exception(f"Failed to load image: {str(e)}")
    
    # Update status
    processing_status[job_id]["message"] = "Preprocessing image..."
    processing_status[job_id]["progress"] = 30
    
    # Step 2: Preprocess image
    preprocessor = ImagePreprocessor(config.PREPROCESS_CONFIG)
    processed_image = preprocessor.preprocess(image)
    logger.info("Image preprocessing completed")
    
    # Update status
    processing_status[job_id]["message"] = "Extracting text with OCR..."
    processing_status[job_id]["progress"] = 50
    
    # Step 3: OCR
    ocr_config = {
        'easyocr': {
            'languages': config.EASYOCR_LANGUAGES,
            'gpu': config.EASYOCR_GPU
        },
        'google_vision': {
            'credentials_path': config.GOOGLE_CREDENTIALS_PATH
        }
    }
    
    ocr = OCREngine(ocr_engine, **ocr_config.get(ocr_engine, {}))
    
    # Process single image
    result = ocr.recognize_text(processed_image)
    logger.info(f"OCR completed - Confidence: {result.confidence:.2f}")
    processing_status[job_id]["progress"] = 80
    
    # Update status
    processing_status[job_id]["message"] = "Postprocessing text..."
    processing_status[job_id]["progress"] = 85
    
    # Step 4: Postprocess
    postprocessor = TextPostprocessor(config.POSTPROCESS_CONFIG)
    final_text = postprocessor.process(result.text, result.confidence)
    
    # Update status
    processing_status[job_id]["message"] = "Saving outputs..."
    processing_status[job_id]["progress"] = 95
    
    # Step 5: Save outputs
    output_base = os.path.join(output_folder, "extracted_text")
    
    # Save as TXT
    create_output_file(final_text, output_base, format="txt")
    
    # Save as DOCX
    try:
        create_output_file(final_text, output_base, format="docx")
    except Exception as e:
        logger.warning(f"Could not create DOCX: {str(e)}")
    
    # Calculate metrics
    processing_time = time.time() - start_time
    
    logger.info(f"Processing completed in {processing_time:.2f}s (Job: {job_id})")
    
    return {
        "text": final_text,
        "confidence": result.confidence,
        "processing_time": processing_time,
        "ocr_engine": ocr_engine,
        "output_files": {
            "txt": f"{output_base}.txt",
            "docx": f"{output_base}.docx"
        }
    }


@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """
    Get processing status for a job
    
    Args:
        job_id: Job identifier
        
    Returns:
        Status information
    """
    if job_id not in processing_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JSONResponse(processing_status[job_id])


@app.get("/download/{job_id}/{format}")
async def download_file(job_id: str, format: str):
    """
    Download processed file
    
    Args:
        job_id: Job identifier
        format: File format ('txt' or 'docx')
        
    Returns:
        File download
    """
    if format not in config.OUTPUT_FORMATS:
        raise HTTPException(status_code=400, detail=f"Invalid format. Choose from {config.OUTPUT_FORMATS}")
    
    file_path = os.path.join(config.OUTPUT_FOLDER, job_id, f"extracted_text.{format}")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type='application/octet-stream',
        filename=f"extracted_text.{format}"
    )


@app.get("/result/{job_id}")
async def get_result(job_id: str):
    """
    Get the extracted text result
    
    Args:
        job_id: Job identifier
        
    Returns:
        Extracted text and metadata
    """
    if job_id not in processing_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    status = processing_status[job_id]
    
    if status["status"] != "completed":
        raise HTTPException(status_code=400, detail="Processing not completed")
    
    return JSONResponse(status["result"])


@app.delete("/cleanup/{job_id}")
async def cleanup_job(job_id: str):
    """
    Clean up files for a job
    
    Args:
        job_id: Job identifier
        
    Returns:
        Success message
    """
    # Remove upload folder
    upload_folder = os.path.join(config.UPLOAD_FOLDER, job_id)
    if os.path.exists(upload_folder):
        shutil.rmtree(upload_folder)
    
    # Remove output folder
    output_folder = os.path.join(config.OUTPUT_FOLDER, job_id)
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    
    # Remove from status
    if job_id in processing_status:
        del processing_status[job_id]
    
    logger.info(f"Cleaned up job: {job_id}")
    
    return JSONResponse({"message": "Job cleaned up successfully"})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy",
        "app": config.APP_NAME,
        "version": config.VERSION
    })


@app.post("/evaluate/{job_id}")
async def evaluate_answers(
    job_id: str,
    answer_key: str = Form(default=""),
    subject: str = Form(default="General"),
    total_marks: int = Form(default=100)
):
    """
    Evaluate extracted answers using Gemini AI
    
    Args:
        job_id: Job identifier
        answer_key: Correct answers or marking scheme (optional)
        subject: Subject of the exam
        total_marks: Total marks for the assignment
        
    Returns:
        Evaluation results with score and feedback
    """
    if job_id not in processing_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    status = processing_status[job_id]
    
    if status["status"] != "completed":
        raise HTTPException(status_code=400, detail="Processing not completed yet")
    
    # Get extracted text
    extracted_text = status["result"]["text"]
    
    # Initialize evaluator
    evaluator = AnswerEvaluator(api_key=config.GEMINI_API_KEY)
    
    if not evaluator.enabled:
        raise HTTPException(
            status_code=503,
            detail="Answer evaluation is not available. Please configure GEMINI_API_KEY."
        )
    
    # Perform evaluation
    evaluation = evaluator.evaluate_answers(
        extracted_text=extracted_text,
        answer_key=answer_key if answer_key else None,
        subject=subject,
        total_marks=total_marks
    )
    
    if not evaluation.get("success", False):
        raise HTTPException(
            status_code=500,
            detail=evaluation.get("error", "Evaluation failed")
        )
    
    # Store evaluation in processing status
    processing_status[job_id]["evaluation"] = evaluation
    
    return JSONResponse(evaluation)


@app.post("/evaluate-with-reference/{job_id}")
async def evaluate_with_reference(
    job_id: str,
    reference_file: UploadFile = File(...),
    subject: str = Form(default="General"),
    total_marks: int = Form(default=100)
):
    """
    Evaluate answers by comparing with reference answer sheet image
    
    Args:
        job_id: Job identifier
        reference_file: Reference answer key image file
        subject: Subject of the exam
        total_marks: Total marks
        
    Returns:
        Evaluation results
    """
    if job_id not in processing_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    status = processing_status[job_id]
    
    if status["status"] != "completed":
        raise HTTPException(status_code=400, detail="Processing not completed yet")
    
    # Save reference file temporarily
    reference_path = os.path.join(config.UPLOAD_FOLDER, job_id, "reference_" + reference_file.filename)
    reference_content = await reference_file.read()
    
    with open(reference_path, "wb") as f:
        f.write(reference_content)
    
    # Get extracted text
    extracted_text = status["result"]["text"]
    
    # Initialize evaluator
    evaluator = AnswerEvaluator(api_key=config.GEMINI_API_KEY)
    
    if not evaluator.enabled:
        raise HTTPException(
            status_code=503,
            detail="Answer evaluation is not available. Please configure GEMINI_API_KEY."
        )
    
    # Perform evaluation with reference image
    evaluation = evaluator.evaluate_with_reference(
        extracted_text=extracted_text,
        reference_image_path=reference_path,
        subject=subject,
        total_marks=total_marks
    )
    
    if not evaluation.get("success", False):
        raise HTTPException(
            status_code=500,
            detail=evaluation.get("error", "Evaluation failed")
        )
    
    # Store evaluation in processing status
    processing_status[job_id]["evaluation"] = evaluation
    
    return JSONResponse(evaluation)


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting {config.APP_NAME} v{config.VERSION}")
    logger.info(f"Server running at http://{config.HOST}:{config.PORT}")
    
    uvicorn.run(
        "app:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
