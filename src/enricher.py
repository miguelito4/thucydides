"""
AI Content Enricher for Thucydides chunks.
Uses Claude to generate modern translations, context, annotations, etc.
"""

import anthropic
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.utils import (
    load_config, get_api_keys, load_json, 
    save_json, get_project_root
)


class ThucydidesEnricher:
    """Generate AI-enhanced educational content for each chunk."""
    
    def __init__(self):
        self.config = load_config()
        self.api_keys = get_api_keys()
        self.client = anthropic.Anthropic(api_key=self.api_keys['anthropic'])
        self.model = self.config['anthropic']['model']
        
    def load_chunks(self) -> List[Dict[str, Any]]:
        """Load parsed chunks from JSON."""
        chunks_path = get_project_root() / self.config['paths']['processed_chunks']
        return load_json(chunks_path)
    
    def create_enrichment_prompt(self, chunk: Dict[str, Any]) -> str:
        """Create the prompt for Claude to enrich a chunk."""
        original_text = chunk['original_text']
        book = chunk['book']
        chapter = chunk['chapter']
        chunk_index = chunk['chunk_index']
        
        prompt = f"""You are a classical scholar specializing in Thucydides and ancient Greek history. I need you to create comprehensive educational content for this passage from Thucydides' History of the Peloponnesian War (Crawley translation).

**Original Text (Book {book}, Chapter {chapter}, Day {chunk_index + 1}):**

{original_text}

---

Please provide the following sections in your response. Format your response as JSON with these exact keys:

1. **modern_translation**: A sophisticated modern English translation that captures the nuance and style of the Rex Warner translation. Maintain intellectual rigor while improving clarity and readability. Keep the same length as the original (~{chunk['word_count']} words).

2. **context**: A 150-200 word explanation of what's happening in this passage. Include:
   - The immediate historical situation
   - Key participants and their roles
   - The strategic or political significance
   - How this fits into the broader narrative

3. **annotations**: An array of 3-5 scholarly annotations. Each should be an object with:
   - "topic": The subject (e.g., "Athenian Democracy", "Naval Warfare")
   - "explanation": 50-100 word explanation
   - "link": A relevant scholarly URL (Wikipedia, ancient history encyclopedia, academic resource)
   
4. **parallel_accounts**: An array of 2-4 related passages from other ancient historians. Each should be an object with:
   - "author": Name (Herodotus, Plutarch, Xenophon, etc.)
   - "work": Title of the work
   - "reference": Book/chapter reference
   - "relevance": How it relates (50 words)
   - "link": URL to the text if available (Perseus Digital Library, etc.)

5. **related_passages**: An array of 2-3 related sections within Thucydides. Each should be an object with:
   - "book": Book number
   - "chapter": Chapter number  
   - "summary": Brief summary (30-50 words)
   - "connection": Why it's related (30 words)

6. **discussion_prompts**: An array of 3-4 thought-provoking questions for reflection, suitable for students or reading groups.

7. **key_themes**: An array of 2-4 major themes illustrated in this passage (e.g., "power and justice", "rhetoric and reality", "imperialism").

8. **vocabulary**: An array of 3-5 important terms or concepts with brief definitions.

**Important Instructions:**
- Be scholarly but accessible
- All links must be real, working URLs (use Wikipedia, Perseus Digital Library, Ancient History Encyclopedia, etc.)
- For parallel_accounts, actually cite real passages that relate to this section
- Make sure the modern_translation preserves all the content and meaning of the original
- Use proper JSON formatting

Return ONLY the JSON object, no other text."""

        return prompt
    
    def enrich_chunk(self, chunk: Dict[str, Any]) -> Dict[str, Any]:
        """Generate enriched content for a single chunk using Claude."""
        print(f"\nEnriching chunk {chunk['chunk_index']} (Book {chunk['book']}, Chapter {chunk['chapter']})...")
        
        prompt = self.create_enrichment_prompt(chunk)
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.config['anthropic']['max_tokens'],
                temperature=self.config['anthropic']['temperature'],
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Extract the response
            response_text = message.content[0].text
            
            # Parse JSON response - strip markdown code blocks
            import re
            response_text = response_text.strip()
            # Remove markdown code blocks (```json ... ``` or ``` ... ```)
            response_text = re.sub(r'^```(?:json)?\s*\n?', '', response_text)
            response_text = re.sub(r'\n?```\s*$', '', response_text)
            response_text = response_text.strip()

            enriched_content = json.loads(response_text)
            
            # Add to chunk
            chunk['enriched'] = enriched_content
            chunk['enrichment_model'] = self.model
            
            print(f"✓ Successfully enriched chunk {chunk['chunk_index']}")
            return chunk
            
        except json.JSONDecodeError as e:
            print(f"✗ JSON parsing error for chunk {chunk['chunk_index']}: {e}")
            print(f"Response was: {response_text[:200]}...")
            # Return chunk without enrichment
            return chunk
        except Exception as e:
            print(f"✗ Error enriching chunk {chunk['chunk_index']}: {e}")
            return chunk
    
    def enrich_all_chunks(self, start_index: int = 0, end_index: Optional[int] = None):
        """Enrich all chunks (or a range of chunks)."""
        chunks = self.load_chunks()
        
        if end_index is None:
            end_index = len(chunks)
        
        print(f"\n=== Starting Chunk Enrichment ===")
        print(f"Processing chunks {start_index} to {end_index - 1}")
        print(f"Total: {end_index - start_index} chunks")
        print(f"Using model: {self.model}\n")
        
        newly_enriched_count = 0
        
        for i in range(start_index, end_index):
            if i >= len(chunks):
                break
            
            chunk = chunks[i]
            
            # Skip if already enriched
            if 'enriched' in chunk:
                print(f"⏭ Skipping chunk {i} - already enriched")
                continue
            
            # Enrich the chunk
            enriched_chunk = self.enrich_chunk(chunk)
            
            # Update the chunk IN THE CHUNKS ARRAY
            chunks[i] = enriched_chunk
            newly_enriched_count += 1
            
            # Save progress every 5 chunks
            if newly_enriched_count % 5 == 0:
                self._save_enriched_chunks(chunks)
                print(f"Progress saved: {newly_enriched_count} newly enriched, {i+1}/{end_index} total processed")
        
        # Final save
        self._save_enriched_chunks(chunks)
        print(f"\n=== Enrichment Complete ===")
        print(f"Newly enriched: {newly_enriched_count} chunks")
        print(f"Total chunks in file: {len(chunks)}")
        print(f"Saved to {self.config['paths']['processed_chunks']}")
    
    def _save_enriched_chunks(self, chunks: List[Dict[str, Any]]):
        """Save enriched chunks to JSON file."""
        chunks_path = get_project_root() / self.config['paths']['processed_chunks']
        save_json(chunks, chunks_path)
    
    def enrich_single_chunk(self, chunk_index: int) -> Dict[str, Any]:
        """Enrich a single chunk by index."""
        chunks = self.load_chunks()
        
        if chunk_index >= len(chunks):
            raise ValueError(f"Chunk index {chunk_index} out of range (max: {len(chunks) - 1})")
        
        chunk = chunks[chunk_index]
        enriched_chunk = self.enrich_chunk(chunk)
        
        # Update the chunks list
        chunks[chunk_index] = enriched_chunk
        self._save_enriched_chunks(chunks)
        
        return enriched_chunk
    
    def test_enrichment(self) -> Dict[str, Any]:
        """Test enrichment on the first chunk."""
        chunks = self.load_chunks()
        if not chunks:
            raise ValueError("No chunks found. Run parser first.")
        
        print("\n=== Testing Enrichment on First Chunk ===\n")
        test_chunk = self.enrich_chunk(chunks[0])
        
        # Display results
        if 'enriched' in test_chunk:
            print("\n--- Modern Translation (first 500 chars) ---")
            print(test_chunk['enriched']['modern_translation'][:500] + "...")
            
            print("\n--- Context ---")
            print(test_chunk['enriched']['context'])
            
            print("\n--- Key Themes ---")
            for theme in test_chunk['enriched']['key_themes']:
                print(f"  • {theme}")
            
            print("\n--- Discussion Prompts ---")
            for i, prompt in enumerate(test_chunk['enriched']['discussion_prompts'], 1):
                print(f"  {i}. {prompt}")
        
        return test_chunk


def main():
    """Run the enricher."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Enrich Thucydides chunks with AI content')
    parser.add_argument('--test', action='store_true', help='Test on first chunk only')
    parser.add_argument('--chunk', type=int, help='Enrich a specific chunk by index')
    parser.add_argument('--start', type=int, default=0, help='Start index')
    parser.add_argument('--end', type=int, help='End index (exclusive)')
    parser.add_argument('--batch-size', type=int, default=10, help='Process in batches of N chunks')
    
    args = parser.parse_args()
    
    enricher = ThucydidesEnricher()
    
    if args.test:
        enricher.test_enrichment()
    elif args.chunk is not None:
        enricher.enrich_single_chunk(args.chunk)
    else:
        enricher.enrich_all_chunks(args.start, args.end)


if __name__ == '__main__':
    main()
