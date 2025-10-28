"""
PDF to Image Converter
Converts PDF pages to high-resolution images for OCR processing
"""
from pdf2image import convert_from_path
from PIL import Image
import os
from typing import List
import logging

logger = logging.getLogger(__name__)


class PDFToImageConverter:
    """Converts PDF files to high-resolution images"""
    
    def __init__(self, dpi: int = 300, image_format: str = "PNG"):
        """
        Initialize the PDF to Image converter
        
        Args:
            dpi: Resolution in dots per inch (default: 300 for high quality)
            image_format: Output image format (PNG, JPEG, etc.)
        """
        self.dpi = dpi
        self.image_format = image_format
        
    def convert(self, pdf_path: str, output_folder: str = None) -> List[Image.Image]:
        """
        Convert PDF to list of PIL Images
        
        Args:
            pdf_path: Path to the PDF file
            output_folder: Optional folder to save images (if None, returns images only)
            
        Returns:
            List of PIL Image objects
        """
        try:
            logger.info(f"Converting PDF to images with {self.dpi} DPI: {pdf_path}")
            
            # Convert PDF to images
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                fmt=self.image_format.lower()
            )
            
            logger.info(f"Successfully converted {len(images)} pages")
            
            # Optionally save images to disk
            if output_folder:
                os.makedirs(output_folder, exist_ok=True)
                saved_paths = []
                
                for i, image in enumerate(images):
                    image_path = os.path.join(
                        output_folder,
                        f"page_{i+1}.{self.image_format.lower()}"
                    )
                    image.save(image_path, self.image_format)
                    saved_paths.append(image_path)
                    logger.info(f"Saved page {i+1} to {image_path}")
                
                return images, saved_paths
            
            return images
            
        except Exception as e:
            logger.error(f"Error converting PDF to images: {str(e)}")
            raise Exception(f"Failed to convert PDF: {str(e)}")
    
    def get_page_count(self, pdf_path: str) -> int:
        """
        Get the number of pages in a PDF
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Number of pages
        """
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(pdf_path)
            return len(reader.pages)
        except:
            # Fallback: convert and count
            images = self.convert(pdf_path)
            return len(images)


def convert_pdf_to_images(
    pdf_path: str,
    dpi: int = 300,
    output_folder: str = None
) -> List[Image.Image]:
    """
    Convenience function to convert PDF to images
    
    Args:
        pdf_path: Path to the PDF file
        dpi: Resolution in DPI
        output_folder: Optional output folder
        
    Returns:
        List of PIL Images
    """
    converter = PDFToImageConverter(dpi=dpi)
    return converter.convert(pdf_path, output_folder)
