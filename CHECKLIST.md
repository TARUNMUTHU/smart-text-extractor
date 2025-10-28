# ✅ Setup & Deployment Checklist

## 🚀 Initial Setup

### 1️⃣ System Requirements
- [ ] Python 3.8 or higher installed
- [ ] pip package manager available
- [ ] At least 5 GB free disk space
- [ ] Internet connection (for initial setup)

### 2️⃣ Install Poppler (REQUIRED)

#### Windows
- [ ] Download Poppler from: https://github.com/oschwartz10612/poppler-windows/releases/
- [ ] Extract to a location (e.g., `C:\Program Files\poppler`)
- [ ] Add `bin` folder to PATH environment variable
- [ ] Verify: Open Command Prompt and run `pdftoppm -v`

#### macOS
- [ ] Install Homebrew (if not already): https://brew.sh/
- [ ] Run: `brew install poppler`
- [ ] Verify: Run `pdftoppm -v` in Terminal

#### Linux (Ubuntu/Debian)
- [ ] Run: `sudo apt-get update`
- [ ] Run: `sudo apt-get install poppler-utils`
- [ ] Verify: Run `pdftoppm -v` in Terminal

### 3️⃣ Project Setup

- [ ] Navigate to project directory: `cd "d:\vit hack"`
- [ ] Run setup script:
  - Windows: `setup.bat`
  - Linux/macOS: `chmod +x setup.sh && ./setup.sh`
- [ ] Wait for dependencies to install (5-10 minutes)
- [ ] Verify no errors in installation

### 4️⃣ Configuration (Optional)

- [ ] Review `config.py` settings
- [ ] Choose default OCR engine (easyocr, trocr, or google_vision)
- [ ] Adjust DPI if needed (300 is recommended)
- [ ] Configure max file size
- [ ] Enable/disable spell checking

### 5️⃣ Verify Installation

- [ ] Run: `python check_requirements.py`
- [ ] Ensure all checks pass
- [ ] Fix any reported issues

## 🎯 First Run

### 6️⃣ Start the Application

- [ ] Run the server:
  - Windows: `run.bat`
  - Linux/macOS: `./run.sh`
