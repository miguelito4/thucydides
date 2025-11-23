#!/usr/bin/env python3
"""
Process Thucydides text: Download, parse, and enrich.
This is the main script to prepare the text for daily publishing.
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parser import ThucydidesParser
from src.enricher import ThucydidesEnricher
from src.utils import load_json, get_project_root


def check_prerequisites():
    """Check if required files and credentials exist."""
    print("\n=== Checking Prerequisites ===\n")
    
    issues = []
    
    # Check for .env file
    env_path = get_project_root() / '.env'
    if not env_path.exists():
        issues.append("Missing .env file with API keys")
        print("✗ .env file not found")
    else:
        print("✓ .env file found")
    
    # Check for config
    config_path = get_project_root() / 'config.yaml'
    if not config_path.exists():
        issues.append("Missing config.yaml")
        print("✗ config.yaml not found")
    else:
        print("✓ config.yaml found")
    
    if issues:
        print("\n⚠ Please fix these issues before proceeding:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    
    print("\n✓ All prerequisites met")
    return True


def run_parser():
    """Run the text parser."""
    print("\n" + "="*60)
    print("STEP 1: PARSING TEXT")
    print("="*60 + "\n")
    
    parser = ThucydidesParser()
    metadata = parser.parse_and_save()
    
    print(f"\n✓ Parsing complete: {metadata['total_chunks']} chunks created")
    return metadata


def run_enricher(start_index=0, end_index=None, test_only=False):
    """Run the AI enricher."""
    print("\n" + "="*60)
    print("STEP 2: ENRICHING CONTENT")
    print("="*60 + "\n")
    
    enricher = ThucydidesEnricher()
    
    if test_only:
        print("Running test enrichment on first chunk...\n")
        enricher.test_enrichment()
    else:
        enricher.enrich_all_chunks(start_index, end_index)
    
    print("\n✓ Enrichment complete")


def show_status():
    """Show current processing status."""
    print("\n=== Processing Status ===\n")
    
    # Check if chunks exist
    chunks_path = get_project_root() / 'data' / 'processed' / 'chunks.json'
    
    if not chunks_path.exists():
        print("Status: Not started")
        print("Next step: Run with --parse to begin")
        return
    
    chunks = load_json(chunks_path)
    total = len(chunks)
    enriched = sum(1 for c in chunks if 'enriched' in c)
    
    print(f"Total chunks: {total}")
    print(f"Enriched: {enriched} ({(enriched/total*100):.1f}%)")
    print(f"Remaining: {total - enriched}")
    
    if enriched < total:
        print(f"\nNext step: Run with --enrich to continue enrichment")
    else:
        print(f"\n✓ All chunks processed and ready for publishing!")


def main():
    parser = argparse.ArgumentParser(
        description='Process Thucydides text for daily publishing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full processing (parse + enrich all)
  python scripts/process_text.py --all
  
  # Parse text only
  python scripts/process_text.py --parse
  
  # Test enrichment on first chunk
  python scripts/process_text.py --test-enrich
  
  # Enrich all chunks
  python scripts/process_text.py --enrich
  
  # Enrich specific range
  python scripts/process_text.py --enrich --start 0 --end 10
  
  # Check status
  python scripts/process_text.py --status
        """
    )
    
    parser.add_argument('--all', action='store_true',
                       help='Run full processing pipeline (parse + enrich)')
    parser.add_argument('--parse', action='store_true',
                       help='Parse text into chunks')
    parser.add_argument('--enrich', action='store_true',
                       help='Enrich chunks with AI content')
    parser.add_argument('--test-enrich', action='store_true',
                       help='Test enrichment on first chunk only')
    parser.add_argument('--start', type=int, default=0,
                       help='Start index for enrichment (default: 0)')
    parser.add_argument('--end', type=int,
                       help='End index for enrichment (default: all)')
    parser.add_argument('--status', action='store_true',
                       help='Show processing status')
    parser.add_argument('--skip-check', action='store_true',
                       help='Skip prerequisite checks')
    
    args = parser.parse_args()
    
    # Default to showing status if no args
    if not any([args.all, args.parse, args.enrich, args.test_enrich, args.status]):
        args.status = True
    
    # Check prerequisites
    if not args.skip_check and not args.status:
        if not check_prerequisites():
            return 1
    
    try:
        if args.status:
            show_status()
        
        if args.all:
            run_parser()
            run_enricher()
        
        if args.parse:
            run_parser()
        
        if args.test_enrich:
            run_enricher(test_only=True)
        
        if args.enrich:
            run_enricher(args.start, args.end)
        
        print("\n" + "="*60)
        print("PROCESSING COMPLETE")
        print("="*60 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nProcessing interrupted by user")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
