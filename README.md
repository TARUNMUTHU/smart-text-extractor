# 📝 Smart Handwritten Text Extractor

A powerful Python web application that automatically extracts clean, readable text from handwritten **images** using advanced OCR technology, with **AI-powered answer evaluation** using Google Gemini.

**✨ NEW in v2.1: AI Answer Evaluation with Gemini API!**

![Version](https://img.shields.io/badge/version-2.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8--3.13-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🌟 Features

- **️ Multiple Image Formats**: JPG, PNG, BMP, TIFF, WebP support
- **🔍 Multi-Engine OCR Support**:
  - **EasyOCR**: Fast and accurate local OCR engine for handwritten text
  - **Google Vision API**: Cloud-based OCR with excellent accuracy (optional)
- **🤖 AI Answer Evaluation** (NEW!):
  - **Automatic Grading**: Gemini AI evaluates and scores answer scripts
  - **Detailed Feedback**: Get strengths, improvements, and suggestions
  - **Question Breakdown**: See marks for individual questions
  - **Letter Grades**: Automatic grade calculation (A+, A, B+, etc.)
  - **Reference Comparison**: Upload answer key image for comparison
- **🖼️ Advanced Image Preprocessing**:
  - Automatic grayscale conversion
  - Intelligent deskewing (tilt correction)
  - Noise removal with median blur
  - Contrast enhancement using CLAHE
- **✨ Smart Text Postprocessing**:
  - Remove extra spaces and clean formatting
  - Fix common OCR errors
  - Optional spell checking with TextBlob
- **📊 Real-time Progress Tracking**: Monitor processing status with live updates
- **📥 Multiple Output Formats**: Download as `.txt` or `.docx`
- **🎨 Modern Web Interface**: Beautiful, responsive UI built with HTML/CSS/JavaScript
- **⚡ High Performance**: Advanced image preprocessing for optimal accuracy

## 🏗️ Project Structure

```
vit hack/
├── app.py                      # Main FastAPI application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies (No Poppler!)
├── utils/
│   ├── __init__.py
│   ├── preprocess.py          # Image preprocessing
│   ├── ocr_engine.py          # OCR engine implementations
│   └── postprocess.py         # Text cleaning and correction
├── templates/
│   └── index.html             # Web interface
└── static/
    ├── uploads/               # Temporary upload storage
    └── outputs/               # Processed text outputs
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

**✨ That's it! No Poppler, no external tools needed!**

### Setup Steps

1. **Clone or download this repository**

2. **Navigate to the project directory**
```cmd
cd "d:\vit hack"
```

3. **Create a virtual environment (recommended)**
```cmd
python -m venv venv
venv\Scripts\activate
```

4. **Install dependencies**
```cmd
pip install -r requirements.txt
```

5. **Download TextBlob corpora (for spell checking)**
```cmd
python -m textblob.download_corpora
```

6. **(Optional) Setup Gemini API for Answer Evaluation**
```cmd
# Get your API key from https://makersuite.google.com/app/apikey
# Set environment variable
set GEMINI_API_KEY=your_api_key_here
```

See [GEMINI_EVALUATION_GUIDE.md](GEMINI_EVALUATION_GUIDE.md) for detailed setup instructions.

## ⚙️ Configuration

Edit `config.py` to customize settings:

```python
# Choose default OCR engine
OCR_ENGINE = "easyocr"  # Options: 'easyocr', 'google_vision'

# Adjust image quality
DPI = 300  # Higher = better quality but slower

# Enable/disable preprocessing steps
PREPROCESS_CONFIG = {
    "grayscale": True,
    "deskew": True,
    "denoise": True,
    "enhance_contrast": True,
}

# Configure postprocessing
POSTPROCESS_CONFIG = {
    "remove_extra_spaces": True,
    "spell_check": True,  # Set to False for faster processing
    "min_confidence": 0.5,
}
```

### Google Vision API Setup (Optional)

1. Create a Google Cloud project
2. Enable the Vision API
3. Download credentials JSON file
4. Set environment variable:
```cmd
set GOOGLE_APPLICATION_CREDENTIALS=path\to\credentials.json
```

## 🎯 Usage

### Starting the Server

```cmd
python app.py
```

The application will start at `http://localhost:8000`

### Using the Web Interface

1. **Open your browser** and navigate to `http://localhost:8000`
2. **Upload an image**: Drag and drop or click to browse (JPG, PNG, BMP, TIFF, WebP)
3. **Select OCR Engine**: Choose from EasyOCR or Google Vision (if configured)
4. **Click "Upload & Extract Text"**
5. **Monitor Progress**: Watch real-time status updates
6. **View Results**: See extracted text with confidence scores
7. **Download**: Get your results as TXT or DOCX

### API Endpoints

#### Upload File
```http
POST /upload
Content-Type: multipart/form-data

file: <Image file>
ocr_engine: easyocr|google_vision
```

#### Check Status
```http
GET /status/{job_id}
```

#### Get Result
```http
GET /result/{job_id}
```

#### Download File
```http
GET /download/{job_id}/txt
GET /download/{job_id}/docx
```

#### Cleanup Job
```http
DELETE /cleanup/{job_id}
```

## 🔧 Advanced Usage

### Command Line Processing

You can also use the utilities directly in Python:

```python
from utils.preprocess import preprocess_image
from utils.ocr_engine import create_ocr_engine
from utils.postprocess import postprocess_text, create_output_file
from PIL import Image

# Load image
image = Image.open("handwritten_note.jpg")

# Preprocess
from utils.preprocess import ImagePreprocessor
preprocessor = ImagePreprocessor()
processed_image = preprocessor.preprocess(image)

# OCR
ocr = create_ocr_engine('easyocr')
result = ocr.recognize_text(processed_image)

# Postprocess
final_text = postprocess_text(result.text)

# Save
create_output_file(final_text, "output", format="docx")
```

## 📊 Performance Comparison

| OCR Engine | Speed | Accuracy | GPU Support | Best For |
|------------|-------|----------|-------------|----------|
| **EasyOCR** | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ Excellent | ✅ Yes | Handwritten text, general use |
| **Google Vision** | ⚡ Slower (API) | ⭐⭐⭐⭐⭐ Best | ☁️ Cloud | Highest quality, requires API key |

**Note**: EasyOCR provides excellent accuracy for handwritten documents and is recommended for most use cases.

## 🐛 Troubleshooting

### Common Issues

**Error: "No module named 'fastapi'"**
- Solution: Run `fix_install.bat` or `pip install -r requirements.txt`

**Low OCR Accuracy**
- Ensure good image quality (high resolution, good lighting)
- Try adjusting preprocessing settings in `config.py`
- Check if preprocessing is enabled in config

**Out of Memory Error**
- Reduce image size before processing
- Use CPU instead of GPU if memory is limited
- Process one image at a time

**Slow Processing**
- Enable GPU if available (EasyOCR supports CUDA)
- Disable spell checking in config
- Resize large images before processing

## 🎨 Customization

### Modify the UI

Edit `templates/index.html` to customize colors, layout, or add features.

### Add New OCR Engine

1. Create a new class in `utils/ocr_engine.py` extending `BaseOCREngine`
2. Implement the `recognize()` method
3. Register it in `OCREngine.ENGINES` dictionary

### Custom Preprocessing

Add your own preprocessing steps in `utils/preprocess.py`:

```python
def _custom_preprocessing(self, image: np.ndarray) -> np.ndarray:
    # Your custom logic here
    return processed_image
```

## 📦 Dependencies

Key libraries:
- **FastAPI**: Modern web framework
- **Pillow**: Image processing
- **OpenCV**: Image preprocessing
- **EasyOCR**: OCR engine for handwritten text
- **TextBlob**: Spell checking
- **python-docx**: DOCX generation
- **Google Cloud Vision**: Optional cloud OCR (requires API key)

**No Poppler or pdf2image needed! No PyTorch needed!**

See `requirements.txt` for complete list.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [Google Cloud Vision](https://cloud.google.com/vision)
- [OpenCV](https://opencv.org/)
- [FastAPI](https://fastapi.tiangolo.com/)

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section above

---

**Made with ❤️ for better handwritten text extraction**
