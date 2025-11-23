import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { getReleaseDate } from '../utils/releaseDate.js';

import chunksData from '../../../data/processed/chunks.json';

export async function GET(context: APIContext) {
  
  const releasedChunks = chunksData
    .filter((c: any) => c.enriched?.modern_translation)
    .slice(-20)
    .reverse();

  return rss({
    stylesheet: '/rss-styles.xsl',
    
    title: 'Thucydides Daily Reader',
    description: "A daily journey through Thucydides' History of the Peloponnesian War",
    site: context.site?.toString() || 'https://thucydides.caseyjr.org',
    items: releasedChunks.map((chunk: any) => {
      const dayNumber = chunk.chunk_index + 1;
      const content = 
        (chunk.enriched.context?.substring(0, 200) || '') + '... ' +
        (chunk.enriched.modern_translation?.substring(0, 300) || '') + '...';

      return {
        title: `Day ${dayNumber}: Book ${chunk.book}, Chapter ${chunk.chapter}`,
        pubDate: getReleaseDate(dayNumber),
        description: content,
        link: `/day/${dayNumber}/`,
      };
    }),
  });
}