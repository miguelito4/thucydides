"""
WordPress Publisher for Thucydides daily reader.
Publishes enriched chunks to WordPress via their REST API.
"""

import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from src.utils import (
    load_config, get_api_keys, load_json, 
    get_project_root, mark_as_published, 
    get_next_chunk_to_publish, get_chunk_title
)


class WordPressPublisher:
    """Publish enriched Thucydides chunks to WordPress."""
    
    def __init__(self):
        self.config = load_config()
        self.api_keys = get_api_keys()
        self.site_url = self.api_keys['wordpress_site_url']

        # Construct API base URL
        self.api_base = f"https://public-api.wordpress.com/wp/v2/sites/{self.site_url}"

        # Create authentication header using OAuth
        access_token = self.api_keys.get('wordpress_access_token')
    
        # Validate credentials
        if not all([self.site_url, access_token]):
            raise ValueError("WordPress credentials must be set in environment variables (.env file)")
    
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    
    def load_chunks(self) -> list:
        """Load enriched chunks from JSON."""
        chunks_path = get_project_root() / self.config['paths']['processed_chunks']
        return load_json(chunks_path)
    
    def format_post(self, chunk: Dict[str, Any]) -> Dict[str, str]:
        """Format a chunk as a WordPress post."""
        enriched = chunk.get('enriched', {})
        
        title = get_chunk_title(chunk)
        
        # Build the post content in HTML
        content_parts = []
        
        # Header with progress
        total_chunks = len(self.load_chunks())
        progress_pct = ((chunk['chunk_index'] + 1) / total_chunks) * 100
        content_parts.append(f"<p><em>Day {chunk['chunk_index'] + 1} of {total_chunks} • Book {chunk['book']}, Chapter {chunk['chapter']} • {progress_pct:.1f}% Complete</em></p>\n")
        
        # Original Text section
        content_parts.append("<h2>Original Text (Crawley Translation)</h2>\n")
        content_parts.append(f"<p>{chunk['original_text']}</p>\n")
        content_parts.append("<hr>\n")
        
        if enriched:
            # Modern Translation
            if 'modern_translation' in enriched:
                content_parts.append("<h2>Modern Translation</h2>\n")
                content_parts.append(f"<p>{enriched['modern_translation']}</p>\n")
                content_parts.append("<hr>\n")
            
            # Historical Context
            if 'context' in enriched:
                content_parts.append("<h2>What's Happening</h2>\n")
                content_parts.append(f"<p>{enriched['context']}</p>\n")
                content_parts.append("<hr>\n")
            
            # Key Themes
            if 'key_themes' in enriched and enriched['key_themes']:
                content_parts.append("<h2>Key Themes</h2>\n<ul>\n")
                for theme in enriched['key_themes']:
                    content_parts.append(f"<li>{theme}</li>\n")
                content_parts.append("</ul>\n")
            
            # Annotations
            if 'annotations' in enriched and enriched['annotations']:
                content_parts.append("<h2>Annotations</h2>\n")
                for ann in enriched['annotations']:
                    content_parts.append(f"<h3>{ann['topic']}</h3>\n")
                    content_parts.append(f"<p>{ann['explanation']}</p>\n")
                    if ann.get('link'):
                        content_parts.append(f"<p><a href=\"{ann['link']}\">Learn more</a></p>\n")
            
            # Vocabulary
            if 'vocabulary' in enriched and enriched['vocabulary']:
                content_parts.append("<h2>Important Terms</h2>\n<ul>\n")
                for term in enriched['vocabulary']:
                    if isinstance(term, dict):
                        content_parts.append(f"<li><strong>{term.get('term', 'Term')}</strong>: {term.get('definition', '')}</li>\n")
                    else:
                        content_parts.append(f"<li>{term}</li>\n")
                content_parts.append("</ul>\n")
            
            # Parallel Accounts
            if 'parallel_accounts' in enriched and enriched['parallel_accounts']:
                content_parts.append("<h2>Parallel Accounts from Other Ancient Historians</h2>\n")
                for acc in enriched['parallel_accounts']:
                    content_parts.append(f"<h3>{acc['author']}: <em>{acc['work']}</em> ({acc['reference']})</h3>\n")
                    content_parts.append(f"<p>{acc['relevance']}</p>\n")
                    if acc.get('link'):
                        content_parts.append(f"<p><a href=\"{acc['link']}\">Read the passage</a></p>\n")
            
            # Related Passages in Thucydides
            if 'related_passages' in enriched and enriched['related_passages']:
                content_parts.append("<h2>Related Passages in Thucydides</h2>\n")
                for passage in enriched['related_passages']:
                    content_parts.append(f"<p><strong>Book {passage['book']}, Chapter {passage['chapter']}</strong>: {passage['summary']} ")
                    content_parts.append(f"<em>({passage['connection']})</em></p>\n")
            
            # Discussion Prompts
            if 'discussion_prompts' in enriched and enriched['discussion_prompts']:
                content_parts.append("<h2>Discussion Questions</h2>\n<ol>\n")
                for prompt in enriched['discussion_prompts']:
                    content_parts.append(f"<li>{prompt}</li>\n")
                content_parts.append("</ol>\n")
        
        # Footer
        content_parts.append("<hr>\n")
        content_parts.append(f"<p><em>Reading Thucydides daily at <a href=\"https://{self.site_url}\">thucydides.caseyjr.org</a></em></p>")
        
        body = ''.join(content_parts)
        
        return {
            'title': title,
            'body': body
        }
    
    def publish_post(self, chunk: Dict[str, Any], published_at: Optional[str] = None) -> Dict[str, Any]:
        """Publish a single chunk to WordPress."""
        post_data = self.format_post(chunk)
        
        # WordPress post payload
        category_id = self.get_thucydides_category_id()
        payload = {
            'title': post_data['title'],
            'content': post_data['body'],
            'status': 'publish',
            'date': published_at or datetime.now().isoformat()
        }
        
        # Only add categories if we got a valid ID
        if category_id is not None:
            payload['categories'] = [category_id]

        print(f"\nPublishing: {post_data['title']}")
        print(f"Character count: {len(post_data['body'])}")
        
        # WordPress API endpoint
        url = f"{self.api_base}/posts"
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            post_id = result.get('id', 'unknown')
            post_url = result.get('link', 'unknown')
            
            print(f"✓ Successfully published! Post ID: {post_id}")
            print(f"URL: {post_url}")
            
            mark_as_published(chunk['chunk_index'], str(post_id))
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error publishing: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise
    
    def get_thucydides_category_id(self) -> Optional[int]:
        """Get or create the Thucydides category and return its ID."""
        url = f"{self.api_base}/categories"
        
        # First, search for existing category
        params = {'search': 'Thucydides'}
        try:
            print(f"Searching for Thucydides category...")
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            categories = response.json()
            
            print(f"Found {len(categories)} matching categories")
            
            if categories:
                category_id = categories[0]['id']
                print(f"Using existing category ID: {category_id}")
                return category_id
            
            # Category doesn't exist, create it
            print("Category not found, creating new one...")
            payload = {'name': 'Thucydides', 'slug': 'thucydides'}
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            new_category = response.json()
            category_id = new_category['id']
            print(f"Created new category with ID: {category_id}")
            return category_id
        
        except Exception as e:
            print(f"Warning: Could not set category: {e}")
            return None
            
        except Exception as e:
            print(f"Warning: Could not set category: {e}")
            return None
    
    def publish_next(self) -> Optional[Dict[str, Any]]:
        """Publish the next unpublished chunk."""
        next_index = get_next_chunk_to_publish()
        chunks = self.load_chunks()
        
        if next_index >= len(chunks):
            print("All chunks have been published!")
            return None
        
        chunk = chunks[next_index]
        
        if 'enriched' not in chunk:
            print(f"Warning: Chunk {next_index} has not been enriched yet.")
            print("Run the enricher first: python src/enricher.py")
            return None
        
        return self.publish_post(chunk)
    
    def preview_post(self, chunk_index: int) -> str:
        """Preview what a post would look like without publishing."""
        chunks = self.load_chunks()
        
        if chunk_index >= len(chunks):
            raise ValueError(f"Chunk index {chunk_index} out of range")
        
        chunk = chunks[chunk_index]
        post_data = self.format_post(chunk)
        
        print(f"\n{'='*60}")
        print(f"PREVIEW: {post_data['title']}")
        print(f"{'='*60}\n")
        print(post_data['body'][:2000] + "..." if len(post_data['body']) > 2000 else post_data['body'])
        print(f"\n{'='*60}")
        print(f"Character count: {len(post_data['body'])}")
        
        return post_data['body']
    
    def test_connection(self) -> bool:
        """Test the WordPress API connection."""
        print("Testing WordPress API connection...")
        
        url = f"{self.api_base}/posts"
        params = {'per_page': 1}
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            print("✓ Successfully connected to WordPress API")
            
            posts = response.json()
            print(f"Found {len(posts)} recent posts")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response: {e.response.text}")
            return False


def main():
    """Run the publisher."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Publish Thucydides chunks to WordPress')
    parser.add_argument('--test', action='store_true', help='Test API connection')
    parser.add_argument('--preview', type=int, help='Preview a chunk without publishing')
    parser.add_argument('--chunk', type=int, help='Publish a specific chunk by index')
    parser.add_argument('--next', action='store_true', help='Publish the next unpublished chunk')
    
    args = parser.parse_args()
    
    publisher = WordPressPublisher()
    
    if args.test:
        publisher.test_connection()
    elif args.preview is not None:
        publisher.preview_post(args.preview)
    elif args.chunk is not None:
        chunks = publisher.load_chunks()
        publisher.publish_post(chunks[args.chunk])
    elif args.next:
        publisher.publish_next()
    else:
        publisher.publish_next()


if __name__ == '__main__':
    main()
