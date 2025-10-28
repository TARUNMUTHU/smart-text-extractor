"""
Answer Evaluation Module using Google Gemini API
Evaluates extracted handwritten answers and provides scores
"""
import logging
import os
import json
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai

logger = logging.getLogger(__name__)


class AnswerEvaluator:
    """Evaluate answers using Gemini AI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Answer Evaluator with Gemini API
        
        Args:
            api_key: Gemini API key (if not provided, reads from environment)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        
        if not self.api_key:
            logger.warning("Gemini API key not found. Answer evaluation will be disabled.")
            self.enabled = False
            return
        
        try:
            genai.configure(api_key=self.api_key)
            # Use available model names from the API
            model_names = [
                'models/gemini-2.5-flash',  # Latest fast model
                'models/gemini-2.0-flash',  # Stable fast model
                'models/gemini-flash-latest',  # Auto-latest
                'models/gemini-pro-latest',  # Pro version
            ]
            
            model_loaded = False
            for model_name in model_names:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    logger.info(f"Successfully loaded model: {model_name}")
                    model_loaded = True
                    break
                except Exception as e:
                    logger.debug(f"Model {model_name} not available: {str(e)}")
                    continue
            
            if not model_loaded:
                raise Exception("No compatible Gemini model found")
                
            self.enabled = True
            logger.info("Gemini API configured successfully")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {str(e)}")
            self.enabled = False
    
    def evaluate_answers(
        self, 
        extracted_text: str, 
        answer_key: Optional[str] = None,
        subject: str = "General",
        total_marks: int = 100
    ) -> Dict:
        """
        Evaluate extracted answers using Gemini AI
        
        Args:
            extracted_text: OCR extracted text from answer script
            answer_key: Optional correct answers or marking scheme
            subject: Subject of the exam (e.g., Math, Science, English)
            total_marks: Total marks for the assignment
            
        Returns:
            Dictionary containing evaluation results
        """
        if not self.enabled:
            return {
                "success": False,
                "error": "Gemini API not configured",
                "message": "Please set GEMINI_API_KEY environment variable"
            }
        
        try:
            # Prepare evaluation prompt
            prompt = self._create_evaluation_prompt(
                extracted_text, 
                answer_key, 
                subject, 
                total_marks
            )
            
            logger.info("Sending evaluation request to Gemini API...")
            response = self.model.generate_content(prompt)
            
            # Parse the response
            evaluation_result = self._parse_evaluation_response(
                response.text, 
                total_marks
            )
            
            logger.info(f"Evaluation completed: {evaluation_result['score']}/{total_marks}")
            return evaluation_result
            
        except Exception as e:
            logger.error(f"Answer evaluation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to evaluate answers"
            }
    
    def _create_evaluation_prompt(
        self, 
        extracted_text: str, 
        answer_key: Optional[str], 
        subject: str, 
        total_marks: int
    ) -> str:
        """Create a detailed prompt for Gemini to evaluate answers"""
        
        if answer_key:
            # If answer key is provided, compare answers
            prompt = f"""You are an expert teacher evaluating a student's {subject} answer script.

**EXTRACTED STUDENT ANSWERS:**
{extracted_text}

**CORRECT ANSWERS/MARKING SCHEME:**
{answer_key}

**TOTAL MARKS:** {total_marks}

Please evaluate the student's answers carefully and provide:

1. **Question-by-Question Analysis:**
   - For each question identified, check if the answer is correct, partially correct, or incorrect
   - Highlight what the student got right and what was wrong
   - Award appropriate marks for each question

2. **Overall Score:** Calculate total score out of {total_marks} marks

3. **Strengths:** What did the student do well?

4. **Areas for Improvement:** What mistakes were made? What needs more practice?

5. **Detailed Feedback:** Specific suggestions for improvement

Format your response as follows:

## Question-by-Question Breakdown
[List each question with marks awarded]

## Total Score
[X out of {total_marks}]

## Strengths
[List strengths]

## Areas for Improvement
[List areas needing work]

## Detailed Feedback
[Provide constructive feedback]

Be fair, constructive, and encouraging in your evaluation."""

        else:
            # If no answer key, do general assessment
            prompt = f"""You are an expert teacher reviewing a student's {subject} answer script.

**EXTRACTED STUDENT ANSWERS:**
{extracted_text}

**TOTAL MARKS:** {total_marks}

Since no answer key is provided, please assess the work based on:
- Clarity and organization of answers
- Depth of understanding shown
- Completeness of responses
- Writing quality and presentation

Provide an estimated score and detailed feedback on the student's work.

Format your response as follows:

## Assessment Summary
[Brief overview of the work]

## Estimated Score
[X out of {total_marks}] - (Note: This is an estimate without answer key)

## Strengths
[What was done well]

## Areas for Improvement
[What could be better]

## Detailed Feedback
[Constructive suggestions]

