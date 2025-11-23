# Thucydides Daily Reader

A 507-day journey through Thucydides' *History of the Peloponnesian War*, featuring modern translation, historical context, scholarly annotations, and thematic connections.

**Live site:** [thucydides.caseyjr.org](https://thucydides.caseyjr.org)

## Features

- **Daily releases**: One passage per day starting January 1, 2026
- **Side-by-side translations**: Original Crawley (1910) alongside modern rendering
- **Rich enrichment**: Historical context, annotations, parallel ancient sources
- **Thematic exploration**: Browse passages by theme (power, rhetoric, justice, etc.)
- **Progress tracking**: Visual indicators showing journey through the History
- **Responsive design**: Beautiful reading experience on all devices

## Project Structure

```
thucydides/
├── data/
│   └── processed/
│       └── chunks.json          # Enriched passage data
├── site/                        # Astro static site (THIS DIRECTORY)
│   ├── src/
│   │   ├── pages/              # Page routes
│   │   ├── layouts/            # Layout templates
│   │   ├── utils/              # Utility functions
│   │   └── components/         # Reusable components (future)
│   ├── astro.config.mjs        # Astro configuration
│   └── package.json            # Dependencies
└── .github/
    └── workflows/
        └── daily-build.yml     # Automated daily rebuilds
```

## Local Development

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Setup

```bash
# From the site directory
cd site

# Install dependencies
npm install

# Start development server
npm run dev
```

The site will be available at `http://localhost:4321`

### Build for Production

```bash
npm run build
npm run preview  # Preview production build locally
```

## Deployment

### Vercel Setup

1. **Connect Repository**
   - Import the repository to Vercel
   - Set the root directory to `site/`
   - Framework preset: Astro
   - Build command: `npm run build`
   - Output directory: `dist/`

2. **Configure Domain**
   - Add `thucydides.caseyjr.org` as a custom domain
   - Update DNS records as instructed by Vercel

3. **Set Up Deploy Hook**
   - In Vercel dashboard → Settings → Git → Deploy Hooks
   - Create a hook named "Daily Rebuild"
   - Copy the webhook URL

4. **Add GitHub Secret**
   - In GitHub repository → Settings → Secrets and variables → Actions
   - Add secret: `VERCEL_DEPLOY_HOOK` with the webhook URL

### Automated Daily Rebuilds

The `.github/workflows/daily-build.yml` workflow triggers a Vercel rebuild daily at 00:05 UTC, automatically releasing the next passage.

To manually trigger a rebuild:
- Go to Actions tab in GitHub
- Select "Daily Site Rebuild" workflow
- Click "Run workflow"

## How It Works

### Release Schedule

- **Start date**: January 1, 2026
- **Daily release**: One passage per day at midnight UTC
- **Duration**: 507 days (completes ~July 2027)

### Date-Gating Logic

The `src/utils/releaseDate.js` utility calculates which passages should be visible:

```javascript
// Day 1 releases January 1, 2026
// Day 2 releases January 2, 2026, etc.
const START_DATE = new Date('2026-01-01T00:00:00Z');
```

Pages check release status at build time. Unreleased passages redirect to homepage.

### Data Structure

The site reads from `../data/processed/chunks.json`, which contains:

```json
[
  {
    "chunk_index": 0,
    "book": 1,
    "chapter": 1,
    "original_text": "...",
    "enriched": {
      "modern_translation": "...",
      "context": "...",
      "key_themes": ["power", "methodology"],
      "annotations": [...],
      "parallel_accounts": [...],
      "discussion_prompts": [...]
    }
  }
]
```

## Design System

### Typography

- **Primary font**: EB Garamond (classical serif)
- **UI font**: Inter (clean sans-serif)
- **Body size**: 18px
- **Line height**: 1.7

### Colors

- **Background**: `#FAFAF8` (warm off-white)
- **Text**: `#1A1A1A` (near-black)
- **Muted text**: `#333333` (for Crawley translation)
- **Primary accent**: `#2C5F7C` (Aegean blue) - internal links, navigation
- **Secondary accent**: `#C41E3A` (deep red) - external links, scholarly resources
- **Borders**: `#E5E5E5` (light gray)

### Semantic Color Usage

- **Blue links**: Internal navigation (themes, other passages)
- **Red links**: External resources (Perseus, scholarly articles)

## Contributing

This is an open-source project under the MIT license. Contributions welcome!

Areas for improvement:
- Search functionality
- Mobile optimizations
- Additional scholarly annotations
- Interactive timeline visualization
- Discussion/annotation features

## License

MIT License - see [LICENSE](../LICENSE) for details

Original Thucydides text (Crawley translation) is in the public domain.

## Credits

- **Created by**: [Mike Casey](https://caseyjr.org)
- **AI Enrichment**: Claude by Anthropic
- **Original Translation**: Richard Crawley (1910)
- **Built with**: [Astro](https://astro.build), deployed on [Vercel](https://vercel.com)

## Learn More

- [About the project](https://thucydides.caseyjr.org/about)
- [Thucydides on Wikipedia](https://en.wikipedia.org/wiki/History_of_the_Peloponnesian_War)
- [Perseus Digital Library](https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0200)
