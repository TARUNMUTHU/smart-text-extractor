# 🚀 Installation & Setup Guide

## Smart Handwritten Text Extractor v2.1
**AI-Powered OCR with Answer Evaluation using Gemini**

---

## 📋 Prerequisites

- **Python 3.8 or higher** (Python 3.13 recommended)
- **pip** package manager
- **Internet connection** (for downloading dependencies and AI evaluation)

---

## 🔧 Installation Steps

### Method 1: Quick Setup (Recommended)

#### Windows:

1. **Download/Clone the project**
   ```cmd
   git clone <repository-url>
   cd "vit hack"
   ```
   Or extract the ZIP file and navigate to the folder.

2. **Run the setup script**
   ```cmd
   setup.bat
   ```
   
3. **Follow the prompts**:
   - Press `y` to install Google Vision API (optional)
   - Press `y` to install Gemini AI for answer evaluation (recommended)

4. **Configure Gemini API Key** (for AI evaluation):
   - Get your free API key from: https://aistudio.google.com/app/apikey
   - Set environment variable:
     ```cmd
     set GEMINI_API_KEY=your_api_key_here
     ```

5. **Run the application**
   ```cmd
   run_with_ai.bat
   ```

6. **Open your browser**
   - Navigate to: http://localhost:8000

---

### Method 2: Manual Setup

#### Step 1: Create Virtual Environment

```cmd
python -m venv venv
venv\Scripts\activate
```

#### Step 2: Install Dependencies

```cmd
pip install -r requirements.txt
```

#### Step 3: Download TextBlob Data

```cmd
python -m textblob.download_corpora
```

#### Step 4: Configure API Keys

**For Gemini AI Evaluation (Recommended):**
```cmd
set GEMINI_API_KEY=your_gemini_api_key
```

Get your key from: https://aistudio.google.com/app/apikey

**For Google Vision OCR (Optional):**
```cmd
set GOOGLE_APPLICATION_CREDENTIALS=path\to\credentials.json
```

#### Step 5: Run the Application

```cmd
python app.py
```

Or use the provided script:
```cmd
run_with_ai.bat
```

---

## 🌐 Linux/macOS Setup

### Quick Setup:

```bash
chmod +x setup.sh run.sh
./setup.sh
```

### Run Application:

```bash
export GEMINI_API_KEY=your_api_key_here
./run.sh
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m textblob.download_corpora
python app.py
```

---

## 📦 What Gets Installed

### Core Dependencies (~500 MB):
- **FastAPI** - Web framework
- **EasyOCR** - OCR engine with models
- **OpenCV** - Image processing
- **Pillow** - Image manipulation
- **TextBlob** - Text processing

### Optional (~50 MB):
- **Google Generative AI** - Gemini for answer evaluation
- **Google Cloud Vision** - Premium OCR (requires credentials)

### Total Installation Size: ~550 MB (without venv)

---

## 🎯 First Time Usage

### 1. Start the Application

**Windows:**
```cmd
run_with_ai.bat
```

**Linux/macOS:**
```bash
./run.sh
```

### 2. Access the Web Interface

Open your browser and go to:
```
http://localhost:8000
```

### 3. Extract Handwritten Text

1. **Upload an image** (JPG, PNG, BMP, TIFF, WebP)
2. **Choose OCR engine**: 
   - EasyOCR (recommended for most cases)
   - Google Vision (if configured)
3. **Click "Upload & Extract Text"**
4. **Wait for processing** (20-60 seconds depending on image size)
5. **Download results** as TXT or DOCX

### 4. Evaluate Answers with AI (NEW!)

After text extraction:

1. Scroll to **"📊 Evaluate Answers"** section
2. Enter:
   - **Subject** (e.g., "Mathematics", "Physics")
   - **Total Marks** (e.g., 100)
   - **Answer Key** (optional - paste correct answers)
   - Or upload **reference answer sheet image**
3. Click **"🤖 Evaluate with AI"**
4. Get instant:
   - Score and grade
   - Question-by-question breakdown
   - Detailed feedback and suggestions

---

## ⚙️ Configuration

### Edit `config.py` to customize:

