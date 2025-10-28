# 🔄 Application Workflow

## Complete Processing Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                     USER INTERACTION LAYER                          │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ 1. Upload PDF
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        WEB INTERFACE                                │
│  templates/index.html                                               │
│  • Drag & drop upload                                               │
│  • OCR engine selection (EasyOCR / TrOCR / Google Vision)          │
│  • Real-time progress tracking                                      │
│  • Results display with confidence scores                           │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ 2. HTTP POST /upload
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       FASTAPI SERVER                                │
│  app.py                                                             │
│  • File validation (format, size)                                  │
│  • Generate unique job ID                                           │
│  • Save to uploads folder                                           │
│  • Start processing pipeline                                        │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ 3. Process PDF
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    PROCESSING PIPELINE                              │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ STEP 1: PDF TO IMAGE CONVERSION                               │ │
│  │ utils/pdf_to_image.py                                         │ │
│  │ • Convert PDF pages to images (300 DPI)                       │ │
│  │ • Output: List of PIL Image objects                           │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                            │                                         │
│                            │ [Page 1, Page 2, ..., Page N]          │
│                            ▼                                         │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ STEP 2: IMAGE PREPROCESSING                                   │ │
│  │ utils/preprocess.py                                           │ │
│  │ • Convert to grayscale                                        │ │
│  │ • Auto-deskew (correct tilt)                                  │ │
│  │ • Remove noise (median blur)                                  │ │
│  │ • Enhance contrast (CLAHE)                                    │ │
│  │ • Output: Enhanced images ready for OCR                       │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                            │                                         │
│                            │ [Enhanced images]                       │
│                            ▼                                         │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ STEP 3: OCR TEXT EXTRACTION                                   │ │
│  │ utils/ocr_engine.py                                           │ │
│  │                                                               │ │
│  │ Choose engine:                                                │ │
│  │ ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │ │
│  │ │  EasyOCR    │  │   TrOCR     │  │  Google Vision API  │   │ │
│  │ │             │  │             │  │                     │   │ │
│  │ │ • Fast      │  │ • High      │  │ • Best quality      │   │ │
│  │ │ • Offline   │  │   accuracy  │  │ • Cloud-based       │   │ │
│  │ │ • 80+ langs │  │ • Handwrite │  │ • Requires API key  │   │ │
│  │ └─────────────┘  └─────────────┘  └─────────────────────┘   │ │
│  │                                                               │ │
│  │ • Extract text from each image                                │ │
│  │ • Calculate confidence scores                                 │ │
│  │ • Output: OCRResult objects with text + metadata              │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                            │                                         │
│                            │ [Raw OCR text + confidence]             │
│                            ▼                                         │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ STEP 4: TEXT POSTPROCESSING                                   │ │
│  │ utils/postprocess.py                                          │ │
│  │ • Remove extra whitespace                                     │ │
│  │ • Fix common OCR errors                                       │ │
│  │ • Apply spell checking (TextBlob)                             │ │
│  │ • Combine all pages into single text                          │ │
│  │ • Output: Clean, readable text                                │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                            │                                         │
│                            │ [Final cleaned text]                    │
│                            ▼                                         │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ STEP 5: OUTPUT GENERATION                                     │ │
│  │ utils/postprocess.py - create_output_file()                   │ │
│  │ • Save as .txt (plain text)                                   │ │
│  │ • Save as .docx (Word document)                               │ │
│  │ • Store in static/outputs/{job_id}/                           │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ 4. Update status
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      STATUS TRACKING                                │
│  • Real-time progress updates (0-100%)                             │
│  • Processing messages                                              │
│  • Error handling                                                   │
│  • Completion notification                                          │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ 5. Display results
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        RESULTS                                      │
│  • Extracted text preview                                           │
│  • Statistics:                                                      │
│    - Number of pages processed                                      │
│    - Average confidence score                                       │
│    - Processing time                                                │
│  • Download options:                                                │
│    - 📥 Download .txt                                               │
│    - 📥 Download .docx                                              │
└─────────────────────────────────────────────────────────────────────┘
```

## 📊 Data Flow

```
INPUT                  INTERMEDIATE                      OUTPUT
━━━━━                  ━━━━━━━━━━━━                      ━━━━━━

