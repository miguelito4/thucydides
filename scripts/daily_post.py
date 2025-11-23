#!/usr/bin/env python3
"""
Daily posting script for Thucydides reader.
Publishes the next unpublished chunk to Bear Blog.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.publisher import WordPressPublisher
from src.utils import get_next_chunk_to_publish, load_json, get_project_root


def main():
    """Publish the next chunk."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Publish daily Thucydides post to Bear Blog'
    )
    parser.add_argument('--test', action='store_true',
                       help='Test mode: preview post without publishing')
    parser.add_argument('--chunk', type=int,
                       help='Publish specific chunk by index')
    parser.add_argument('--check', action='store_true',
                       help='Check which chunk would be published next')
    
    args = parser.parse_args()
    
    try:
        publisher = WordPressPublisher()
        
        if args.check:
            next_index = get_next_chunk_to_publish()
            chunks = publisher.load_chunks()
            
            if next_index >= len(chunks):
                print("All chunks have been published!")
                return 0
            
            chunk = chunks[next_index]
            print(f"\nNext to publish:")
            print(f"  Chunk index: {next_index}")
            print(f"  Book: {chunk['book']}, Chapter: {chunk['chapter']}")
            print(f"  Word count: {chunk['word_count']}")
            
            if 'enriched' not in chunk:
                print(f"  ⚠ Warning: Chunk not yet enriched")
            
            return 0
        
        if args.test:
            next_index = get_next_chunk_to_publish()
            print(f"\n=== TEST MODE: Previewing Chunk {next_index} ===\n")
            publisher.preview_post(next_index)
            print("\n(Not published - this was a preview)")
            return 0
        
        if args.chunk is not None:
            chunks = publisher.load_chunks()
            if args.chunk >= len(chunks):
                print(f"Error: Chunk {args.chunk} doesn't exist (max: {len(chunks)-1})")
                return 1
            
            chunk = chunks[args.chunk]
            print(f"\nPublishing chunk {args.chunk}...")
            result = publisher.publish_post(chunk)
            print(f"\n✓ Successfully published!")
            print(f"URL: {result.get('url', 'N/A')}")
            return 0
        
        # Default: publish next
        print(f"\n=== Daily Thucydides Posting ===")
        print(f"Time: {datetime.now().isoformat()}\n")
        
        result = publisher.publish_next()
        
        if result is None:
            print("\nNothing to publish")
            return 0
        
        print(f"\n✓ Daily post published successfully!")
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
