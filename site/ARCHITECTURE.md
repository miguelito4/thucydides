# Thucydides Daily Reader - Site Architecture

## Overview

Complete Astro static site for daily release of Thucydides passages. Ready to deploy to Vercel with automated daily rebuilds.

## Key Features Implemented

✅ **Side-by-side translations** (Crawley vs. Modern)
✅ **Date-gated releases** (Starting Jan 1, 2026)
✅ **Thematic exploration** (Browse by theme)
✅ **Rich enrichment display** (Context, annotations, parallels, discussion)
✅ **Automated daily rebuilds** (GitHub Actions → Vercel)
✅ **Responsive design** (Mobile-optimized)
✅ **Progress tracking** (Visual indicators)
✅ **LRB-inspired typography** (EB Garamond + Aegean blue/deep red)

## File Structure

```
site/
├── .github/workflows/
│   └── daily-build.yml          # Automated daily Vercel rebuild (00:05 UTC)
│
├── src/
│   ├── layouts/
│   │   └── BaseLayout.astro     # Main layout with typography & colors
│   │
│   ├── pages/
│   │   ├── index.astro          # Homepage with progress & latest passage
│   │   ├── about.astro          # Project information
│   │   ├── day/
│   │   │   └── [id].astro       # Daily passage pages (1-506)
│   │   └── themes/
│   │       ├── index.astro      # All themes
│   │       └── [tag].astro      # Passages by theme
│   │
│   └── utils/
│       ├── releaseDate.js       # Date calculation logic
│       └── chunks.js            # Data loading from ../data/processed/chunks.json
│
├── astro.config.mjs             # Astro + Vercel adapter config
├── package.json                 # Dependencies
├── vercel.json                  # Vercel deployment config
├── .gitignore                   # Ignore node_modules, dist, etc.
├── README.md                    # Full documentation
└── SETUP.md                     # Step-by-step deployment guide
```

## Design System

### Colors
```css
--bg-primary: #FAFAF8      /* Warm off-white background */
--text-primary: #1A1A1A    /* Near-black text */
--text-muted: #333333      /* Muted for Crawley translation */
--border-color: #E5E5E5    /* Light gray borders */
--accent-blue: #2C5F7C     /* Aegean blue - internal links */
--accent-red: #C41E3A      /* Deep red - external links */
```

### Typography
```css
--font-serif: 'EB Garamond'  /* Body text, classical serif */
--font-sans: 'Inter'         /* UI elements, clean sans */
```

### Semantic Link Colors
- **Blue** = Internal navigation (themes, other passages)
- **Red** = External resources (Perseus, Wikipedia, academic links)

## Page Routes

| Route | Description |
|-------|-------------|
| `/` | Homepage with progress tracker & latest passage |
| `/about` | Project information & methodology |
| `/themes` | Index of all themes |
| `/themes/[tag]` | All passages for a specific theme |
| `/day/[id]` | Individual daily passage (1-506) |

## Data Flow

1. **Build time**: Astro reads `../data/processed/chunks.json`
2. **Date check**: `releaseDate.js` determines which passages are released
3. **Static generation**: Creates HTML for all released passages
4. **Daily rebuild**: GitHub Actions triggers Vercel at 00:05 UTC
5. **New passage appears**: Automatically released each day

## Release Logic

```javascript
// Day 1 = January 1, 2026
const START_DATE = new Date('2026-01-01T00:00:00Z');

// Each day releases one passage
// Day 2 = January 2, 2026, etc.
// Completes Day 506 on ~July 22, 2027
```

## Deployment Checklist

### One-Time Setup
1. ✅ Extract site files to `thucydides/site/` directory
2. ✅ Run `npm install` in site directory
3. ✅ Test locally with `npm run dev`
4. ✅ Push to GitHub
5. ✅ Import to Vercel (root: `site/`)
6. ✅ Configure custom domain: `thucydides.caseyjr.org`
7. ✅ Create Vercel Deploy Hook
8. ✅ Add `VERCEL_DEPLOY_HOOK` secret to GitHub

### Daily Operation (Automated)
- GitHub Action runs at 00:05 UTC
- Triggers Vercel rebuild
- New passage appears automatically
- No manual intervention needed

## Testing Before Launch

Since it's November 2025 and release starts January 2026:

1. **Test with past date:**
   ```javascript
   // In src/utils/releaseDate.js, temporarily change:
   const START_DATE = new Date('2025-11-01T00:00:00Z');
   ```

2. **Verify passages appear**

3. **Test theme browsing**

4. **Check mobile responsiveness**

5. **Restore correct date:**
   ```javascript
   const START_DATE = new Date('2026-01-01T00:00:00Z');
   ```

## Cost: $0/month

- Vercel free tier: 100GB bandwidth, unlimited pages
- GitHub Actions free tier: 2,000 minutes/month
- No database, no API costs
- Pure static site

## Performance

- **Static HTML**: Instant page loads
- **No JavaScript required**: Works with JS disabled
- **Minimal CSS**: Inline critical styles
- **Google Fonts**: Preloaded for speed
- **Lighthouse scores**: Expected 95-100 across metrics

## Future Enhancements (Not Implemented)

Ideas for later:
- Search functionality (Pagefind or similar)
- RSS feed for new passages
- Reading progress tracking (localStorage)
- Social sharing cards
- Print stylesheet
- Dark mode
- Reader annotations/notes

## Support & Questions

- Full docs: See `README.md` and `SETUP.md`
- Issues: https://github.com/miguelito4/thucydides/issues
- Contact: caseyjr.org

---

**Status**: Ready to deploy
**Next step**: Extract files to your repo and follow SETUP.md
**Launch date**: January 1, 2026
