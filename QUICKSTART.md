# 🚀 Quick Start Guide

## Get Started in 2 Steps (No Poppler Needed!)

### Step 1: Setup the Application

**Windows:**
```cmd
fix_install.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh run.sh
./setup.sh
```

### Step 2: Run the Application

**Windows:**
```cmd
run.bat
```

**macOS/Linux:**
```bash
./run.sh
```

Then open your browser and go to: **http://localhost:8000**

## 🎯 First Time Usage

1. **Upload an Image**: Click or drag-and-drop a handwritten image (JPG, PNG, etc.)
2. **Choose OCR Engine**: 
   - **EasyOCR** (recommended, fast and accurate)
   - **Google Vision** (requires API credentials, highest quality)
3. **Process**: Click "Upload & Extract Text"
4. **Download**: Get your extracted text as TXT or DOCX

## ⚡ Tips for Best Results

- **Use high-quality images** (clear, well-lit photos)
- **Avoid blurry or low-resolution images**
- **Good contrast** between text and background works best
- **EasyOCR** works great for both handwritten and printed text
- **For highest quality**: Use Google Vision API (if configured)

## 🔧 Customization

Edit `config.py` to change:
- Default OCR engine
- Preprocessing settings
- Maximum file size

## 📚 More Information

See `README.md` for:
- Detailed API documentation
- Advanced usage examples
- Performance comparison
- Troubleshooting guide

---

**Need help?** Check the README.md or open an issue!
