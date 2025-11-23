# Setup Guide for Daily Thucydides

This guide walks you through setting up your automated daily Thucydides reader from scratch. No prior development experience required!

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Getting API Keys](#getting-api-keys)
4. [Processing the Text](#processing-the-text)
5. [Testing Publishing](#testing-publishing)
6. [Enabling Automation](#enabling-automation)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

You'll need:

- A computer with internet access
- A GitHub account (free)
- A Bear Blog account at thucydides.caseyjr.org (already set up)
- Claude Pro account (you have this)
- About 1-2 hours for initial setup

### Install Required Software

#### 1. Install Python

**On Mac:**
```bash
# Check if Python is already installed
python3 --version

# If not, install via Homebrew (if you have it)
brew install python3

# Or download from: https://www.python.org/downloads/
```

**On Windows:**
1. Download from https://www.python.org/downloads/
2. Run installer
3. **Important:** Check "Add Python to PATH" during installation

**On Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

#### 2. Install Git

**On Mac:**
```bash
# Check if Git is installed
git --version

# If not, install via Homebrew
brew install git

# Or download from: https://git-scm.com/download/mac
```

**On Windows:**
Download from: https://git-scm.com/download/win

**On Linux:**
```bash
sudo apt-get install git
```

---

## Initial Setup

### 1. Clone the Repository

Open your terminal (Mac/Linux) or Command Prompt (Windows) and run:

```bash
# Navigate to where you want the project
cd ~/Documents  # or wherever you prefer

# Clone your repository
git clone https://github.com/miguelito4/thucydides.git

# Enter the project directory
cd thucydides
```

### 2. Install Python Dependencies

```bash
# Install required packages
pip3 install -r requirements.txt
```

If you get permission errors, try:
```bash
pip3 install --user -r requirements.txt
```

### 3. Configure Your Credentials

Create a file named `.env` in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Now edit `.env` with your actual credentials. You'll get these in the next section.

---

## Getting API Keys

### 1. Anthropic API Key

1. Go to https://console.anthropic.com/
2. Log in with your Claude Pro account
3. Navigate to "Settings" → "API Keys"
4. Click "Create Key"
5. Copy the key and paste it into your `.env` file:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-...
   ```

**Important:** Keep this key secret! Don't share it or commit it to GitHub.

### 2. Bear Blog API Key

1. Log in to your Bear Blog dashboard
2. Go to Settings → API
3. Generate a new API key
4. Copy both the API key and your Blog ID
5. Add them to your `.env` file:
   ```
   BEAR_BLOG_API_KEY=your_key_here
   BEAR_BLOG_ID=your_blog_id_here
   ```

### Verify Your .env File

Your `.env` file should now look like:

```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx...
BEAR_BLOG_API_KEY=xxxx...
BEAR_BLOG_ID=xxxx...
```

**Never commit this file to GitHub!** It's already in `.gitignore`.

---

## Processing the Text

Now let's prepare the Thucydides text for publishing.

### 1. Parse the Text

This downloads the book from Project Gutenberg and divides it into ~515 daily chunks:

```bash
python scripts/process_text.py --parse
```

This will:
- Download the Crawley translation
- Divide it into 2500-character chunks
- Save to `data/processed/chunks.json`
- Take about 30 seconds

### 2. Test AI Enrichment

Before processing all chunks, let's test on one:

```bash
python scripts/process_text.py --test-enrich
```

This will show you what the AI-generated content looks like. Review it to make sure it meets your expectations.

### 3. Enrich All Chunks

Now let's generate content for all chunks. **This will take several hours and use significant API credits.**

#### Option A: Process Everything at Once (Recommended for overnight)

```bash
python scripts/process_text.py --enrich
```

This will process all ~515 chunks. On Claude Sonnet 4, this takes approximately:
- **Time:** 8-12 hours (running continuously)
- **API Cost:** ~$200-300 (estimate, varies by model)

#### Option B: Process in Batches

If you want to process incrementally:

```bash
# Process first 50 chunks
python scripts/process_text.py --enrich --start 0 --end 50

# Later, process next 50
python scripts/process_text.py --enrich --start 50 --end 100

# And so on...
```

#### Check Progress

At any time, see how many chunks are done:

```bash
python scripts/process_text.py --status
```

### 4. Dealing with Errors

If enrichment fails partway through:
1. The progress is saved automatically
2. Just run the command again - it will skip chunks that are already enriched
3. Check `data/processed/chunks.json` to see what's been completed

---

## Testing Publishing

Before automating, let's test publishing manually.

### 1. Test API Connection

```bash
python scripts/daily_post.py --check
```

This verifies your Bear Blog credentials are working.

### 2. Preview a Post

See what the first post will look like:

```bash
python scripts/daily_post.py --test
```

This shows the full formatted post without actually publishing it.

### 3. Publish First Post Manually

When you're ready:

```bash
python scripts/daily_post.py
```

This publishes chunk 0 (the first chunk) to your blog.

Visit https://thucydides.caseyjr.org to see it!

### 4. Publish a Specific Chunk

If you want to publish a different chunk:

```bash
python scripts/daily_post.py --chunk 5
```

---

## Enabling Automation

Now let's set up GitHub Actions to post automatically every day.

### 1. Add Secrets to GitHub

1. Go to https://github.com/miguelito4/thucydides
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Add these three secrets:

   **Secret 1:**
   - Name: `ANTHROPIC_API_KEY`
   - Value: Your Anthropic API key

   **Secret 2:**
   - Name: `BEAR_BLOG_API_KEY`
   - Value: Your Bear Blog API key

   **Secret 3:**
   - Name: `BEAR_BLOG_ID`
   - Value: Your Bear Blog ID

### 2. Push Your Code

Make sure all your processed data is committed:

```bash
# Add all files
git add .

# Commit
git commit -m "Initial setup with processed chunks"

# Push to GitHub
git push origin main
```

**Important:** The `.env` file won't be pushed (it's in `.gitignore`), but the processed chunks in `data/processed/` will be.

### 3. Verify GitHub Actions

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. You should see the "Daily Thucydides Post" workflow
4. It will run automatically every day at 6:00 AM UTC

### 4. Manual Trigger

To trigger a post immediately:

1. Go to Actions tab
2. Click "Daily Thucydides Post"
3. Click "Run workflow"
4. Click the green "Run workflow" button

---

## Troubleshooting

### "Module not found" errors

```bash
# Make sure you're in the right directory
cd ~/Documents/thucydides  # or wherever your project is

# Reinstall dependencies
pip3 install -r requirements.txt
```

### "API key not found" errors

Make sure:
1. Your `.env` file is in the project root directory
2. The keys are formatted correctly (no quotes, no spaces around =)
3. You're running commands from the project root

### Bear Blog publishing fails

Check:
1. Your Bear Blog API key is valid
2. Your Blog ID is correct
3. Your internet connection is working

Test with:
```bash
python scripts/daily_post.py --check
```

### GitHub Actions not running

Make sure:
1. You've added all three secrets in GitHub Settings
2. The workflow file is in `.github/workflows/daily-post.yml`
3. You've pushed your code to GitHub

### Chunks not enriching properly

If AI enrichment fails:
1. Check your Anthropic API key is valid
2. Check you have sufficient API credits
3. Try processing a single chunk to see the error:
   ```bash
   python src/enricher.py --chunk 0
   ```

### Need to regenerate a chunk

If a specific chunk has issues:

```bash
# Regenerate enrichment for chunk 42
python src/enricher.py --chunk 42
```

---

## Maintenance

### Checking Publication Status

See what's been published:

```bash
cat data/published/log.json
```

### Skipping Ahead

If you want to skip to a specific day:

1. Manually publish chunks until you reach the desired position
2. Or modify `data/published/log.json` to mark chunks as published

### Pausing Automation

To temporarily stop daily posts:

1. Go to GitHub → Settings → Actions
2. Disable workflows
3. Re-enable when ready to resume

---

## Getting Help

If you run into issues:

1. Check the error messages carefully
2. Review this guide
3. Check GitHub Issues for the repository
4. The log files may have more details about errors

---

## Next Steps

Once everything is running:

1. Monitor the first few days of posts
2. Adjust the AI prompts in `src/enricher.py` if needed
3. Customize the post formatting in `src/publisher.py`
4. Consider adding social media integration
5. Add analytics to track readership

Enjoy your daily Thucydides journey!
