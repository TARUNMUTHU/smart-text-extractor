# 📊 Answer Evaluation with Gemini AI

## Overview

The Smart Handwritten Text Extractor now includes **AI-powered answer evaluation** using Google's Gemini API. This feature automatically grades and evaluates student answer scripts, providing detailed feedback and scores.

## Features

✨ **Automatic Grading**: AI evaluates answers and assigns scores
📝 **Detailed Feedback**: Get strengths, improvements, and constructive feedback
📊 **Question Breakdown**: See marks for individual questions
🎯 **Grade Calculation**: Automatic letter grade assignment (A+, A, B+, etc.)
📈 **Percentage Score**: View performance as a percentage
🖼️ **Reference Comparison**: Upload reference answer sheet for comparison

## Setup

### 1. Install Gemini API Package

Run the installation script and choose to install Gemini:

```cmd
fix_install.bat
```

When prompted:
```
Install Google Gemini API for answer evaluation? (y/n): y
```

Or install manually:
```cmd
pip install google-generativeai
```

### 2. Get Your Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 3. Configure API Key

**Option 1: Environment Variable (Recommended)**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

For permanent setup, add to system environment variables:
1. Right-click "This PC" → Properties
2. Advanced System Settings → Environment Variables
3. Add new variable: `GEMINI_API_KEY` = `your_api_key`

**Option 2: Edit config.py**
```python
GEMINI_API_KEY = "your_api_key_here"
```

## Usage

### Method 1: Text-Based Evaluation

1. **Upload and Process** your handwritten answer script image
2. Wait for OCR extraction to complete
3. In the **Evaluation Section**:
   - Enter **Subject** (e.g., Mathematics, Science)
   - Enter **Total Marks** (e.g., 100)
   - (Optional) Enter **Answer Key/Marking Scheme** in the text box
4. Click **"🤖 Evaluate with AI"**
5. View detailed evaluation results

**Example Answer Key Format:**
```
Q1. Answer: 42 (5 marks)
Q2. Answer: Photosynthesis is the process... (10 marks)
Q3. Answer: x = 5, y = 3 (8 marks)
...
```

### Method 2: Reference Image Evaluation

1. **Upload and Process** your student's answer script
2. In the **Evaluation Section**:
   - Enter **Subject** and **Total Marks**
   - Click **"Choose File"** under reference section
   - Upload the **reference answer sheet image**
3. Click **"🤖 Evaluate with AI"**
4. AI compares student answers with reference image

### Evaluation Results

The evaluation report includes:

#### 📊 Score Display
- **Total Score**: Points earned out of total marks
- **Grade**: Letter grade (A+, A, A-, B+, etc.)
- **Percentage**: Score as a percentage

#### 📋 Detailed Analysis
- **Question-by-Question Breakdown**: Marks for each question
- **Strengths**: What the student did well
- **Areas for Improvement**: Topics needing more practice
- **Detailed Feedback**: Constructive suggestions

## Grading Scale

| Percentage | Grade |
|------------|-------|
| 90-100% | A+ |
| 85-89% | A |
| 80-84% | A- |
| 75-79% | B+ |
| 70-74% | B |
| 65-69% | B- |
| 60-64% | C+ |
| 55-59% | C |
| 50-54% | C- |
| 45-49% | D |
| 0-44% | F |

## Tips for Best Results

### For Accurate Evaluation:

1. **Clear Answer Key**: Provide detailed correct answers for best results
2. **Specify Subject**: More specific subjects (e.g., "Algebra" vs "Math") give better context
3. **Good OCR Quality**: Ensure text extraction is accurate before evaluation
4. **Complete Answers**: Partial or unclear OCR may affect evaluation accuracy

### For Meaningful Feedback:

1. **Use Marking Schemes**: Include point values for partial credit
2. **Specify Total Marks**: Set realistic total marks for the assignment
3. **Subject Context**: Subject helps AI understand expected answer format
4. **Review AI Feedback**: AI provides suggestions, but human review is valuable

## API Endpoints

### Evaluate with Text Answer Key

```http
POST /evaluate/{job_id}
Content-Type: multipart/form-data

answer_key: string (optional)
subject: string (default: "General")
total_marks: integer (default: 100)
```

**Response:**
```json
{
  "success": true,
  "score": 85,
  "total_marks": 100,
  "percentage": 85.0,
  "grade": "A",
  "evaluation_text": "...",
  "strengths": [...],
  "improvements": [...],
  "feedback": "..."
}
```

### Evaluate with Reference Image

```http
POST /evaluate-with-reference/{job_id}
Content-Type: multipart/form-data

reference_file: image file
subject: string (default: "General")
total_marks: integer (default: 100)
```

## Example Workflow

### Complete Grading Workflow:

```
1. Student submits handwritten answer script (image)
   ↓
2. Upload to Smart Text Extractor
   ↓
3. OCR extracts handwritten text
   ↓
4. Teacher provides answer key or reference image
   ↓
5. Gemini AI evaluates answers
   ↓
6. System displays:
   - Total score and grade
   - Question breakdown
   - Strengths and improvements
   - Detailed feedback
   ↓
7. Teacher reviews and finalizes grade
```

## Troubleshooting

### "Gemini API not configured"
- Check that `GEMINI_API_KEY` is set in environment variables or config.py
- Verify API key is valid

### "Evaluation failed"
- Check internet connection (Gemini requires API access)
- Verify API key hasn't expired or hit quota limits
- Check Google Cloud Console for API status

### Low Accuracy Evaluation
- Ensure OCR extraction quality is good
- Provide detailed answer key
- Specify subject clearly
- Review extracted text before evaluation

### API Quota Exceeded
- Gemini has free tier limits
- Upgrade to paid tier for higher quotas
- Monitor usage at: https://console.cloud.google.com

## Pricing

**Google Gemini API Pricing** (as of 2024):

- **Free Tier**: 60 requests/minute
- **Paid Tier**: Higher limits, pay-per-use

Check current pricing: https://ai.google.dev/pricing

## Privacy & Security

⚠️ **Important Considerations:**

1. **Data Transmission**: Student answers are sent to Google's servers
2. **Privacy Compliance**: Ensure compliance with educational data privacy laws
3. **Consent**: Get appropriate consent before using AI evaluation
4. **Review Results**: AI evaluation should supplement, not replace, human review

## Best Practices

✅ **Do:**
- Use for preliminary grading and feedback
- Review AI evaluations before finalizing grades
- Provide clear answer keys for objective questions
- Use for formative assessment and learning

❌ **Don't:**
- Rely solely on AI for high-stakes exams
- Share API keys publicly
- Process sensitive data without consent
- Skip human review of results

## Support

For issues or questions:
1. Check this guide
2. Review API documentation: https://ai.google.dev/docs
3. Check error messages in browser console
4. Verify API key and configuration

## Updates

**Version 2.1** - Added Gemini AI evaluation
- Text-based answer key evaluation
- Reference image comparison
- Detailed feedback generation
- Automatic grading with letter grades
- Question-by-question breakdown

---

**Powered by Google Gemini AI** 🤖