Be encouraging and provide actionable advice."""

        return prompt
    
    def _parse_evaluation_response(
        self, 
        response_text: str, 
        total_marks: int
    ) -> Dict:
        """Parse Gemini's response and extract key information"""
        
        try:
            # Extract score from response
            score = self._extract_score(response_text, total_marks)
            
            # Extract sections
            sections = self._extract_sections(response_text)
            
            return {
                "success": True,
                "score": score,
                "total_marks": total_marks,
                "percentage": round((score / total_marks) * 100, 2),
                "grade": self._calculate_grade(score, total_marks),
                "evaluation_text": response_text,
                "strengths": sections.get("strengths", []),
                "improvements": sections.get("improvements", []),
                "feedback": sections.get("feedback", ""),
                "question_breakdown": sections.get("breakdown", "")
            }
            
        except Exception as e:
            logger.error(f"Failed to parse evaluation response: {str(e)}")
            return {
                "success": True,
                "score": 0,
                "total_marks": total_marks,
                "percentage": 0,
                "grade": "N/A",
                "evaluation_text": response_text,
                "error": "Could not parse score from response"
            }
    
    def _extract_score(self, text: str, total_marks: int) -> int:
        """Extract numerical score from evaluation text"""
        import re
        
        # Look for patterns like "X out of Y", "X/Y", "Score: X"
        patterns = [
            r'(\d+)\s*out of\s*\d+',
            r'(\d+)\s*/\s*\d+',
            r'[Ss]core[:\s]+(\d+)',
            r'[Tt]otal[:\s]+(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                score = int(match.group(1))
                # Validate score is within range
                if 0 <= score <= total_marks:
                    return score
        
        # If no score found, return 0
        logger.warning("Could not extract score from evaluation text")
        return 0
    
    def _extract_sections(self, text: str) -> Dict[str, any]:
        """Extract different sections from the evaluation text"""
        
        sections = {}
        
        # Extract strengths
        strengths_match = text.split("## Strengths")
        if len(strengths_match) > 1:
            strengths_text = strengths_match[1].split("##")[0].strip()
            sections["strengths"] = [
                s.strip() for s in strengths_text.split("\n") 
                if s.strip() and not s.strip().startswith("#")
            ]
        
        # Extract improvements
        improvements_match = text.split("## Areas for Improvement")
        if len(improvements_match) > 1:
            improvements_text = improvements_match[1].split("##")[0].strip()
            sections["improvements"] = [
                s.strip() for s in improvements_text.split("\n") 
                if s.strip() and not s.strip().startswith("#")
            ]
        
        # Extract feedback
        feedback_match = text.split("## Detailed Feedback")
        if len(feedback_match) > 1:
            sections["feedback"] = feedback_match[1].split("##")[0].strip()
        
        # Extract question breakdown
        breakdown_match = text.split("## Question-by-Question Breakdown")
        if len(breakdown_match) > 1:
            sections["breakdown"] = breakdown_match[1].split("##")[0].strip()
        
        return sections
    
    def _calculate_grade(self, score: int, total_marks: int) -> str:
        """Calculate letter grade based on percentage"""
        
        if total_marks == 0:
            return "N/A"
        
        percentage = (score / total_marks) * 100
        
        if percentage >= 90:
            return "A+"
        elif percentage >= 85:
            return "A"
        elif percentage >= 80:
            return "A-"
        elif percentage >= 75:
            return "B+"
        elif percentage >= 70:
            return "B"
        elif percentage >= 65:
            return "B-"
        elif percentage >= 60:
            return "C+"
        elif percentage >= 55:
            return "C"
        elif percentage >= 50:
            return "C-"
        elif percentage >= 45:
            return "D"
        else:
            return "F"
    
    def evaluate_with_reference(
        self, 
        extracted_text: str, 
        reference_image_path: str,
        subject: str = "General",
        total_marks: int = 100
    ) -> Dict:
        """
        Evaluate answers by comparing with a reference answer sheet image
        
        Args:
            extracted_text: OCR extracted text from student's answer script
            reference_image_path: Path to reference answer key image
            subject: Subject of the exam
            total_marks: Total marks
            
        Returns:
            Evaluation results
        """
        if not self.enabled:
            return {
                "success": False,
                "error": "Gemini API not configured"
            }
        
        try:
            # Upload reference image to Gemini
            from PIL import Image
            
            reference_image = Image.open(reference_image_path)
            
            prompt = f"""You are an expert teacher evaluating a student's {subject} answer script.

**STUDENT'S ANSWERS (extracted via OCR):**
{extracted_text}

**REFERENCE ANSWER KEY:**
The attached image shows the correct answers or marking scheme.

**TOTAL MARKS:** {total_marks}

Please compare the student's answers with the reference and provide a detailed evaluation including:
- Question-by-question marks breakdown
- Total score out of {total_marks}
- Strengths and areas for improvement
- Detailed constructive feedback

Format as before with clear sections."""

            response = self.model.generate_content([prompt, reference_image])
            
            evaluation_result = self._parse_evaluation_response(
                response.text, 
                total_marks
            )
            
            return evaluation_result
            
        except Exception as e:
            logger.error(f"Reference-based evaluation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
