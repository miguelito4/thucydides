#!/usr/bin/env python3
"""
Remap existing themes to Waltz's three levels of analysis framework.
Creates a clean, MECE taxonomy based on Man, The State, and War.
"""

import json
import sys
from pathlib import Path

# Waltz Framework: Three Levels of Analysis
WALTZ_THEMES = {
    # Level I: The Individual (Physis - Human Nature)
    "Fear, Honor, and Interest": [
        "power", "power and justice", "fear and security", "honor", 
        "prestige", "reputation", "self-interest", "rational choice"
    ],
    "Hope vs. Reality": [
        "rhetoric", "persuasion", "rhetoric and reality", "rhetoric and persuasion",
        "rhetoric and diplomatic persuasion", "appearance versus reality",
        "deception", "propaganda", "expectations"
    ],
    "The Corrosion of Morality": [
        "morality", "ethics", "justice", "brutality", "cruelty",
        "violence", "plague", "civil war", "stasis", "moral decay",
        "breakdown of norms"
    ],
    
    # Level II: The State (Polis - Domestic Structure)
    "Democracy vs. Oligarchy": [
        "democracy", "oligarchy", "athenian democracy", "spartan system",
        "political systems", "governance", "decision-making", 
        "assembly", "popular rule", "demagogues", "leadership"
    ],
    "Sea Power vs. Land Power": [
        "naval", "naval warfare", "sea power", "maritime", "fleet",
        "land warfare", "hoplite", "geography", "geography and strategy",
        "geography and strategic advantage", "environmental determinism",
        "economic development", "economic power", "resources", "wealth"
    ],
    "Civil Strife (Stasis)": [
        "stasis", "civil war", "internal conflict", "faction",
        "polarization", "revolution", "class conflict", "party politics",
        "domestic crisis"
    ],
    
    # Level III: The System (Kinesis - International Dynamics)
    "The Thucydides Trap": [
        "balance of power", "power transition", "rising power",
        "hegemony", "structural realism", "security dilemma",
        "preventive war", "fear of decline"
    ],
    "Empire and Hegemony": [
        "empire", "imperialism", "athenian empire", "hegemony",
        "imperial overreach", "expansion", "colonization", "colonial",
        "tribute", "subject allies", "autonomy"
    ],
    "Power vs. Justice (Melian Paradigm)": [
        "might makes right", "realpolitik", "necessity", "compulsion",
        "strong and weak", "inequality", "exploitation", "justice"
    ],
    "Alliance Politics": [
        "alliance", "coalition", "neutrality", "diplomatic failure",
        "alliance systems", "entrapment", "abandonment", "treaty",
        "third party", "intervention"
    ],
    "Escalation Dynamics": [
        "escalation", "spiral", "conflict escalation", "inevitability",
        "chain reaction", "domino effect", "local to systemic",
        "unintended consequences"
    ]
}

def load_chunks(chunks_path):
    """Load chunks from JSON file."""
    with open(chunks_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_chunks(chunks, chunks_path):
    """Save chunks back to JSON file."""
    with open(chunks_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

def normalize_theme(theme):
    """Normalize theme string for matching."""
    return theme.lower().strip()

def remap_theme(old_theme):
    """Map an old theme to a Waltz framework category."""
    normalized = normalize_theme(old_theme)
    
    # Check each Waltz category
    for waltz_theme, keywords in WALTZ_THEMES.items():
        for keyword in keywords:
            if keyword in normalized or normalized in keyword:
                return waltz_theme
    
    # If no match found, return None (will be manually reviewed)
    return None

def remap_all_themes(chunks):
    """Remap all themes in all chunks."""
    stats = {
        'total_chunks': len(chunks),
        'chunks_updated': 0,
        'themes_remapped': 0,
        'unmapped_themes': set()
    }
    
    for chunk in chunks:
        if not chunk.get('enriched') or not chunk['enriched'].get('key_themes'):
            continue
        
        old_themes = chunk['enriched']['key_themes']
        new_themes = set()
        
        for old_theme in old_themes:
            new_theme = remap_theme(old_theme)
            if new_theme:
                new_themes.add(new_theme)
                stats['themes_remapped'] += 1
            else:
                stats['unmapped_themes'].add(old_theme)
        
        if new_themes:
            chunk['enriched']['key_themes'] = sorted(list(new_themes))
            stats['chunks_updated'] += 1
    
    return chunks, stats

def main():
    # Path to chunks file
    chunks_path = Path('data/processed/chunks.json')
    
    if not chunks_path.exists():
        print(f"Error: {chunks_path} not found")
        sys.exit(1)
    
    print("Loading chunks...")
    chunks = load_chunks(chunks_path)
    
    print(f"\n{'='*60}")
    print("REMAPPING THEMES TO WALTZ FRAMEWORK")
    print(f"{'='*60}\n")
    
    print("New Theme Structure:")
    print("\nLevel I: The Individual (Physis)")
    print("  • Fear, Honor, and Interest")
    print("  • Hope vs. Reality")
    print("  • The Corrosion of Morality")
    
    print("\nLevel II: The State (Polis)")
    print("  • Democracy vs. Oligarchy")
    print("  • Sea Power vs. Land Power")
    print("  • Civil Strife (Stasis)")
    
    print("\nLevel III: The System (Kinesis)")
    print("  • The Thucydides Trap")
    print("  • Empire and Hegemony")
    print("  • Power vs. Justice (Melian Paradigm)")
    print("  • Alliance Politics")
    print("  • Escalation Dynamics")
    
    print(f"\n{'-'*60}")
    print("Processing chunks...\n")
    
    chunks, stats = remap_all_themes(chunks)
    
    print(f"\n{'='*60}")
    print("REMAPPING COMPLETE")
    print(f"{'='*60}")
    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Chunks updated: {stats['chunks_updated']}")
    print(f"Themes remapped: {stats['themes_remapped']}")
    
    if stats['unmapped_themes']:
        print(f"\n⚠ Unmapped themes ({len(stats['unmapped_themes'])}):")
        for theme in sorted(stats['unmapped_themes']):
            print(f"  • {theme}")
        print("\nThese will be removed. Add them to the mapping if needed.")
    
    # Create backup
    backup_path = chunks_path.with_suffix('.json.backup')
    print(f"\n📦 Creating backup: {backup_path}")
    save_chunks(chunks, backup_path)
    
    # Save updated chunks
    print(f"💾 Saving updated chunks: {chunks_path}")
    save_chunks(chunks, chunks_path)
    
    print("\n✅ Theme remapping complete!")
    print("\nRestart your dev server to see the new themes.")

if __name__ == "__main__":
    main()
