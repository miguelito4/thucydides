# Daily Thucydides

An automated daily reader of Thucydides' *History of the Peloponnesian War* with AI-enhanced educational content, published to [thucydides.caseyjr.org](https://thucydides.caseyjr.org).

## Overview

This project transforms the Crawley translation of Thucydides' history into a ~515-day educational journey, with each day featuring:
- A passage of 2500 characters (~350-500 words)
- Modern translation (sophisticated prose)
- Historical context
- Scholarly annotations with links
- Parallel accounts from other ancient historians
- Related passages within Thucydides
- Discussion prompts
- Reading progress tracking

## Project Structure

```
thucydides/
├── src/                      # Source code
│   ├── parser.py            # Text parsing into chunks
│   ├── enricher.py          # AI content generation
│   ├── publisher.py         # Bear Blog API integration
│   └── utils.py             # Helper functions
├── data/
│   ├── raw/                 # Original Gutenberg text
│   ├── processed/           # Parsed chunks (JSON)
│   └── published/           # Publication tracking
├── scripts/
│   ├── setup.sh             # Initial setup script
│   ├── process_text.py      # One-time text processing
│   └── daily_post.py        # Daily posting script
├── .github/workflows/
│   └── daily-post.yml       # GitHub Actions automation
├── requirements.txt         # Python dependencies
├── config.yaml              # Configuration file
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Anthropic API key (Claude Pro)
- Bear Blog API key
- GitHub account (for automation)

### Step 1: Clone and Install

```bash
git clone https://github.com/miguelito4/thucydides.git
cd thucydides
pip install -r requirements.txt
```

### Step 2: Configure

Create a `.env` file with your credentials:

```
ANTHROPIC_API_KEY=your_anthropic_key
BEAR_BLOG_API_KEY=your_bear_blog_key
BEAR_BLOG_ID=your_blog_id
```

### Step 3: Process the Text

Download and process Thucydides' text:

```bash
python scripts/process_text.py
```

This will:
1. Download the Crawley translation from Project Gutenberg
2. Parse it into 2500-character chunks
3. Generate AI-enhanced content for each chunk
4. Save everything to `data/processed/`

### Step 4: Test Publishing

Test a single post:

```bash
python scripts/daily_post.py --test
```

### Step 5: Enable Automation

The GitHub Action will automatically post one passage per day at 6:00 AM UTC.

Set repository secrets:
- `ANTHROPIC_API_KEY`
- `BEAR_BLOG_API_KEY`
- `BEAR_BLOG_ID`

## How It Works

### Text Processing

The parser divides Thucydides into ~515 logical chunks, respecting:
- Natural paragraph breaks
- Book/chapter divisions
- Narrative flow
- 2500-character target length

### AI Enhancement

For each passage, Claude generates:

1. **Modern Translation**: Sophisticated prose matching the Warner translation style
2. **Historical Context**: What's happening in the narrative
3. **Annotations**: Links to scholarly analyses and resources
4. **Parallel Accounts**: Related passages from Herodotus, Plutarch, Xenophon
5. **Internal References**: Related sections within Thucydides
6. **Discussion Prompts**: Thoughtful questions for reflection
7. **Progress Tracking**: Current position in the overall work

### Daily Publishing

GitHub Actions runs daily to:
1. Load the next unpublished passage
2. Format it for Bear Blog
3. Publish via Bear Blog API
4. Track publication status

## Development

### Running Locally

```bash
# Process a single chunk for testing
python src/parser.py --test-chunk 10

# Regenerate enrichment for a specific chunk
python src/enricher.py --chunk-id 42 --regenerate

# Publish a specific chunk
python src/publisher.py --chunk-id 100
```

### Configuration

Edit `config.yaml` to customize:
- Chunk size parameters
- AI prompts and templates
- Publishing schedule
- Blog post formatting

## Bear Blog Integration

Posts are formatted as Markdown with:
- Title: "Day X: [Book and Chapter]"
- Publication date scheduled sequentially
- Tags: thucydides, ancient-greece, history
- Custom CSS for styling (if needed)

## License

The original text is in the public domain. AI-generated enhancements are released under MIT License.

## Acknowledgments

- Crawley translation from Project Gutenberg
- Bear Blog for hosting
- Anthropic Claude for AI enhancements
