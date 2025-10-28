"""
Configuration file for Smart Handwritten Text Extractor
"""
import os

# Application settings
APP_NAME = "Smart Handwritten Text Extractor"
VERSION = "2.1.0"
DEBUG = True

# Server settings
HOST = "0.0.0.0"
PORT = 8000

# File upload settings
UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/outputs"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}  # Image formats only

# Image preprocessing settings
PREPROCESS_CONFIG = {
    "grayscale": True,
    "deskew": True,
    "denoise": True,
    "enhance_contrast": True,
    "median_blur_kernel": 3,
    "clahe_clip_limit": 2.0,
    "clahe_grid_size": (8, 8),
}

# OCR Engine settings
# Options: 'easyocr', 'google_vision'
OCR_ENGINE = "easyocr"  # Default engine

# EasyOCR settings
EASYOCR_LANGUAGES = ['en']
EASYOCR_GPU = False  # Set to True if GPU is available

# Google Vision API settings (optional)
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")

# Gemini API settings (for answer evaluation)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")  # Set your Gemini API key here
ENABLE_ANSWER_EVALUATION = True  # Enable/disable answer evaluation feature

# Text postprocessing settings
POSTPROCESS_CONFIG = {
    "remove_extra_spaces": True,
    "spell_check": True,
    "min_confidence": 0.5,  # Minimum confidence threshold
}

# Output settings
OUTPUT_FORMATS = ["txt", "docx"]
DEFAULT_OUTPUT_FORMAT = "txt"

# Logging settings
LOG_PROCESSING_TIME = True
LOG_CONFIDENCE_SCORES = True

# Create required directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
