"""
Parser for Thucydides' History of the Peloponnesian War.
Divides the text into ~2500 character chunks suitable for daily reading.
"""

import re
import requests
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from bs4 import BeautifulSoup
from src.utils import (
    load_config, ensure_directories, save_json, 
    clean_text, estimate_word_count
)


class ThucydidesParser:
    """Parse and chunk Thucydides' text."""
    
    def __init__(self):
        self.config = load_config()
        self.parsing_config = self.config['parsing']
        self.source_config = self.config['source']
        ensure_directories()
        
    def download_text(self) -> str:
        """Download the Crawley translation from Project Gutenberg."""
        print("Downloading Thucydides from Project Gutenberg...")
        response = requests.get(self.source_config['url'])
        response.raise_for_status()
        
        # Save raw text
        raw_path = Path(self.config['paths']['raw_text'])
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        with open(raw_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"Saved raw text to {raw_path}")
        return response.text
    
    def extract_main_text(self, full_text: str) -> str:
        """Extract the main text, removing Gutenberg headers/footers and preliminaries."""
        # First, remove Gutenberg boilerplate
        start_marker = self.source_config['start_marker']
        end_marker = self.source_config['end_marker']
        
        # Find start
        start_idx = full_text.find(start_marker)
        if start_idx == -1:
            print("Warning: Start marker not found, using full text")
            start_idx = 0
        else:
            # Skip past the marker and several lines
            start_idx = full_text.find('\n', start_idx) + 1
            start_idx = full_text.find('\n', start_idx) + 1
        
        # Find end
        end_idx = full_text.find(end_marker)
        if end_idx == -1:
            print("Warning: End marker not found")
            end_idx = len(full_text)
        
        text = full_text[start_idx:end_idx].strip()
        
        # Now find where the actual History begins (Book I)
        # Look for "BOOK I" or similar
        book_one_patterns = [
            'BOOK I',
            'FIRST BOOK',
            'Book I',
            'Book 1'
        ]
        
        actual_start = -1
        for pattern in book_one_patterns:
            idx = text.find(pattern)
            if idx != -1 and idx < len(text) // 4:  # Should be in first quarter
                actual_start = idx
                break
        
        if actual_start > 0:
            print(f"Found start of Book I at position {actual_start}, removing preliminaries")
            text = text[actual_start:]
        
        return text.strip()
    
    def identify_structure(self, text: str) -> List[Dict[str, any]]:
        """Identify books and chapters in the text."""
        # Patterns for book and chapter headers
        book_pattern = r'BOOK\s+([IVXLCDM]+)'
        chapter_pattern = r'CHAPTER\s+([IVXLCDM]+)'
        
        structure = []
        lines = text.split('\n')
        current_book = None
        current_chapter = None
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Check for book
            book_match = re.match(book_pattern, line_stripped)
            if book_match:
                current_book = self.roman_to_int(book_match.group(1))
                current_chapter = None
                structure.append({
                    'type': 'book',
                    'number': current_book,
                    'line': i,
                    'text': line_stripped
                })
                continue
            
            # Check for chapter
            chapter_match = re.match(chapter_pattern, line_stripped)
            if chapter_match:
                current_chapter = self.roman_to_int(chapter_match.group(1))
                structure.append({
                    'type': 'chapter',
                    'book': current_book,
                    'number': current_chapter,
                    'line': i,
                    'text': line_stripped
                })
        
        return structure
    
    def roman_to_int(self, s: str) -> int:
        """Convert Roman numeral to integer."""
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        result = 0
        prev_value = 0
        
        for char in reversed(s):
            value = roman_map.get(char, 0)
            if value < prev_value:
                result -= value
            else:
                result += value
            prev_value = value
        
        return result
    
    def split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs."""
        # Split on double newlines or more
        paragraphs = re.split(r'\n\s*\n', text)
        # Clean each paragraph
        paragraphs = [clean_text(p) for p in paragraphs if p.strip()]
        return paragraphs
    
    def create_chunks(self, text: str) -> List[Dict[str, any]]:
        """
        Create chunks of approximately target_chunk_size characters.
        Respects paragraph and chapter boundaries where possible.
        """
        structure = self.identify_structure(text)
        paragraphs = self.split_into_paragraphs(text)
        
        target_size = self.parsing_config['target_chunk_size']
        min_size = self.parsing_config['min_chunk_size']
        max_size = self.parsing_config['max_chunk_size']
        
        chunks = []
        current_chunk = []
        current_size = 0
        current_book = 1
        current_chapter = 1
        
        # Track structure markers
        structure_idx = 0
        
        for para in paragraphs:
            para_len = len(para)
            
            # Check if this paragraph is a book/chapter marker
            is_marker = False
            if re.match(r'BOOK\s+[IVXLCDM]+', para.strip()):
                is_marker = True
                if current_chunk:  # Save current chunk before book marker
                    chunks.append(self._finalize_chunk(
                        current_chunk, current_book, current_chapter, len(chunks)
                    ))
                    current_chunk = []
                    current_size = 0
                # Extract book number
                match = re.match(r'BOOK\s+([IVXLCDM]+)', para.strip())
                if match:
                    current_book = self.roman_to_int(match.group(1))
                continue
            
            if re.match(r'CHAPTER\s+[IVXLCDM]+', para.strip()):
                is_marker = True
                if current_chunk and current_size >= min_size:
                    chunks.append(self._finalize_chunk(
                        current_chunk, current_book, current_chapter, len(chunks)
                    ))
                    current_chunk = []
                    current_size = 0
                # Extract chapter number
                match = re.match(r'CHAPTER\s+([IVXLCDM]+)', para.strip())
                if match:
                    current_chapter = self.roman_to_int(match.group(1))
                continue
            
            # Regular paragraph
            if current_size + para_len > max_size and current_chunk:
                # Current chunk would be too large, save it
                chunks.append(self._finalize_chunk(
                    current_chunk, current_book, current_chapter, len(chunks)
                ))
                current_chunk = [para]
                current_size = para_len
            elif current_size + para_len >= target_size and current_size >= min_size:
                # Good size reached, save chunk
                current_chunk.append(para)
                chunks.append(self._finalize_chunk(
                    current_chunk, current_book, current_chapter, len(chunks)
                ))
                current_chunk = []
                current_size = 0
            else:
                # Add to current chunk
                current_chunk.append(para)
                current_size += para_len
        
        # Don't forget the last chunk
        if current_chunk:
            chunks.append(self._finalize_chunk(
                current_chunk, current_book, current_chapter, len(chunks)
            ))
        
        return chunks
    
    def _finalize_chunk(self, paragraphs: List[str], book: int, 
                       chapter: int, index: int) -> Dict[str, any]:
        """Create a chunk dictionary from accumulated paragraphs."""
        text = '\n\n'.join(paragraphs)
        return {
            'chunk_index': index,
            'book': book,
            'chapter': chapter,
            'original_text': text,
            'character_count': len(text),
            'word_count': estimate_word_count(text),
            'paragraph_count': len(paragraphs)
        }
    
    def parse_and_save(self) -> Dict[str, any]:
        """Main method: download, parse, and save chunks."""
        print("\n=== Starting Thucydides Text Parsing ===\n")
        
        # Download
        full_text = self.download_text()
        
        # Extract main text
        print("Extracting main text...")
        main_text = self.extract_main_text(full_text)
        print(f"Main text length: {len(main_text):,} characters")
        
        # Create chunks
        print("\nCreating chunks...")
        chunks = self.create_chunks(main_text)
        
        # Calculate statistics
        total_chars = sum(c['character_count'] for c in chunks)
        total_words = sum(c['word_count'] for c in chunks)
        avg_chars = total_chars / len(chunks)
        avg_words = total_words / len(chunks)
        
        print(f"\nChunking complete!")
        print(f"Total chunks: {len(chunks)}")
        print(f"Average chunk size: {avg_chars:.0f} characters ({avg_words:.0f} words)")
        print(f"Estimated reading time: {len(chunks)} days")
        
        # Save chunks
        chunks_path = Path(self.config['paths']['processed_chunks'])
        save_json(chunks, chunks_path)
        print(f"\nSaved chunks to {chunks_path}")
        
        # Save metadata
        metadata = {
            'source': self.source_config,
            'parsing_config': self.parsing_config,
            'total_chunks': len(chunks),
            'total_characters': total_chars,
            'total_words': total_words,
            'average_chunk_size': avg_chars,
            'average_word_count': avg_words,
            'parsed_at': str(Path(__file__).parent.parent)
        }
        
        metadata_path = Path(self.config['paths']['metadata'])
        save_json(metadata, metadata_path)
        print(f"Saved metadata to {metadata_path}")
        
        return metadata


def main():
    """Run the parser."""
    parser = ThucydidesParser()
    metadata = parser.parse_and_save()
    print("\n=== Parsing Complete ===")
    print(f"\nYou now have {metadata['total_chunks']} chunks ready for enrichment!")
    print("Next step: Run the enricher to generate AI content for each chunk.")


if __name__ == '__main__':
    main()
