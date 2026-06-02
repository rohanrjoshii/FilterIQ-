# 🚀 How to Push FilterIQ to GitHub

## Step-by-Step Guide

### Step 1: Create a GitHub Account (if you don't have one)
1. Go to https://github.com
2. Click "Sign up"
3. Follow the registration process

---

### Step 2: Create a New Repository on GitHub

1. **Log in to GitHub**
2. **Click the "+" icon** in the top right corner
3. **Select "New repository"**
4. **Fill in the details:**
   - **Repository name**: `filteriq` (or `FilterIQ` or `data-filter-tool`)
   - **Description**: "Smart data filtering application - Filter Excel/CSV/PDF files using natural language queries"
   - **Visibility**: Choose "Public" (to showcase on your resume) or "Private"
   - **DO NOT** initialize with README (we already have one)
   - **DO NOT** add .gitignore (we already have one)
   - **DO NOT** choose a license (we already have one)
5. **Click "Create repository"**

---

### Step 3: Configure Git (First Time Only)

Open Terminal and run these commands:

```bash
# Set your name (will appear in commits)
git config --global user.name "Your Name"

# Set your email (use your GitHub email)
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

---

### Step 4: Initialize Git in Your Project

Navigate to your project folder and run:

```bash
# Navigate to project directory
cd "/Users/akshayjoshi/Documents/Filtering tool"

# Initialize git repository
git init

# Check git status
git status
```

---

### Step 5: Stage and Commit Your Files

```bash
# Add all files to staging
git add .

# Check what will be committed
git status

# Create your first commit
git commit -m "Initial commit: FilterIQ - Smart Data Filtering Application"
```

---

### Step 6: Connect to GitHub Repository

Replace `yourusername` with your actual GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/yourusername/filteriq.git

# Verify remote was added
git remote -v
```

**Example:**
If your GitHub username is `akshayjoshi123`, use:
```bash
git remote add origin https://github.com/akshayjoshi123/filteriq.git
```

---

### Step 7: Push to GitHub

```bash
# Rename branch to 'main' (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**If prompted for credentials:**
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (not your account password)

---

### Step 8: Create Personal Access Token (if needed)

If GitHub asks for a password and rejects it, you need a Personal Access Token:

1. **Go to GitHub** → Settings (click your profile picture)
2. **Scroll down** to "Developer settings"
3. **Click "Personal access tokens"** → "Tokens (classic)"
4. **Click "Generate new token"** → "Generate new token (classic)"
5. **Fill in:**
   - Note: "FilterIQ Repository Access"
   - Expiration: Choose your preference (90 days recommended)
   - Select scopes: ✅ Check "repo" (all repo permissions)
6. **Click "Generate token"**
7. **Copy the token** (you won't see it again!)
8. **Use this token as your password** when pushing

---

### Step 9: Verify Upload

1. Go to your GitHub repository: `https://github.com/yourusername/filteriq`
2. You should see all your files!
3. The README.md will be displayed automatically

---

### Step 10: Update README with Your Information

Before finalizing, update the README.md file:

```bash
# Edit README.md and replace:
# - [Your Name] with your actual name
# - yourusername with your GitHub username
# - your.email@example.com with your email
# - @yourtwitter with your Twitter (or remove if not applicable)

# After editing, commit and push again:
git add README.md
git commit -m "Update README with personal information"
git push
```

---

## 🎉 You're Done!

Your repository is now live at:
```
https://github.com/yourusername/filteriq
```

---

## 📋 Quick Command Reference

### Common Git Commands

```bash
# Check status
git status

# Add specific file
git add filename.py

# Add all files
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push

# Pull latest changes
git pull

# View commit history
git log

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

---

## 🔧 Troubleshooting

### Problem: "Permission denied (publickey)"

**Solution:** Use HTTPS instead of SSH (which we did above), or set up SSH keys.

### Problem: "Repository not found"

**Solution:** Check that:
1. Repository exists on GitHub
2. Username is correct in the URL
3. You have access to the repository

### Problem: "Updates were rejected"

**Solution:**
```bash
# Pull first, then push
git pull origin main --rebase
git push origin main
```

### Problem: Large files warning

**Solution:**
```bash
# If you accidentally added large files:
# Remove them from git tracking
git rm --cached path/to/large/file

# Add to .gitignore
echo "path/to/large/file" >> .gitignore

# Commit and push
git add .gitignore
git commit -m "Remove large files"
git push
```

---

## 📝 Next Steps After Pushing

### 1. Add Topics/Tags
On your GitHub repository page:
- Click the ⚙️ (settings) icon next to "About"
- Add topics: `python`, `fastapi`, `data-filtering`, `pandas`, `excel`, `csv`, `web-application`, `data-analysis`

### 2. Add Repository Description
- Click the ⚙️ icon next to "About"
- Add: "Smart data filtering application - Filter Excel/CSV/PDF files using natural language queries"
- Add website URL (if deployed): `https://filteriq.herokuapp.com`

### 3. Create a Release
- Go to "Releases" → "Create a new release"
- Tag: `v1.0.0`
- Title: "FilterIQ v1.0.0 - Initial Release"
- Description: Copy key features from README

### 4. Enable GitHub Pages (for documentation)
- Go to Settings → Pages
- Source: Deploy from a branch
- Branch: main, folder: /docs
- This will host your documentation

### 5. Add a Project Banner
Create a banner image (use Canva or Figma) and add to README:
```markdown
![FilterIQ Banner](docs/banner.png)
```

---

## 🎯 For Your Resume

Once pushed, use this on your resume:

```markdown
FilterIQ | Full-Stack Developer
• Developed data filtering application with natural language query support
• GitHub: github.com/yourusername/filteriq
• Tech Stack: Python, FastAPI, Pandas, JavaScript, Docker
• 500+ lines of code, 10+ API endpoints, 12+ filter operators
```

---

## 📸 Adding Screenshots (Optional but Recommended)

1. Take screenshots of your application
2. Create a `docs` folder: `mkdir docs`
3. Save screenshots there
4. Reference in README: `![Screenshot](docs/screenshot.png)`

---

## 🌟 Get Stars!

Share your repository:
- LinkedIn: "Excited to share my latest project..."
- Twitter: "Built a data filtering tool..."
- Reddit: r/Python, r/webdev, r/datascience
- Dev.to: Write a blog post about building it

---

**Need Help?** Check the troubleshooting section or create an issue on GitHub!

Good luck! 🚀