📄 PDF File     →     🖼️ Images (300 DPI)      →       📝 Clean Text
                              │
                              ↓
                      🎨 Enhanced Images
                       (grayscale, denoised,
                        deskewed, contrasted)
                              │
                              ↓
                      🤖 OCR Processing
                       (text + confidence)
                              │
                              ↓
                      ✨ Cleaned Text
                       (spell-checked,
                        formatted)
                              │
                              ↓
                      💾 Output Files
                       (.txt, .docx)
```

## 🔀 API Request Flow

```
┌──────────┐
│  Client  │
│ (Browser)│
└─────┬────┘
      │
      │ POST /upload (PDF + engine choice)
      ▼
┌─────────────┐
│   FastAPI   │──────┐
│   Server    │      │ Save file
└─────┬───────┘      │ Generate job_id
      │              ▼
      │         ┌──────────┐
      │         │ Uploads  │
      │         │  Folder  │
      │         └──────────┘
      │
      │ Start background processing
      ▼
┌─────────────┐
│  Pipeline   │
│ Processing  │
└─────┬───────┘
      │
      ├─→ Update status: "Converting PDF..."
      ├─→ Update status: "Preprocessing..."
      ├─→ Update status: "Running OCR..."
      ├─→ Update status: "Postprocessing..."
      └─→ Update status: "Complete!"
      
      
┌──────────┐
│  Client  │
└─────┬────┘
      │
      │ GET /status/{job_id} (polling every 1s)
      ▼
┌─────────────┐
│   FastAPI   │
│   Server    │
└─────┬───────┘
      │
      │ Return: {progress: 75%, message: "Running OCR..."}
      ▼
┌──────────┐
│  Client  │
│  (Shows  │
│ Progress)│
└──────────┘


After completion:

┌──────────┐
│  Client  │
└─────┬────┘
      │
      │ GET /download/{job_id}/txt
      ▼
┌─────────────┐
│   FastAPI   │
│   Server    │
└─────┬───────┘
      │
      │ Return file from outputs folder
      ▼
┌──────────┐
│  Client  │
│(Download)│
└──────────┘
```

## 🎯 File Organization During Processing

```
vit hack/
├── static/
│   ├── uploads/
│   │   └── {job_id}/
│   │       └── uploaded_document.pdf    ← Original PDF
│   │
│   └── outputs/
│       └── {job_id}/
│           ├── extracted_text.txt       ← Final TXT output
│           └── extracted_text.docx      ← Final DOCX output
│
└── (temporary in memory)
    ├── images/                          ← PDF pages as images
    ├── preprocessed_images/             ← Enhanced images
    └── ocr_results/                     ← Raw OCR text
```

## ⚡ Performance Optimization Points

```
1. PDF Conversion
   • Adjustable DPI (lower = faster)
   • Batch processing
   
2. Preprocessing
   • Toggleable steps
   • GPU acceleration (OpenCV)
   
3. OCR Engine
   • EasyOCR: Fast, good for printed text
   • TrOCR: Best for handwriting
   • Google Vision: Highest quality (requires API)
   
4. Postprocessing
   • Optional spell checking
   • Configurable confidence threshold
   
5. Caching
   • Reuse models between requests
   • Keep engines loaded in memory
```

## 🔒 Security Considerations

```
✓ File type validation (.pdf only)
✓ File size limits (50 MB default)
✓ Unique job IDs (UUID)
✓ Isolated job folders
✓ Cleanup endpoint for file removal
✓ No code execution from PDFs
```

---

**This workflow diagram shows the complete journey from PDF upload to text extraction!**
