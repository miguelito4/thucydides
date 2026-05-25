import type { APIContext } from 'astro';
import { isReleased } from '../utils/releaseDate.js';

import chunksData from '../../../data/processed/chunks.json';

// Build artifact consumed by the main site (https://thucydides.caseyjr.org/passages.json).
// Emitted on every build so it refreshes as new days are released.
//
// Day indexing mirrors src/pages/day/[id].astro exactly: a day's page is live
// only when the chunk has enrichment AND has been released, and the day number
// is chunk_index + 1. We do NOT recompute the day -> book/chapter mapping here;
// we reuse the reader's own data and indexing.
export async function GET(_context: APIContext) {
  const passages = (chunksData as any[])
    .filter((c) => c.enriched && Object.keys(c.enriched).length > 0)
    .map((c) => ({ ...c, dayNumber: c.chunk_index + 1 }))
    .filter((c) => isReleased(c.dayNumber))
    .sort((a, b) => a.dayNumber - b.dayNumber)
    .map((c) => ({
      day: c.dayNumber,
      book: c.book,
      chapter: c.chapter,
      // Reading text only (Crawley translation, public domain) — no annotations.
      passage: c.original_text,
    }));

  return new Response(JSON.stringify(passages), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
    },
  });
}
