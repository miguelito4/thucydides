#!/usr/bin/env python3
"""
Improved gap filler with better JSON error handling.
Use this instead of fill_gaps.py for the remaining 33 chunks.
"""

import sys
import json
import re
sys.path.insert(0, '.')

from src.enricher import ThucydidesEnricher
from src.utils import load_json, save_json, get_project_root

# Missing chunks from your latest check
missing = [42, 143, 181, 222, 246, 247, 266, 275, 290, 353, 365, 366, 372, 377, 378, 382, 387, 412, 414, 415, 448, 452, 478, 479, 480, 481, 482, 483, 494, 495, 496, 501, 502]

def clean_json_response(text: str) -> str:
    """Clean JSON response - remove markdown and common issues."""
    text = text.strip()
    
    # Remove markdown code fences
    text = re.sub(r'^```(?:json)?\s*\n?', '', text)
    text = re.sub(r'\n?```\s*$', '', text)
    text = text.strip()
    
    # Try to find JSON object boundaries if there's extra text
    start = text.find('{')
    end = text.rfind('}')
    
    if start != -1 and end != -1 and start > 0:
        text = text[start:end+1]
    
    # Remove trailing commas before closing braces/brackets
    text = re.sub(r',(\s*[}\]])', r'\\1', text)
    
    return text

def enrich_chunk_with_retry(enricher, chunk_id, max_retries=2):
    """Enrich a chunk with retry logic and better JSON handling."""
    
    for attempt in range(max_retries):
        try:
            # Load current chunks
            chunks = enricher.load_chunks()
            chunk = chunks[chunk_id]
            
            # Create prompt and get response
            prompt = enricher.create_enrichment_prompt(chunk)
            
            message = enricher.client.messages.create(
                model=enricher.model,
                max_tokens=enricher.config['anthropic']['max_tokens'],
                temperature=enricher.config['anthropic']['temperature'],
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            
            # Clean and parse JSON
            cleaned = clean_json_response(response_text)
            
            try:
                enriched_content = json.loads(cleaned)
            except json.JSONDecodeError:
                # Try even more aggressive cleaning
                # Remove any text before first { and after last }
                cleaned = re.sub(r'^[^{]*', '', cleaned)
                cleaned = re.sub(r'[^}]*$', '', cleaned)
                enriched_content = json.loads(cleaned)
            
            # Success! Save it
            chunk['enriched'] = enriched_content
            chunk['enrichment_model'] = enricher.model
            chunks[chunk_id] = chunk
            
            # Save back to file
            enricher._save_enriched_chunks(chunks)
            
            return True, None
            
        except json.JSONDecodeError as e:
            error_msg = f"JSON parse error (attempt {attempt + 1}/{max_retries}): {str(e)}"
            print(f"  ⚠ {error_msg}")
            
            if attempt < max_retries - 1:
                print(f"  → Retrying chunk {chunk_id}...")
                continue
            else:
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"  ✗ {error_msg}")
            return False, error_msg
    
    return False, "Max retries exceeded"


# Main execution
if __name__ == "__main__":
    enricher = ThucydidesEnricher()
    
    print(f"\n{'='*60}")
    print(f"FILLING {len(missing)} MISSING CHUNKS WITH IMPROVED ERROR HANDLING")
    print(f"{'='*60}\n")
    
    successful = []
    failed = []
    
    for i, chunk_id in enumerate(missing, 1):
        print(f"[{i}/{len(missing)}] Enriching chunk {chunk_id}...")
        
        success, error = enrich_chunk_with_retry(enricher, chunk_id)
        
        if success:
            print(f"  ✓ Chunk {chunk_id} complete\n")
            successful.append(chunk_id)
        else:
            print(f"  ✗ Chunk {chunk_id} FAILED: {error}\n")
            failed.append(chunk_id)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"ENRICHMENT COMPLETE")
    print(f"{'='*60}")
    print(f"✓ Successful: {len(successful)}/{len(missing)}")
    print(f"✗ Failed: {len(failed)}/{len(missing)}")
    
    if failed:
        print(f"\nFailed chunks: {failed}")
        print(f"\nTo retry failed chunks, update the 'missing' list in this script and run again.")
    else:
        print(f"\n🎉 ALL CHUNKS ENRICHED! Ready to build the site!")
