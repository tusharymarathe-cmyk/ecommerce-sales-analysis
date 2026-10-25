# Git and GitHub Guide
## E-Commerce Sales Analysis Project — Week 6 Internship Assignment

---

## Table of Contents
1. [What is Git?](#what-is-git)
2. [Core Git Commands](#core-git-commands)
3. [Creating a GitHub Repository](#creating-a-github-repository)
4. [Uploading Your Project to GitHub](#uploading-your-project-to-github)
5. [Complete Git Workflow for This Project](#complete-git-workflow-for-this-project)
6. [Git Troubleshooting](#git-troubleshooting)

---

## What is Git?

**Git** is a distributed version control system that tracks changes to your files over time. It allows you to:
- Save snapshots of your project (called **commits**)
- Go back to any previous version
- Collaborate with others without overwriting each other's work
- Maintain a complete history of all changes

**GitHub** is a cloud platform that hosts Git repositories online, making it easy to share, collaborate, and showcase your work.

---

## Core Git Commands

### `git clone`
**Purpose:** Download a remote repository to your local machine

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
```

**When to use:** When you want to get a copy of an existing GitHub repository.

---

### `git status`
**Purpose:** See which files have been changed, added, or deleted

```bash
git status
```

**Output shows:**
- **Untracked files:** New files Git doesn't know about yet
- **Modified files:** Files that have been changed since the last commit
- **Staged files:** Files ready to be committed

---

### `git add`
**Purpose:** Stage files for the next commit

```bash
# Add a specific file
git add filename.py

# Add all files in a folder
git add src/

# Add ALL changed files
git add .
```

**Important:** `git add` does NOT save your work — it only prepares files for committing.

---

### `git commit`
**Purpose:** Save a snapshot of your staged files with a message

```bash
git commit -m "Add data cleaning script and cleaned dataset"
```

**Best practices for commit messages:**
- Use present tense: "Add feature" not "Added feature"
- Be specific: "Fix date parsing bug in data_cleaning.py" not "Fix bug"
- Keep it under 72 characters
- Start with a capital letter

---

### `git push`
**Purpose:** Upload your local commits to GitHub

```bash
# Push to the main branch
git push origin main

# First push (sets tracking)
git push -u origin main
```

**Requires:** GitHub authentication (see section below)

---

### `git pull`
**Purpose:** Download and merge remote changes to your local copy

```bash
git pull origin main
```

**When to use:** Before starting new work, especially when collaborating.

---

### `git log`
**Purpose:** View the commit history

```bash
# Standard log
git log

# Compact one-line format
git log --oneline

# Graphical branch view
git log --oneline --graph --all
```

---

## Creating a GitHub Repository

1. Go to **https://github.com** and sign in (or create a free account)
2. Click the **"+"** icon in the top-right corner → **"New repository"**
3. Fill in:
   - **Repository name:** `ecommerce-sales-analysis`
   - **Description:** `Week 6 Internship Assignment: E-Commerce Sales Data Analysis and Interactive Power BI Dashboard`
   - **Visibility:** Public (so evaluators can view it)
   - **DO NOT** check "Add a README file" (we already have one)
   - **DO NOT** add .gitignore or license (we have those too)
4. Click **"Create repository"**
5. Copy the repository URL — it will look like:
   `https://github.com/YOUR-USERNAME/ecommerce-sales-analysis.git`

---

## Uploading Your Project to GitHub

After creating the remote repository on GitHub, run these commands in your terminal from inside the project folder:

```bash
# Navigate to the project folder
cd "c:\Users\TUSHAR MARATHE\OneDrive\Documents\ai pROJECT\ecommerce-sales-analysis"

# Verify Git is initialized
git status

# Configure your identity (only needed once per machine)
git config user.email "your.email@example.com"
git config user.name "Your Name"

# Connect to your GitHub repository
git remote add origin https://github.com/YOUR-USERNAME/ecommerce-sales-analysis.git

# Push all commits to GitHub
git push -u origin main
```

### GitHub Authentication

When you run `git push`, GitHub will ask you to authenticate:

**Option A (Recommended): Personal Access Token (PAT)**
1. On GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scope: `repo` (Full control of private repositories)
4. Copy the token and use it as your password when prompted

**Option B: GitHub CLI**
1. Install: https://cli.github.com/
2. Run: `gh auth login`
3. Follow the browser authentication flow

**⚠️ NEVER paste your token or password into a chat. Keep it secret.**

---

## Complete Git Workflow for This Project

The following commits were made (or should be made) for this project:

### Commit 1: Initial project structure
```bash
git add .gitignore .gitattributes requirements.txt README.md
git commit -m "Initial project structure and configuration files"
```

### Commit 2: Dataset and data cleaning
```bash
git add data/ src/generate_dataset.py src/data_cleaning.py reports/data_cleaning_summary.md
git commit -m "Add synthetic dataset, data cleaning script, and cleaning report"
```

### Commit 3: EDA and visualizations
```bash
git add src/eda_analysis.py visualizations/ reports/eda_summary.md
git commit -m "Add EDA analysis script and 10 data visualizations"
```

### Commit 4: Documentation and Power BI
```bash
git add docs/ powerbi/ notebooks/
git commit -m "Add Power BI setup guide, DAX measures, and Jupyter notebook"
```

### Commit 5: Reports and presentation
```bash
git add reports/ presentation/
git commit -m "Add business insights, project report, and presentation"
```

### Commit 6: Tests and final review
```bash
git add tests/
git commit -m "Add unit tests for data cleaning pipeline"
```

---

## Checking Repository Status

```bash
# View current status
git status

# View commit history
git log --oneline

# View remote connections
git remote -v

# View branches
git branch -a
```

---

## Git Troubleshooting

| Problem | Solution |
|---------|---------|
| "fatal: not a git repository" | Run `git init` first |
| "remote origin already exists" | Run `git remote set-url origin NEW-URL` |
| Accidental commit of sensitive file | Run `git rm --cached filename` then recommit |
| Wrong commit message | Run `git commit --amend -m "New message"` (only before pushing) |
| Push rejected | Run `git pull origin main` first, resolve conflicts, then push |
| Large file error | Add the file to `.gitignore` and run `git rm --cached filename` |

---

## GitHub Repository Best Practices

1. ✅ Always include a **README.md** — it's the front page of your repository
2. ✅ Use **.gitignore** to exclude temporary and sensitive files
3. ✅ Write meaningful **commit messages** — they are your project's changelog
4. ✅ **Never commit** passwords, API keys, or personal credentials
5. ✅ Make **small, frequent commits** rather than one massive commit
6. ✅ Use **relative links** in your README for portability

---

*Guide created for Week 6 Internship Assignment — Git/GitHub section*
