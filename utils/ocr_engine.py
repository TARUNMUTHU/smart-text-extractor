"""
OCR Engine Module
Supports multiple OCR backends: EasyOCR and Google Vision API
"""
from PIL import Image
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
import time

logger = logging.getLogger(__name__)


class OCRResult:
    """Container for OCR results"""
    
    def __init__(self, text: str, confidence: float = 0.0, metadata: dict = None):
        self.text = text
        self.confidence = confidence
        self.metadata = metadata or {}
    
    def __str__(self):
        return self.text


class BaseOCREngine:
    """Base class for OCR engines"""
    
    def __init__(self):
        self.name = "Base"
    
    def recognize(self, image: Image.Image) -> OCRResult:
        """Recognize text in an image"""
        raise NotImplementedError


class EasyOCREngine(BaseOCREngine):
    """EasyOCR - Easy to use OCR engine"""
    
    def __init__(self, languages: List[str] = None, gpu: bool = False):
        super().__init__()
        self.name = "EasyOCR"
        self.languages = languages or ['en']
        self.gpu = gpu
        self._load_model()
    
    def _load_model(self):
        """Load EasyOCR reader"""
        try:
            import easyocr
            
            logger.info(f"Loading EasyOCR with languages: {self.languages}")
            self.reader = easyocr.Reader(self.languages, gpu=self.gpu)
            logger.info("EasyOCR loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load EasyOCR: {str(e)}")
            raise
    
    def recognize(self, image: Image.Image) -> OCRResult:
        """
        Recognize text using EasyOCR
        
        Args:
            image: PIL Image
            
        Returns:
            OCRResult with extracted text and confidence
        """
        try:
            logger.debug("Running EasyOCR recognition")
            start_time = time.time()
            
            # Convert PIL to numpy array
            img_array = np.array(image)
            
            # Perform OCR
            results = self.reader.readtext(img_array)
            
            # Combine all text results
            texts = []
            confidences = []
            
            for (bbox, text, conf) in results:
                texts.append(text)
                confidences.append(conf)
            
            combined_text = " ".join(texts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            processing_time = time.time() - start_time
            logger.debug(f"EasyOCR recognition completed in {processing_time:.2f}s")
            
            return OCRResult(
                text=combined_text,
                confidence=avg_confidence,
                metadata={
                    "processing_time": processing_time,
                    "num_detections": len(results),
                    "languages": self.languages
                }
            )
            
        except Exception as e:
            logger.error(f"EasyOCR recognition failed: {str(e)}")
            return OCRResult(text="", confidence=0.0, metadata={"error": str(e)})


class GoogleVisionEngine(BaseOCREngine):
    """Google Cloud Vision API OCR"""
    
    def __init__(self, credentials_path: str = None):
        super().__init__()
        self.name = "Google Vision"
        self.credentials_path = credentials_path
        self._load_client()
    
    def _load_client(self):
        """Initialize Google Vision client"""
        try:
            from google.cloud import vision
            import os
            
            if self.credentials_path:
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
            
            logger.info("Initializing Google Vision client")
            self.client = vision.ImageAnnotatorClient()
            logger.info("Google Vision client initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Vision: {str(e)}")
            raise
    
    def recognize(self, image: Image.Image) -> OCRResult:
        """
        Recognize text using Google Vision API
        
        Args:
            image: PIL Image
            
        Returns:
            OCRResult with extracted text
        """
        try:
            from google.cloud import vision
            import io
            
            logger.debug("Running Google Vision recognition")
            start_time = time.time()
            
            # Convert PIL Image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Create Vision API image object
            vision_image = vision.Image(content=img_byte_arr)
            
            # Perform document text detection
            response = self.client.document_text_detection(image=vision_image)
            
            if response.error.message:
                raise Exception(response.error.message)
            
            # Extract text
            text = response.full_text_annotation.text if response.full_text_annotation else ""
            
            # Calculate average confidence
            confidences = []
            for page in response.full_text_annotation.pages:
                for block in page.blocks:
                    confidences.append(block.confidence)
            
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            processing_time = time.time() - start_time
            logger.debug(f"Google Vision recognition completed in {processing_time:.2f}s")
            
            return OCRResult(
                text=text,
                confidence=avg_confidence,
                metadata={"processing_time": processing_time}
            )
            
        except Exception as e:
            logger.error(f"Google Vision recognition failed: {str(e)}")
            return OCRResult(text="", confidence=0.0, metadata={"error": str(e)})


class OCREngine:
    """Main OCR Engine that manages multiple backends"""
    
    ENGINES = {
        'easyocr': EasyOCREngine,
        'google_vision': GoogleVisionEngine
    }
    
    def __init__(self, engine_type: str = 'easyocr', **kwargs):
        """
        Initialize OCR Engine
        
        Args:
            engine_type: Type of OCR engine ('easyocr', 'google_vision')
            **kwargs: Engine-specific parameters
        """
        self.engine_type = engine_type.lower()
        
        if self.engine_type not in self.ENGINES:
            raise ValueError(f"Unknown engine type: {engine_type}. Choose from {list(self.ENGINES.keys())}")
        
        logger.info(f"Initializing {self.engine_type} OCR engine")
        
        # Initialize the selected engine
        engine_class = self.ENGINES[self.engine_type]
        self.engine = self._create_engine(engine_class, **kwargs)
    
    def _create_engine(self, engine_class, **kwargs):
        """Create engine instance with appropriate parameters"""
        if engine_class == EasyOCREngine:
            return engine_class(
                languages=kwargs.get('languages', ['en']),
                gpu=kwargs.get('gpu', False)
            )
        elif engine_class == GoogleVisionEngine:
            return engine_class(
                credentials_path=kwargs.get('credentials_path')
            )
    
    def recognize_text(self, image: Image.Image) -> OCRResult:
        """
        Recognize text in an image
        
        Args:
            image: PIL Image
            
        Returns:
            OCRResult
        """
        return self.engine.recognize(image)
    
    def recognize_batch(self, images: List[Image.Image]) -> List[OCRResult]:
        """
        Recognize text in multiple images
        
        Args:
            images: List of PIL Images
            
        Returns:
            List of OCRResults
        """
        results = []
        for i, image in enumerate(images):
            logger.info(f"Processing image {i+1}/{len(images)}")
            result = self.recognize_text(image)
            results.append(result)
        
        return results


def create_ocr_engine(engine_type: str = 'easyocr', **kwargs) -> OCREngine:
    """
    Factory function to create OCR engine
    
    Args:
        engine_type: Type of engine
        **kwargs: Engine-specific parameters
        
    Returns:
        OCREngine instance
    """
    return OCREngine(engine_type, **kwargs)
