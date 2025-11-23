#!/usr/bin/env python3
"""
Strict remapping to EXACTLY 11 Waltz themes.
Removes all themes that don't fit the framework.
"""

import json
from pathlib import Path

# STRICT Waltz Framework - Only these 11 themes
WALTZ_MAPPING = {
    # Level I: The Individual (Physis)
    "Fear, Honor, and Interest": [
        "fear", "honor", "interest", "self-interest", "prestige", 
        "reputation", "glory", "ambition", "greed", "pride",
        "human motivation", "psychological", "individual motivation"
    ],
    
    "Hope vs. Reality": [
        "hope", "reality", "rhetoric", "persuasion", "speech", 
        "appearance", "deception", "propaganda", "words versus deeds",
        "expectation", "illusion", "logos", "ergon", "elpis"
    ],
    
    "The Corrosion of Morality": [
        "morality", "ethics", "corruption", "brutality", "violence",
        "plague", "civil war", "stasis", "breakdown", "decay",
        "cruelty", "atrocity", "dehumanization", "moral"
    ],
    
    # Level II: The State (Polis)
    "Democracy vs. Oligarchy": [
        "democracy", "oligarchy", "athenian democracy", "spartan",
        "political system", "constitution", "governance", "assembly",
        "leadership", "demagogue", "faction", "decision-making"
    ],
    
    "Sea Power vs. Land Power": [
        "naval", "sea", "maritime", "fleet", "navy", "ship",
        "land power", "hoplite", "army", "geography", "strategic",
        "terrain", "economic", "resources", "wealth", "trade",
        "material", "infrastructure"
    ],
    
    "Civil Strife (Stasis)": [
        "stasis", "civil war", "revolution", "internal conflict",
        "domestic", "class", "polarization", "party", "partisan",
        "corcyra", "factional", "sedition"
    ],
    
    # Level III: The System (Kinesis)
    "The Thucydides Trap": [
        "balance of power", "power transition", "rising power",
        "security dilemma", "preventive", "structural", "systemic",
        "inevitable", "truest cause"
    ],
    
    "Empire and Hegemony": [
        "empire", "imperial", "imperialism", "hegemony", "hegemon",
        "athenian empire", "expansion", "colonial", "subject",
        "tribute", "domination", "control"
    ],
    
    "Power vs. Justice (Melian Paradigm)": [
        "melian", "might", "strong", "weak", "realpolitik",
        "necessity", "compulsion", "power and justice", "justice",
        "right", "fair", "equality", "exploitation"
    ],
    
    "Alliance Politics": [
        "alliance", "coalition", "ally", "allies", "neutral",
        "treaty", "pact", "entrapment", "abandonment", "commitment",
        "corinth", "corcyra", "diplomatic"
    ],
    
    "Escalation Dynamics": [
        "escalation", "spiral", "chain reaction", "domino",
        "unintended", "consequence", "conflict", "war causation",
        "local", "systemic", "contagion", "spread"
    ]
}

def normalize(text):
    """Normalize text for matching."""
    return text.lower().strip()

def map_to_waltz(theme_text):
    """Map a theme to one of the 11 Waltz categories."""
    norm = normalize(theme_text)
    
    for waltz_theme, keywords in WALTZ_MAPPING.items():
        for keyword in keywords:
            if keyword in norm or norm in keyword:
                return waltz_theme
    
    return None

def remap_chunks_strict(chunks):
    """Strictly remap all chunks to 11 Waltz themes only."""
    stats = {
        'chunks_processed': 0,
        'chunks_with_themes': 0,
        'themes_kept': 0,
        'themes_removed': 0,
        'removed_themes': set()
    }
    
    for chunk in chunks:
        if not chunk.get('enriched') or not chunk['enriched'].get('key_themes'):
            continue
        
        stats['chunks_processed'] += 1
        old_themes = chunk['enriched']['key_themes']
        new_themes = set()
        
        for old_theme in old_themes:
            waltz_theme = map_to_waltz(old_theme)
            if waltz_theme:
                new_themes.add(waltz_theme)
                stats['themes_kept'] += 1
            else:
                stats['themes_removed'] += 1
                stats['removed_themes'].add(old_theme)
        
        chunk['enriched']['key_themes'] = sorted(list(new_themes))
        
        if new_themes:
            stats['chunks_with_themes'] += 1
    
    return chunks, stats

def main():
    chunks_path = Path('data/processed/chunks.json')
    
    print("\n" + "="*60)
    print("STRICT WALTZ FRAMEWORK REMAPPING")
    print("="*60 + "\n")
    
    print("Loading chunks...")
    with open(chunks_path) as f:
        chunks = json.load(f)
    
    print(f"Processing {len(chunks)} chunks...\n")
    
    chunks, stats = remap_chunks_strict(chunks)
    
    print("="*60)
    print("RESULTS")
    print("="*60)
    print(f"Chunks processed: {stats['chunks_processed']}")
    print(f"Chunks with themes: {stats['chunks_with_themes']}")
    print(f"Themes kept: {stats['themes_kept']}")
    print(f"Themes removed: {stats['themes_removed']}")
    
    if stats['removed_themes']:
        print(f"\nRemoved themes ({len(stats['removed_themes'])}):")
        for theme in sorted(stats['removed_themes']):
            print(f"  • {theme}")
    
    # Backup
    backup_path = chunks_path.with_suffix('.json.backup2')
    print(f"\n📦 Creating backup: {backup_path}")
    with open(backup_path, 'w') as f:
        json.dump(chunks, f, indent=2)
    
    # Save
    print(f"💾 Saving updated chunks: {chunks_path}")
    with open(chunks_path, 'w') as f:
        json.dump(chunks, f, indent=2)
    
    print("\n✅ Strict remapping complete!")
    print("\nYou now have EXACTLY 11 theme categories.")
    print("Restart dev server to see the clean structure.")

if __name__ == "__main__":
    main()