```python
# Default OCR engine
OCR_ENGINE = "easyocr"  # Options: 'easyocr', 'google_vision'

# Image preprocessing
PREPROCESS_CONFIG = {
    "grayscale": True,
    "deskew": True,
    "denoise": True,
    "enhance_contrast": True,
}

# Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
```

---

## 🔑 Getting API Keys

### Gemini API (Free - for Answer Evaluation)

1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key
5. Set environment variable:
   ```cmd
   set GEMINI_API_KEY=your_key_here
   ```

**Free Tier Limits:**
- 60 requests per minute
- 1,500 requests per day
- Perfect for educational use!

### Google Vision API (Optional - Premium OCR)

1. Go to: https://console.cloud.google.com/
2. Create a new project
3. Enable Vision API
4. Create service account credentials
5. Download JSON file
6. Set path:
   ```cmd
   set GOOGLE_APPLICATION_CREDENTIALS=path\to\credentials.json
   ```

---

## 🐛 Troubleshooting

### "Module not found" errors
```cmd
pip install -r requirements.txt
```

### "Gemini API not configured"
Make sure to set the environment variable:
```cmd
set GEMINI_API_KEY=your_api_key_here
```

### "Port 8000 already in use"
Kill the existing process or change port in `config.py`:
```python
PORT = 8001  # Change to different port
```

### Slow OCR processing
- Enable GPU in `config.py`:
  ```python
  EASYOCR_GPU = True
  ```
- Or use smaller images

### Package installation fails
Update pip first:
```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📂 Project Structure

```
vit hack/
├── app.py                          # Main FastAPI application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── run_with_ai.bat                 # Start with AI evaluation
├── run.bat                         # Basic start script
├── setup.bat                       # Installation script
├── utils/
│   ├── answer_evaluator.py        # Gemini AI evaluation
│   ├── ocr_engine.py              # OCR engines
│   ├── preprocess.py              # Image preprocessing
│   └── postprocess.py             # Text postprocessing
├── templates/
│   └── index.html                 # Web interface
├── static/
│   ├── uploads/                   # Uploaded files
│   └── outputs/                   # Processed results
├── README.md                      # Main documentation
├── GEMINI_EVALUATION_GUIDE.md    # AI evaluation guide
└── .env.example                   # Environment variables template
```

---

## 🚀 Quick Start Commands

### Windows:
```cmd
# First time setup
setup.bat

# Set API key
set GEMINI_API_KEY=your_key_here

# Run application
run_with_ai.bat

# Open browser to http://localhost:8000
```

### Linux/macOS:
```bash
# First time setup
chmod +x setup.sh run.sh
./setup.sh

# Set API key
export GEMINI_API_KEY=your_key_here

# Run application
./run.sh

# Open browser to http://localhost:8000
```

---

## 📖 Documentation

- **README.md** - Main documentation
- **GEMINI_EVALUATION_GUIDE.md** - AI evaluation features
- **QUICKSTART.md** - Quick start guide
- **TROUBLESHOOTING_INSTALL.md** - Installation help

---

## 🎓 Use Cases

1. **Teachers**: Grade homework and tests automatically
2. **Students**: Check your own work with instant feedback
3. **Researchers**: Digitize handwritten notes and documents
4. **Offices**: Convert handwritten forms to digital text

---

## 📊 Features

✅ **Multi-format support**: JPG, PNG, BMP, TIFF, WebP
✅ **Advanced preprocessing**: Grayscale, deskew, denoise, enhance
✅ **Multiple OCR engines**: EasyOCR, Google Vision
✅ **AI evaluation**: Automatic grading with Gemini
✅ **Detailed feedback**: Strengths, improvements, suggestions
✅ **Multiple outputs**: TXT, DOCX download
✅ **Real-time progress**: Live status updates
✅ **Modern UI**: Beautiful, responsive web interface

---

## 🤝 Support

For issues or questions:
1. Check documentation files
2. Review error messages in terminal
3. Verify API keys are set correctly
4. Ensure all dependencies are installed

---

## 📄 License

MIT License - Free to use and modify

---

## 🌟 Version

**v2.1.0** - AI Answer Evaluation with Gemini
- ✨ NEW: AI-powered answer grading
- ✨ NEW: Detailed feedback generation
- ✅ Simplified to 2 OCR engines
- ✅ No PDF dependencies needed
- ✅ Python 3.13 compatible

---

**Happy Grading! 🎉**
