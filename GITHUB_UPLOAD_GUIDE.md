# 🚀 HOW TO UPLOAD TO GITHUB AND USE THIS PROJECT

## PART 1: UPLOADING TO GITHUB

### Step 1: Create GitHub Account (if you don't have one)
1. Go to https://github.com
2. Click "Sign up"
3. Follow the registration steps

### Step 2: Create New Repository
1. Log in to GitHub
2. Click the "+" icon (top right) → "New repository"
3. Fill in details:
   - **Repository name**: `smart-text-extractor` (or any name)
   - **Description**: "AI-powered handwritten text extraction with answer evaluation"
   - **Public** or **Private**: Choose based on your preference
   - ✓ Check "Add a README file" (optional)
   - Choose License: MIT (recommended)
4. Click "Create repository"

### Step 3: Install Git (if not already installed)
**Windows:**
- Download from: https://git-scm.com/download/win
- Run installer with default settings

**Verify installation:**
```cmd
git --version
```

### Step 4: Upload Your Project

**Option A: Using Git Command Line (Recommended)**

Open Command Prompt in your project folder:

```cmd
cd "C:\Users\arjun\Desktop\vit hack"

# Initialize git repository
git init

# Add all files (respects .gitignore)
git add .

# Create first commit
git commit -m "Initial commit - Smart Handwritten Text Extractor v2.1"

# Connect to your GitHub repository (replace with YOUR repository URL)
git remote add origin https://github.com/YOUR_USERNAME/smart-text-extractor.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Option B: Using GitHub Desktop (Easier)**

1. Download GitHub Desktop: https://desktop.github.com
2. Install and sign in
3. Click "Add" → "Add Existing Repository"
4. Select your project folder: `C:\Users\arjun\Desktop\vit hack`
5. Click "Publish repository"
6. Choose public/private and click "Publish"

### Step 5: Verify Upload
1. Go to your GitHub repository page
2. You should see all your files uploaded
3. Files excluded by `.gitignore` won't be uploaded (like `venv/`, uploaded files, etc.)

---

## PART 2: USING THE PROJECT FROM GITHUB

### For You (on another laptop) or Others:

### Step 1: Clone the Repository

```cmd
# Navigate to where you want the project
cd C:\Users\YourName\Desktop

# Clone your repository (replace with YOUR repository URL)
git clone https://github.com/YOUR_USERNAME/smart-text-extractor.git

# Enter the project folder
cd smart-text-extractor
```

### Step 2: Install Python

**IMPORTANT: Use Python 3.8 - 3.13 (NOT 3.14)**

Download Python 3.13: https://www.python.org/downloads/release/python-3130/

During installation:
- ✓ Check "Add Python to PATH"
- ✓ Check "Install pip"

### Step 3: Create Virtual Environment

```cmd
python -m venv venv
```

### Step 4: Activate Virtual Environment

**Windows:**
```cmd
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 5: Install Dependencies

**Option A: Automatic (Recommended)**
```cmd
fix_install.bat
```

**Option B: Manual**
```cmd
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**If numpy fails (Python 3.14 issue):**
```cmd
pip install "numpy<2.3" --only-binary :all:
pip install -r requirements.txt
```

### Step 6: Get Gemini API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy your key

### Step 7: Set API Key

**Windows (Temporary):**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

**Windows (Permanent):**
1. Search "Environment Variables" in Windows
2. Click "Edit system environment variables"
3. Click "Environment Variables"
4. Under "User variables", click "New"
5. Variable name: `GEMINI_API_KEY`
6. Variable value: `your_api_key_here`
7. Click OK

**Linux/Mac:**
```bash
export GEMINI_API_KEY=your_api_key_here
```

Or add to `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export GEMINI_API_KEY=your_api_key_here' >> ~/.bashrc
```

### Step 8: Run the Application

**Windows:**
```cmd
run_with_ai.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Or manually:**
```cmd
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

python app.py
```

### Step 9: Access the Application

Open your browser and go to:
```
http://localhost:8000
```

---

## PART 3: TROUBLESHOOTING

### Problem: "Python is not recognized"
**Solution:** Reinstall Python and check "Add to PATH"

### Problem: "ModuleNotFoundError"
**Solution:**
```cmd
venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: Packages installing to wrong Python
**Solution:** Use explicit path:
```cmd
venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Problem: numpy installation fails
**Solution:** You're using Python 3.14. Use Python 3.13 instead:
```cmd
# Delete old venv
rmdir /s venv

# Make sure Python 3.13 is installed
python --version

# Create new venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: "Gemini API not configured"
**Solution:** Make sure API key is set:
```cmd
echo %GEMINI_API_KEY%  # Should show your key
```

If empty, set it again:
```cmd
set GEMINI_API_KEY=your_key_here
```

---

## PART 4: KEEPING YOUR PROJECT UPDATED

### If you make changes and want to update GitHub:

```cmd
cd "path\to\your\project"

# Check what changed
git status

# Add all changes
git add .

# Commit changes
git commit -m "Description of what you changed"

# Push to GitHub
git push
```

### If someone else (or you on another laptop) wants latest version:

```cmd
cd "path\to\your\project"
git pull
```

---

## PART 5: PROJECT STRUCTURE

```
smart-text-extractor/
├── app.py                      # Main application
├── config.py                   # Configuration
├── requirements.txt            # Python packages
├── fix_install.bat            # Quick installer
├── run_with_ai.bat            # Run script
├── utils/                     # Core modules
│   ├── answer_evaluator.py   # AI evaluation
│   ├── ocr_engine.py          # OCR engines
│   ├── preprocess.py          # Image processing
│   └── postprocess.py         # Text processing
├── templates/                 # Web interface
│   └── index.html
├── static/                    # Static files
│   ├── uploads/              # (not in git)
│   └── outputs/              # (not in git)
├── README.md                  # Documentation
├── INSTALL.md                 # Installation guide
└── .gitignore                # Git ignore rules
```

---

## PART 6: SHARING WITH OTHERS

### Share Repository Link:
```
https://github.com/YOUR_USERNAME/smart-text-extractor
```

### Others can:
1. Click the link
2. Click green "Code" button
3. Click "Download ZIP" or copy git URL
4. Follow "PART 2: USING THE PROJECT FROM GITHUB"

---

## QUICK REFERENCE CARD

### First Time Setup:
```cmd
git clone https://github.com/YOUR_USERNAME/smart-text-extractor.git
cd smart-text-extractor
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
set GEMINI_API_KEY=your_key
python app.py
```

### Daily Use:
```cmd
cd smart-text-extractor
venv\Scripts\activate
set GEMINI_API_KEY=your_key  # if not permanent
run_with_ai.bat
```

### Update from GitHub:
```cmd
cd smart-text-extractor
git pull
```

### Push Changes to GitHub:
```cmd
git add .
git commit -m "Updated feature"
git push
```

---

## IMPORTANT FILES TO KEEP

✅ Include in Git:
- All `.py` files
- `requirements.txt`
- `.bat` and `.sh` scripts
- `templates/` folder
- `static/` structure (but not contents)
- `.gitignore`
- All `.md` documentation

❌ Exclude from Git (already in .gitignore):
- `venv/` folder
- `__pycache__/` folders
- `static/uploads/*` (uploaded files)
- `static/outputs/*` (generated files)
- `.env` file (contains secrets)

---

## SUPPORT

- **Documentation**: See INSTALL.md and README.md
- **Issues**: Create issue on GitHub repository
- **API Key**: https://aistudio.google.com/app/apikey

---

**You're ready to use GitHub! 🎉**

Share your repository link with others, and they can use your project!
