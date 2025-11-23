# Quick Reference Guide

## Common Commands

### Text Processing

```bash
# Parse Thucydides into chunks
python scripts/process_text.py --parse

# Check processing status
python scripts/process_text.py --status

# Test enrichment on first chunk
python scripts/process_text.py --test-enrich

# Enrich all chunks
python scripts/process_text.py --enrich

# Enrich specific range (chunks 0-49)
python scripts/process_text.py --enrich --start 0 --end 50

# Do everything (parse + enrich)
python scripts/process_text.py --all
```

### Publishing

```bash
# Check what would be published next
python scripts/daily_post.py --check

# Preview next post without publishing
python scripts/daily_post.py --test

# Publish the next unpublished chunk
python scripts/daily_post.py

# Publish a specific chunk
python scripts/daily_post.py --chunk 42
```

### Direct Script Usage

```bash
# Run parser directly
python src/parser.py

# Run enricher directly  
python src/enricher.py --chunk 10

# Run publisher directly
python src/publisher.py --preview 0
```

## File Locations

```
Config and credentials:
  .env                         # API keys (don't commit!)
  config.yaml                  # Settings

Source text:
  data/raw/                    # Downloaded Gutenberg text
  
Processed data:
  data/processed/chunks.json   # Parsed chunks with enrichment
  data/processed/metadata.json # Processing metadata
  
Publishing:
  data/published/log.json      # Publication tracking
```

## Environment Variables

Required in `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-...
BEAR_BLOG_API_KEY=...
BEAR_BLOG_ID=...
```

## GitHub Actions

Workflow file: `.github/workflows/daily-post.yml`

Runs daily at 6:00 AM UTC.

Required GitHub Secrets:
- `ANTHROPIC_API_KEY`
- `BEAR_BLOG_API_KEY`
- `BEAR_BLOG_ID`

## Customization

### Change chunk size:
Edit `config.yaml`:
```yaml
parsing:
  target_chunk_size: 2500
  min_chunk_size: 2000
  max_chunk_size: 3000
```

### Change AI model:
Edit `config.yaml`:
```yaml
anthropic:
  model: "claude-sonnet-4-20250514"
```

### Change post format:
Edit `src/publisher.py` → `format_post()` method

### Change AI prompts:
Edit `src/enricher.py` → `create_enrichment_prompt()` method

### Change posting time:
Edit `.github/workflows/daily-post.yml`:
```yaml
on:
  schedule:
    - cron: '0 6 * * *'  # 6:00 AM UTC
```

## Troubleshooting

### Reset and start over:
```bash
# Delete processed data
rm -rf data/processed/* data/published/*

# Keep .gitkeep files
touch data/processed/.gitkeep data/published/.gitkeep

# Start fresh
python scripts/process_text.py --parse
```

### Check for errors:
```bash
# Test parser
python src/parser.py

# Test enricher
python src/enricher.py --chunk 0

# Test publisher
python src/publisher.py --test
```

### View chunk content:
```bash
# View chunks JSON (first 100 lines)
head -n 100 data/processed/chunks.json

# View publication log
cat data/published/log.json | python -m json.tool
```

## API Cost Management

Enriching ~515 chunks costs approximately:
- Claude Sonnet 4: ~$200-300
- Claude Opus 4: ~$600-800

To reduce costs:
- Use smaller batch sizes
- Test on fewer chunks first
- Use Claude Haiku 4.5 for testing (much cheaper)

## Development Workflow

1. Make changes to source code
2. Test locally:
   ```bash
   python scripts/process_text.py --test-enrich
   python scripts/daily_post.py --test
   ```
3. Commit changes:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```

## Useful Git Commands

```bash
# Check status
git status

# View recent commits
git log --oneline -10

# Discard local changes
git checkout -- filename.py

# Pull latest from GitHub
git pull origin main

# Create a backup branch
git branch backup-$(date +%Y%m%d)
```
