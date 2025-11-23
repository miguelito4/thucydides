#!/usr/bin/env python3
"""
Nuclear option: Ultra-aggressive JSON fixer for stubborn chunks.
This will try multiple repair strategies.
"""

import sys
import json
import re
sys.path.insert(0, '.')

from src.enricher import ThucydidesEnricher

# The 14 stubborn chunks
missing = [143, 222, 246, 275, 353, 377, 412, 415, 452, 478, 480, 482, 483, 494]

def fix_json_delimiters(text: str) -> str:
    """Fix common delimiter issues in JSON."""
    # Remove trailing commas before closing braces/brackets
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    
    # Fix missing commas between array elements (common issue)
    # Look for patterns like: }"  {" and add comma
    text = re.sub(r'"\s*\n\s*"', '",\n"', text)
    
    # Fix missing commas between object properties
    # Look for patterns like: }  "key" and add comma  
    text = re.sub(r'}\s*\n\s*"', '},\n"', text)
    
    # Fix missing commas in arrays
    # Look for patterns like: ]  [
    text = re.sub(r']\s*\n\s*\[', '],\n[', text)
    
    return text

def nuclear_json_clean(text: str) -> str:
    """Most aggressive JSON cleaning possible."""
    text = text.strip()
    
    # Remove any markdown
    text = re.sub(r'^```(?:json)?\s*\n?', '', text)
    text = re.sub(r'\n?```\s*$', '', text)
    
    # Extract just the JSON object
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        text = text[start:end+1]
    
    # Fix delimiter issues
    text = fix_json_delimiters(text)
    
    # Remove any control characters that might cause issues
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    return text

def manual_json_repair(text: str) -> dict:
    """
    Last resort: manually extract fields even if JSON is broken.
    Returns a dict with whatever we can salvage.
    """
    result = {}
    
    try:
        # Extract modern_translation
        match = re.search(r'"modern_translation"\s*:\s*"((?:[^"\\]|\\.)*)"\s*,', text, re.DOTALL)
        if match:
            result['modern_translation'] = match.group(1).replace('\\"', '"').replace('\\n', '\n')
        
        # Extract context
        match = re.search(r'"context"\s*:\s*"((?:[^"\\]|\\.)*)"\s*,', text, re.DOTALL)
        if match:
            result['context'] = match.group(1).replace('\\"', '"').replace('\\n', '\n')
        
        # Extract key_themes as array
        match = re.search(r'"key_themes"\s*:\s*\[(.*?)\]', text, re.DOTALL)
        if match:
            themes_text = match.group(1)
            themes = re.findall(r'"([^"]*)"', themes_text)
            result['key_themes'] = themes
        
        # If we got at least modern_translation and context, it's usable
        if len(result) >= 2:
            return result
    except Exception as e:
        print(f"    Manual repair failed: {e}")
    
    return None

def enrich_with_nuclear_option(enricher, chunk_id):
    """Try everything to get this chunk enriched."""
    
    try:
        chunks = enricher.load_chunks()
        chunk = chunks[chunk_id]
        prompt = enricher.create_enrichment_prompt(chunk)
        
        # Get response
        message = enricher.client.messages.create(
            model=enricher.model,
            max_tokens=enricher.config['anthropic']['max_tokens'],
            temperature=enricher.config['anthropic']['temperature'],
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        
        # Strategy 1: Nuclear clean
        try:
            cleaned = nuclear_json_clean(response_text)
            enriched_content = json.loads(cleaned)
            chunk['enriched'] = enriched_content
            chunk['enrichment_model'] = enricher.model
            chunks[chunk_id] = chunk
            enricher._save_enriched_chunks(chunks)
            return True, "nuclear_clean"
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Manual repair
        manual_result = manual_json_repair(response_text)
        if manual_result:
            chunk['enriched'] = manual_result
            chunk['enrichment_model'] = enricher.model
            chunk['enrichment_status'] = 'partial'
            chunks[chunk_id] = chunk
            enricher._save_enriched_chunks(chunks)
            return True, "manual_repair"
        
        return False, "all_strategies_failed"
        
    except Exception as e:
        return False, str(e)

# Main execution
if __name__ == "__main__":
    enricher = ThucydidesEnricher()
    
    print(f"\n{'='*60}")
    print(f"NUCLEAR OPTION: ENRICHING {len(missing)} STUBBORN CHUNKS")
    print(f"{'='*60}\n")
    
    successful = []
    failed = []
    methods = {}
    
    for i, chunk_id in enumerate(missing, 1):
        print(f"[{i}/{len(missing)}] Enriching chunk {chunk_id}...")
        
        success, method = enrich_with_nuclear_option(enricher, chunk_id)
        
        if success:
            print(f"  ✓ Chunk {chunk_id} complete (method: {method})\n")
            successful.append(chunk_id)
            methods[chunk_id] = method
        else:
            print(f"  ✗ Chunk {chunk_id} FAILED: {method}\n")
            failed.append(chunk_id)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"NUCLEAR ENRICHMENT COMPLETE")
    print(f"{'='*60}")
    print(f"✓ Successful: {len(successful)}/{len(missing)}")
    print(f"✗ Failed: {len(failed)}/{len(missing)}")
    
    if successful:
        print(f"\nSuccess methods used:")
        for chunk_id, method in methods.items():
            print(f"  Chunk {chunk_id}: {method}")
    
    if failed:
        print(f"\nFailed chunks: {failed}")
        print(f"These chunks may need manual intervention.")
    else:
        print(f"\n🎉 ALL CHUNKS ENRICHED! Ready to build the site!")
