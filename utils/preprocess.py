"""
Image Preprocessing Module
Prepares images for optimal OCR performance through various enhancement techniques
"""
import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ImagePreprocessor:
    """Preprocesses images for better OCR accuracy"""
    
    def __init__(self, config: dict = None):
        """
        Initialize the preprocessor
        
        Args:
            config: Dictionary with preprocessing settings
        """
        self.config = config or {
            "grayscale": True,
            "deskew": True,
            "denoise": True,
            "enhance_contrast": True,
            "median_blur_kernel": 3,
            "clahe_clip_limit": 2.0,
            "clahe_grid_size": (8, 8),
        }
    
    def preprocess(self, image: Image.Image) -> Image.Image:
        """
        Apply all preprocessing steps to an image
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed PIL Image
        """
        logger.info("Starting image preprocessing")
        
        # Convert PIL to OpenCV format
        img_array = np.array(image)
        
        # Convert to grayscale
        if self.config.get("grayscale", True):
            img_array = self._convert_to_grayscale(img_array)
        
        # Deskew the image
        if self.config.get("deskew", True):
            img_array = self._deskew(img_array)
        
        # Remove noise
        if self.config.get("denoise", True):
            img_array = self._denoise(img_array)
        
        # Enhance contrast
        if self.config.get("enhance_contrast", True):
            img_array = self._enhance_contrast(img_array)
        
        # Convert back to PIL Image
        processed_image = Image.fromarray(img_array)
        
        logger.info("Image preprocessing completed")
        return processed_image
    
    def _convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """Convert image to grayscale"""
        if len(image.shape) == 3:
            logger.debug("Converting to grayscale")
            return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return image
    
    def _deskew(self, image: np.ndarray) -> np.ndarray:
        """
        Automatically deskew (align) tilted images
        Uses Hough Line Transform to detect and correct skew
        """
        logger.debug("Deskewing image")
        
        # Ensure grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image.copy()
        
        # Apply threshold to get binary image
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Detect edges
        edges = cv2.Canny(binary, 50, 150, apertureSize=3)
        
        # Detect lines using Hough Transform
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        
        if lines is not None and len(lines) > 0:
            # Calculate average angle
            angles = []
            for rho, theta in lines[:, 0]:
                angle = np.degrees(theta) - 90
                angles.append(angle)
            
            median_angle = np.median(angles)
            
            # Only deskew if angle is significant (> 0.5 degrees)
            if abs(median_angle) > 0.5:
                logger.debug(f"Rotating image by {median_angle:.2f} degrees")
                
                # Get image dimensions
                (h, w) = image.shape[:2]
                center = (w // 2, h // 2)
                
                # Calculate rotation matrix
                M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
                
                # Perform rotation
                rotated = cv2.warpAffine(
                    image,
                    M,
                    (w, h),
                    flags=cv2.INTER_CUBIC,
                    borderMode=cv2.BORDER_REPLICATE
                )
                return rotated
        
        return image
    
    def _denoise(self, image: np.ndarray) -> np.ndarray:
        """
        Remove noise from image using median blur
        """
        logger.debug("Removing noise")
        kernel_size = self.config.get("median_blur_kernel", 3)
        
        # Apply median blur to remove salt-and-pepper noise
        denoised = cv2.medianBlur(image, kernel_size)
        
        return denoised
    
    def _enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """
        Enhance contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
        """
        logger.debug("Enhancing contrast with CLAHE")
        
        # Ensure grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image.copy()
        
        # Apply CLAHE
        clip_limit = self.config.get("clahe_clip_limit", 2.0)
        grid_size = self.config.get("clahe_grid_size", (8, 8))
        
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
        enhanced = clahe.apply(gray)
        
        return enhanced
    
    def resize_if_needed(
        self,
        image: Image.Image,
        max_width: int = None,
        max_height: int = None
    ) -> Image.Image:
        """
        Resize image if it exceeds maximum dimensions
        
        Args:
            image: PIL Image
            max_width: Maximum width
            max_height: Maximum height
            
        Returns:
            Resized image if needed, otherwise original
        """
        width, height = image.size
        
        if max_width and width > max_width:
            ratio = max_width / width
            new_height = int(height * ratio)
            image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
            logger.debug(f"Resized image to {max_width}x{new_height}")
        
        if max_height and image.size[1] > max_height:
            ratio = max_height / image.size[1]
            new_width = int(image.size[0] * ratio)
            image = image.resize((new_width, max_height), Image.Resampling.LANCZOS)
            logger.debug(f"Resized image to {new_width}x{max_height}")
        
        return image


def preprocess_image(image: Image.Image, config: dict = None) -> Image.Image:
    """
    Convenience function to preprocess an image
    
    Args:
        image: PIL Image
        config: Preprocessing configuration
        
    Returns:
        Preprocessed PIL Image
    """
    preprocessor = ImagePreprocessor(config)
    return preprocessor.preprocess(image)
