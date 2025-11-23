"""
Utility functions for the Thucydides daily reader project.
"""

import os
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def load_config() -> Dict[str, Any]:
    """Load configuration from config.yaml."""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_api_keys() -> Dict[str, str]:
    """Get API keys from environment variables."""
    return {
        'anthropic': os.getenv('ANTHROPIC_API_KEY'),
        'wordpress_site_url': os.getenv('WORDPRESS_SITE_URL'),
        'wordpress_username': os.getenv('WORDPRESS_USERNAME'),
        'wordpress_access_token': os.getenv('WORDPRESS_ACCESS_TOKEN')
    }


def ensure_directories():
    """Ensure all required directories exist."""
    base_dir = Path(__file__).parent.parent
    dirs = [
        base_dir / "data" / "raw",
        base_dir / "data" / "processed",
        base_dir / "data" / "published"
    ]
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)


def save_json(data: Any, filepath: str):
    """Save data to a JSON file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(filepath: str) -> Any:
    """Load data from a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def calculate_posting_date(chunk_index: int, start_date: str = None) -> str:
    """Calculate the posting date for a given chunk index."""
    config = load_config()
    if start_date is None:
        start_date = config['schedule']['start_date']
    
    start = datetime.fromisoformat(start_date)
    post_date = start + timedelta(days=chunk_index)
    return post_date.isoformat()


def get_next_chunk_to_publish() -> Optional[int]:
    """Get the index of the next chunk that needs to be published."""
    try:
        log_path = get_project_root() / "data" / "published" / "log.json"
        if not log_path.exists():
            return 0
        
        log = load_json(log_path)
        published_indices = [entry['chunk_index'] for entry in log.get('published', [])]
        
        if not published_indices:
            return 0
        
        return max(published_indices) + 1
    except Exception as e:
        print(f"Error getting next chunk: {e}")
        return 0


def mark_as_published(chunk_index: int, post_id: str):
    """Mark a chunk as published in the log."""
    log_path = get_project_root() / "data" / "published" / "log.json"
    
    if log_path.exists():
        log = load_json(log_path)
    else:
        log = {'published': []}
    
    log['published'].append({
        'chunk_index': chunk_index,
        'post_id': post_id,
        'published_at': datetime.now().isoformat(),
        'url': f"https://thucydides.caseyjr.org/{post_id}"
    })
    
    save_json(log, log_path)


def format_progress(current_chunk: int, total_chunks: int) -> str:
    """Format reading progress as a string."""
    percentage = (current_chunk / total_chunks) * 100
    return f"Day {current_chunk + 1} of {total_chunks} ({percentage:.1f}% complete)"


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    # Remove excessive whitespace
    text = ' '.join(text.split())
    # Fix common OCR issues
    replacements = {
        ' ,': ',',
        ' .': '.',
        ' ;': ';',
        ' :': ':',
        '( ': '(',
        ' )': ')',
        '  ': ' '
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.strip()


def estimate_word_count(text: str) -> int:
    """Estimate word count of text."""
    return len(text.split())


def validate_chunk(chunk: Dict[str, Any]) -> bool:
    """Validate that a chunk has all required fields."""
    required_fields = [
        'chunk_index',
        'original_text',
        'book',
        'chapter',
        'character_count',
        'word_count'
    ]
    return all(field in chunk for field in required_fields)


def create_backup(filepath: str):
    """Create a backup of a file before modifying it."""
    path = Path(filepath)
    if path.exists():
        backup_path = path.with_suffix(path.suffix + '.backup')
        import shutil
        shutil.copy2(path, backup_path)


def get_chunk_title(chunk: Dict[str, Any]) -> str:
    """Generate a title for a chunk."""
    book = chunk.get('book', 'Unknown')
    chapter = chunk.get('chapter', 'Unknown')
    chunk_index = chunk.get('chunk_index', 0)
    
    return f"Day {chunk_index + 1}: Book {book}, Chapter {chapter}"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max_length, breaking at word boundaries."""
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length - len(suffix)]
    # Break at last space
    last_space = truncated.rfind(' ')
    if last_space > 0:
        truncated = truncated[:last_space]
    
    return truncated + suffix
