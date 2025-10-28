"""
Text Postprocessing Module
Cleans and corrects extracted text
"""
import re
from typing import List
import logging

logger = logging.getLogger(__name__)


class TextPostprocessor:
    """Postprocesses OCR output text"""
    
    def __init__(self, config: dict = None):
        """
        Initialize postprocessor
        
        Args:
            config: Postprocessing configuration
        """
        self.config = config or {
            "remove_extra_spaces": True,
            "spell_check": True,
            "min_confidence": 0.5,
        }
        
        # Initialize spell checker if needed
        if self.config.get("spell_check", False):
            self._init_spell_checker()
    
    def _init_spell_checker(self):
        """Initialize spell checker"""
        try:
            from textblob import TextBlob
            self.spell_checker = TextBlob
            logger.info("Spell checker initialized")
        except ImportError:
            logger.warning("TextBlob not available, spell checking disabled")
            self.spell_checker = None
    
    def process(self, text: str, confidence: float = 1.0) -> str:
        """
        Process and clean text
        
        Args:
            text: Raw OCR text
            confidence: OCR confidence score
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        logger.debug("Starting text postprocessing")
        
        # Check confidence threshold
        min_confidence = self.config.get("min_confidence", 0.5)
        if confidence < min_confidence:
            logger.warning(f"Low confidence ({confidence:.2f}), results may be unreliable")
        
        # Clean text
        cleaned_text = text
        
        # Remove extra spaces
        if self.config.get("remove_extra_spaces", True):
            cleaned_text = self._remove_extra_spaces(cleaned_text)
        
        # Fix common OCR errors
        cleaned_text = self._fix_common_errors(cleaned_text)
        
        # Apply spell checking
        if self.config.get("spell_check", False) and self.spell_checker:
            cleaned_text = self._spell_check(cleaned_text)
        
        logger.debug("Text postprocessing completed")
        return cleaned_text
    
    def _remove_extra_spaces(self, text: str) -> str:
        """Remove extra whitespace"""
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Remove spaces at start/end of lines
        text = '\n'.join(line.strip() for line in text.split('\n'))
        
        # Remove multiple blank lines
        text = re.sub(r'\n\n+', '\n\n', text)
        
        return text.strip()
    
    def _fix_common_errors(self, text: str) -> str:
        """Fix common OCR errors"""
        # Fix common character substitutions
        replacements = {
            r'\b0\b': 'O',  # Zero to letter O in words
            r'\bl\b': 'I',  # Lowercase l to uppercase I
            r'~': '-',      # Tilde to hyphen
            r'[''`]': "'",  # Smart quotes to regular apostrophe
            r'["""]': '"',  # Smart quotes to regular quotes
        }
        
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text)
        
        # Remove unwanted symbols (keep alphanumeric, punctuation, whitespace)
        text = re.sub(r'[^\w\s\.,;:!?\-\'"()\[\]{}/@#$%&*+=]', '', text)
        
        return text
    
    def _spell_check(self, text: str) -> str:
        """
        Apply spell checking with TextBlob
        Note: This is conservative and may not correct all errors
        """
        try:
            if not self.spell_checker:
                return text
            
            logger.debug("Applying spell checking")
            
            # Process text with TextBlob
            blob = self.spell_checker(text)
            
            # Get corrected text
            corrected = str(blob.correct())
            
            return corrected
            
        except Exception as e:
            logger.warning(f"Spell checking failed: {str(e)}")
            return text
    
    def process_batch(self, texts: List[str], confidences: List[float] = None) -> List[str]:
        """
        Process multiple text strings
        
        Args:
            texts: List of text strings
            confidences: Optional list of confidence scores
            
        Returns:
            List of processed texts
        """
        if confidences is None:
            confidences = [1.0] * len(texts)
        
        processed = []
        for text, conf in zip(texts, confidences):
            processed.append(self.process(text, conf))
        
        return processed
    
    def combine_texts(self, texts: List[str], separator: str = "\n\n") -> str:
        """
        Combine multiple text segments
        
        Args:
            texts: List of text strings (e.g., from different pages)
            separator: Separator between texts
            
        Returns:
            Combined text
        """
        # Filter out empty texts
        non_empty = [t for t in texts if t.strip()]
        
        # Combine with separator
        combined = separator.join(non_empty)
        
        return combined


def postprocess_text(text: str, config: dict = None) -> str:
    """
    Convenience function to postprocess text
    
    Args:
        text: Raw text
        config: Postprocessing config
        
    Returns:
        Cleaned text
    """
    processor = TextPostprocessor(config)
    return processor.process(text)


def create_output_file(text: str, output_path: str, format: str = "txt"):
    """
    Save text to output file
    
    Args:
        text: Text to save
        output_path: Output file path (without extension)
        format: Output format ('txt' or 'docx')
    """
    if format == "txt":
        with open(f"{output_path}.txt", "w", encoding="utf-8") as f:
            f.write(text)
        logger.info(f"Saved text output to {output_path}.txt")
        
    elif format == "docx":
        try:
            from docx import Document
            
            doc = Document()
            
            # Add text paragraphs
            for paragraph in text.split('\n\n'):
                if paragraph.strip():
                    doc.add_paragraph(paragraph.strip())
            
            doc.save(f"{output_path}.docx")
            logger.info(f"Saved DOCX output to {output_path}.docx")
            
        except ImportError:
            logger.error("python-docx not available, falling back to txt")
            create_output_file(text, output_path, format="txt")
        except Exception as e:
            logger.error(f"Failed to create DOCX: {str(e)}")
            raise
    
    else:
        raise ValueError(f"Unsupported format: {format}")
