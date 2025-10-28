# 🔧 Troubleshooting Installation Issues

## ❗ Common Issue: Pillow/Python 3.13 Compatibility

If you see errors during installation like:
```
KeyError: '__version__'
Getting requirements to build wheel did not run successfully
```

This is caused by older package versions incompatible with Python 3.13+.

## ✅ Solution: Use the Fix Script

Run this command in your terminal:

```cmd
fix_install.bat
```

This script will:
1. ✅ Upgrade pip
2. ✅ Install compatible versions of all packages
3. ✅ Let you choose which OCR engines to install
4. ✅ Download required language models

## 🚀 Quick Fix Steps

### Step 1: Run the Fix Script
```cmd
cd "d:\vit hack"
fix_install.bat
```

### Step 2: Choose Your OCR Engines

The script will ask you:

**Install TrOCR?** (for handwriting)
- Type `y` if you want the best handwriting recognition (~2GB download)
- Type `n` for faster setup (you can install later)

**Install Google Vision API?**
- Type `y` if you have Google Cloud credentials
- Type `n` to skip (recommended for testing)

### Step 3: Start the Application
```cmd
run.bat
```

Open browser: http://localhost:8000

## 🎯 Alternative: Minimal Installation

For fastest setup with basic functionality:

```cmd
cd "d:\vit hack"
venv\Scripts\activate
pip install -r requirements_minimal.txt
```

This installs only EasyOCR (fastest engine).

## 📦 Manual Installation (If Scripts Fail)

If the automated scripts don't work, install manually:

```cmd
cd "d:\vit hack"
venv\Scripts\activate

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install core dependencies
pip install fastapi "uvicorn[standard]" python-multipart aiofiles Jinja2

REM Install image processing
pip install pdf2image Pillow opencv-python numpy

REM Install EasyOCR (required)
pip install easyocr

REM Install text processing
pip install textblob python-docx
python -m textblob.download_corpora

REM Optional: Install TrOCR for handwriting
pip install torch torchvision transformers

REM Optional: Install Google Vision API
pip install google-cloud-vision
```

## 🐛 Specific Error Solutions

### Error: "ModuleNotFoundError: No module named 'fastapi'"
**Solution**: Run `fix_install.bat` or manually install:
```cmd
venv\Scripts\activate
pip install fastapi uvicorn[standard]
```

### Error: "Pillow build failed"
**Solution**: Update requirements.txt to use Pillow>=10.4.0 (already fixed)
```cmd
venv\Scripts\activate
pip install --upgrade Pillow
```

### Error: "No module named 'textblob'"
**Solution**: Install TextBlob:
```cmd
venv\Scripts\activate
pip install textblob
python -m textblob.download_corpora
```

### Error: "torch not found" or "transformers not found"
**Solution**: These are only needed for TrOCR. Skip TrOCR or install:
```cmd
venv\Scripts\activate
pip install torch torchvision transformers
```

## 🔍 Verify Installation

After installation, check everything is working:

```cmd
cd "d:\vit hack"
python check_requirements.py
```

This will show you what's installed and what's missing.

## 💡 Tips for Success

1. **Use the fix_install.bat script** - it handles everything automatically
2. **Start with minimal installation** - install only what you need first
3. **Install TrOCR later** if you need handwriting support
4. **Skip Google Vision** unless you have API credentials
5. **Always activate venv** before running pip commands

## 📊 Installation Size Guide

| Component | Size | Required? |
|-----------|------|-----------|
| Core (FastAPI, etc.) | ~50 MB | ✅ Yes |
| Image Processing | ~200 MB | ✅ Yes |
| EasyOCR | ~400 MB | ✅ Yes (one OCR needed) |
| TrOCR (PyTorch) | ~2 GB | ❌ Optional |
| Google Vision | ~20 MB | ❌ Optional |

**Total for basic setup**: ~650 MB
**Total with all features**: ~2.7 GB

## 🎯 Recommended Setup

**For Testing**: Use `fix_install.bat` and answer `n` to both TrOCR and Google Vision
- Install time: ~5 minutes
- Download size: ~650 MB
- OCR engine: EasyOCR only

**For Production**: Install everything
- Install time: ~15-20 minutes
- Download size: ~2.7 GB
- OCR engines: All three available

## 🆘 Still Having Issues?

1. **Check Python version**:
   ```cmd
   python --version
   ```
   Should be 3.8 or higher (3.13+ is fine)

2. **Check pip version**:
   ```cmd
   python -m pip --version
   ```
   Should be 20.0 or higher

3. **Check virtual environment**:
   ```cmd
   venv\Scripts\activate
   where python
   ```
   Should point to venv folder

4. **Clear pip cache** (if corruption):
   ```cmd
   pip cache purge
   ```

5. **Recreate virtual environment**:
   ```cmd
   rmdir /s /q venv
   python -m venv venv
   fix_install.bat
   ```

## ✅ Success Checklist

After running `fix_install.bat`, you should have:
- [x] Virtual environment activated
- [x] pip upgraded to latest version
- [x] FastAPI and Uvicorn installed
- [x] Image processing libraries installed
- [x] At least one OCR engine (EasyOCR)
- [x] TextBlob with corpora downloaded
- [x] No error messages

Then run:
```cmd
run.bat
```

And visit: http://localhost:8000

---

**If all else fails, see the detailed installation logs and report the specific error message.**
