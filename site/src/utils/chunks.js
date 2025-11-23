import fs from 'fs';
import path from 'path';
import { isReleased } from './releaseDate.js';

let chunksCache = null;

export function loadChunks() {
  if (chunksCache) return chunksCache;
  
  // Load from data/processed/chunks.json (relative to site directory)
  const dataPath = path.join(process.cwd(), '..', 'data', 'processed', 'chunks.json');
  const rawData = fs.readFileSync(dataPath, 'utf-8');
  chunksCache = JSON.parse(rawData);
  
  return chunksCache;
}

export function getChunk(chunkIndex) {
  const chunks = loadChunks();
  return chunks.find(c => c.chunk_index === chunkIndex);
}

export function getReleasedChunks() {
  const chunks = loadChunks();
  return chunks.filter((chunk, index) => {
    const dayNumber = index + 1; // Day 1 = chunk_index 0
    return isReleased(dayNumber) && chunk.enriched && Object.keys(chunk.enriched).length > 0;
  });
}

export function getAllThemes() {
  const chunks = getReleasedChunks();
  const themes = new Set();
  
  chunks.forEach(chunk => {
    if (chunk.enriched?.key_themes) {
      chunk.enriched.key_themes.forEach(theme => themes.add(theme));
    }
  });
  
  return Array.from(themes).sort();
}

export function getChunksByTheme(theme) {
  const chunks = getReleasedChunks();
  return chunks.filter(chunk => 
    chunk.enriched?.key_themes?.includes(theme)
  );
}