- [ ] Wait for "Application startup complete" message
- [ ] Note the server URL (default: http://localhost:8000)

### 7️⃣ Test the Web Interface

- [ ] Open browser and go to http://localhost:8000
- [ ] Verify the upload interface loads
- [ ] Check all three OCR engine options are visible

### 8️⃣ Test with Sample PDF

- [ ] Prepare a sample PDF file (handwritten or printed)
- [ ] Upload via drag-and-drop or browse button
- [ ] Select an OCR engine (start with EasyOCR)
- [ ] Click "Upload & Process PDF"
- [ ] Monitor progress bar
- [ ] Verify results display correctly
- [ ] Test TXT download
- [ ] Test DOCX download

## 🔧 Optional Enhancements

### 9️⃣ GPU Acceleration (Optional)

If you have an NVIDIA GPU:
- [ ] Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads
- [ ] Install cuDNN
- [ ] Update `config.py`:
  ```python
  EASYOCR_GPU = True
  TROCR_DEVICE = "cuda"
  ```
- [ ] Restart the application
- [ ] Test processing speed improvement

### 🔟 Google Vision API (Optional)

For best OCR quality:
- [ ] Create Google Cloud account
- [ ] Create new project
- [ ] Enable Cloud Vision API
- [ ] Create service account
- [ ] Download credentials JSON file
- [ ] Set environment variable:
  - Windows: `set GOOGLE_APPLICATION_CREDENTIALS=path\to\credentials.json`
  - Linux/macOS: `export GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json`
- [ ] Update `config.py`:
  ```python
  GOOGLE_CREDENTIALS_PATH = "path/to/credentials.json"
  ```
- [ ] Test with Google Vision engine

### 1️⃣1️⃣ TrOCR Model (Optional)

For best handwriting recognition:
- [ ] First run will auto-download TrOCR model (~300 MB)
- [ ] Wait for model download to complete
- [ ] Test with handwritten PDF
- [ ] Compare results with EasyOCR

## 📊 Performance Testing

### 1️⃣2️⃣ Benchmark Different Engines

Create test matrix:
- [ ] Test EasyOCR with printed text
- [ ] Test EasyOCR with handwritten text
- [ ] Test TrOCR with printed text
- [ ] Test TrOCR with handwritten text
- [ ] Test Google Vision (if configured)
- [ ] Note processing times and accuracy
- [ ] Choose default engine based on needs

### 1️⃣3️⃣ Optimize Settings

- [ ] Test different DPI values (150, 200, 300, 400)
- [ ] Enable/disable preprocessing steps
- [ ] Test with/without spell checking
- [ ] Find optimal balance for your use case

## 🌐 Production Deployment

### 1️⃣4️⃣ Security Hardening

- [ ] Change default host/port in `config.py` if needed
- [ ] Set `DEBUG = False` in `config.py`
- [ ] Configure firewall rules
- [ ] Set up HTTPS (use reverse proxy like Nginx)
- [ ] Implement user authentication (if needed)
- [ ] Set up rate limiting

### 1️⃣5️⃣ Production Server Setup

Using Gunicorn (recommended for production):
- [ ] Install: `pip install gunicorn`
- [ ] Create systemd service (Linux):
  ```ini
  [Unit]
  Description=Smart Handwritten Text Extractor
  After=network.target

  [Service]
  User=youruser
  WorkingDirectory=/path/to/vit hack
  ExecStart=/path/to/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```
- [ ] Enable and start service
- [ ] Set up Nginx reverse proxy
- [ ] Configure SSL certificate

### 1️⃣6️⃣ Monitoring & Logging

- [ ] Set up log rotation
- [ ] Monitor disk space in uploads/outputs folders
- [ ] Set up automated cleanup of old files
- [ ] Configure error alerts
- [ ] Set up performance monitoring

## 🧪 Testing Checklist

### 1️⃣7️⃣ Test Different Scenarios

- [ ] Single-page PDF
- [ ] Multi-page PDF (10+ pages)
- [ ] Handwritten text
- [ ] Printed text
- [ ] Mixed handwritten and printed
- [ ] Tilted/skewed pages
- [ ] Low-quality scans
- [ ] High-quality scans
- [ ] Different languages (if configured)
- [ ] Large file (near size limit)

### 1️⃣8️⃣ Error Handling Tests

- [ ] Upload non-PDF file (should reject)
- [ ] Upload oversized file (should reject)
- [ ] Upload corrupted PDF
- [ ] Test with no internet (EasyOCR/TrOCR should work)
- [ ] Stop server during processing
- [ ] Multiple concurrent uploads

## 📚 Documentation

### 1️⃣9️⃣ Update Documentation

- [ ] Document your specific configuration
- [ ] Add notes about your environment
- [ ] Document any custom modifications
- [ ] Create user guide for your team
- [ ] Document API endpoints if using programmatically

## 🎓 Training & Usage

### 2️⃣0️⃣ User Training

- [ ] Create internal documentation
- [ ] Provide sample PDFs for testing
- [ ] Document best practices for scanning
- [ ] Share tips for best OCR results
- [ ] Create FAQ based on common issues

## 🔄 Maintenance

### 2️⃣1️⃣ Regular Maintenance Tasks

- [ ] Update Python packages monthly: `pip install -U -r requirements.txt`
- [ ] Clean old upload/output files
- [ ] Monitor disk usage
- [ ] Review logs for errors
- [ ] Update OCR models if available
- [ ] Backup configuration files

## ✅ Final Verification

### 2️⃣2️⃣ Complete System Check

- [ ] All dependencies installed
- [ ] Server starts without errors
- [ ] Web interface accessible
- [ ] File upload works
- [ ] All OCR engines tested (that you plan to use)
- [ ] Downloads work (TXT and DOCX)
- [ ] Cleanup functionality works
- [ ] Documentation is complete
- [ ] Team is trained (if applicable)

## 🎉 Launch Ready!

When all items are checked:
- [ ] System is ready for production use
- [ ] Backup configuration documented
- [ ] Support process defined
- [ ] Monitoring in place

---

## 📞 Support Resources

- **README.md**: Full documentation
- **QUICKSTART.md**: Quick start guide
- **WORKFLOW.md**: Processing pipeline details
- **PROJECT_SUMMARY.md**: Complete feature list
- **config_presets.py**: Configuration examples
- **test_example.py**: Testing examples
- **check_requirements.py**: System checker

---

## 🐛 Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| "Poppler not found" | Install Poppler and add to PATH |
| "Out of memory" | Reduce DPI or use CPU mode |
| "Low accuracy" | Try TrOCR, ensure good scan quality |
| "Slow processing" | Use EasyOCR, disable spell check |
| "Module not found" | Run `pip install -r requirements.txt` |
| "Port already in use" | Change PORT in config.py |

---

**Print this checklist and check off items as you complete them!**
