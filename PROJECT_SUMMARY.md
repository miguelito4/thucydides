# Daily Thucydides Project Summary

## What This Does

Transforms Thucydides' *History of the Peloponnesian War* into a 515-day educational journey with daily posts to thucydides.caseyjr.org featuring:

- Original Crawley translation text
- Modern sophisticated translation
- Historical context & analysis
- Scholarly annotations with links
- Parallel accounts from other ancient historians
- Related passages within Thucydides
- Discussion questions
- Progress tracking

## How It Works

### 1. Text Processing (One-Time Setup)
- Downloads Crawley translation from Project Gutenberg
- Divides into ~515 chunks of 2500 characters each
- AI generates enriched content for every chunk
- Saves everything to JSON files

### 2. Daily Publishing (Automated)
- GitHub Actions runs daily at 6:00 AM UTC
- Publishes next unpublished chunk to Bear Blog
- Tracks what's been published
- Commits publication log back to repository

## Key Technologies

- **Python 3.9+**: Core language
- **Anthropic Claude API**: AI content generation
- **Bear Blog API**: Publishing platform
- **GitHub Actions**: Automation
- **Project Gutenberg**: Source text

## Repository Structure

```
thucydides/
├── src/                    # Core Python modules
│   ├── parser.py          # Text chunking
│   ├── enricher.py        # AI content generation
│   ├── publisher.py       # Bear Blog posting
│   └── utils.py           # Helper functions
├── scripts/               # User-facing scripts
│   ├── process_text.py    # Main processing workflow
│   └── daily_post.py      # Daily posting script
├── data/
│   ├── raw/              # Downloaded Gutenberg text
│   ├── processed/        # Parsed & enriched chunks
│   └── published/        # Publication tracking
├── .github/workflows/    # GitHub Actions config
├── config.yaml          # Project configuration
├── .env                 # API keys (not in git)
├── README.md           # Overview
├── SETUP.md            # Detailed setup guide
└── QUICKREF.md         # Command reference
```

## Workflow

### Initial Setup (You do this once)
1. Clone repository
2. Install Python dependencies
3. Configure API keys in `.env`
4. Run: `python scripts/process_text.py --parse`
5. Run: `python scripts/process_text.py --enrich` (takes hours)
6. Test: `python scripts/daily_post.py --test`
7. Configure GitHub Secrets
8. Push to GitHub

### Daily Operation (Automated)
1. GitHub Actions triggers at 6 AM UTC
2. Script loads next unpublished chunk
3. Formats as Markdown post
4. Publishes to Bear Blog
5. Updates publication log
6. Commits log back to repository

## API Costs

**One-time setup cost** (enriching all chunks):
- ~$200-300 using Claude Sonnet 4
- Takes 8-12 hours
- Processes ~515 chunks

**Ongoing cost**: $0 (no API calls after initial enrichment)

## Important Files

- **config.yaml**: All settings and configuration
- **.env**: API keys (keep secret!)
- **data/processed/chunks.json**: All chunks with enrichment
- **data/published/log.json**: What's been published
- **.github/workflows/daily-post.yml**: Automation config

## Customization Points

1. **Chunk size**: config.yaml → `parsing.target_chunk_size`
2. **AI model**: config.yaml → `anthropic.model`
3. **Posting time**: .github/workflows/daily-post.yml → `cron`
4. **Post format**: src/publisher.py → `format_post()`
5. **AI prompts**: src/enricher.py → `create_enrichment_prompt()`
6. **Content sections**: config.yaml → `content.sections`

## Key Features

### Smart Chunking
- Respects paragraph boundaries
- Respects book/chapter divisions
- Targets 2500 characters (~350-500 words)
- Maintains narrative flow

### Rich AI Content
- Modern translation matching Warner's style
- Historical context (150-200 words)
- 3-5 scholarly annotations with links
- 2-4 parallel accounts from other historians
- 2-3 related passages in Thucydides
- 3-4 discussion prompts
- Key themes and vocabulary

### Reliable Publishing
- Automatic daily posts
- Progress tracking
- Error handling
- Manual override capability
- Preview before publishing

## Getting Started

**Absolute beginner?** Read SETUP.md

**Quick start for developers:**
```bash
git clone https://github.com/miguelito4/thucydides.git
cd thucydides
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
python scripts/process_text.py --all
python scripts/daily_post.py --test
```

**Just want commands?** Read QUICKREF.md

## Maintenance

### Regular Tasks
- Monitor daily posts (first few days especially)
- Check GitHub Actions run status
- Review publication log occasionally

### Troubleshooting
- Check GitHub Actions tab for errors
- Review SETUP.md troubleshooting section
- Test individual components:
  ```bash
  python src/parser.py
  python src/enricher.py --chunk 0
  python src/publisher.py --test
  ```

## Project Goals

1. ✅ Make Thucydides accessible with modern translation
2. ✅ Provide rich historical context
3. ✅ Connect to other ancient sources
4. ✅ Create daily reading habit
5. ✅ Fully automated publishing
6. ✅ Track progress through the work

## Future Enhancements

Potential additions:
- Social media integration (Twitter/X, Threads)
- RSS feed with enhanced content
- Discussion forum integration
- Maps showing geographic locations
- Timeline visualization
- Audio narration
- Reader comments/notes
- Mobile app
- Email newsletter version

## Credits

- **Text**: Richard Crawley translation (Project Gutenberg)
- **AI Enhancement**: Anthropic Claude
- **Platform**: Bear Blog
- **Automation**: GitHub Actions
- **Author**: Mike Casey (Portico Advisers)

## License

MIT License - See LICENSE file

Original Thucydides text is public domain.
