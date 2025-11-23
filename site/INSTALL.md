# Installing the Thucydides Daily Reader Site

## What You Have

A complete, production-ready Astro static site that will:
- Display Thucydides passages side-by-side (Crawley vs. Modern)
- Release one passage per day starting January 1, 2026
- Automatically rebuild daily via GitHub Actions
- Deploy to `thucydides.caseyjr.org` on Vercel
- Cost $0/month to run

## Quick Install (5 minutes)

### 1. Extract Files
```bash
cd ~/path/to/thucydides  # Your existing repo
tar -xzf /path/to/thucydides-site-complete.tar.gz
mv thucydides-site site
```

Your repo now has:
```
thucydides/
├── data/processed/chunks.json  # Your enriched data
├── site/                        # NEW: The website
├── src/                         # Your Python scripts
└── ...
```

### 2. Test Locally
```bash
cd site
npm install
npm run dev
```

Visit `http://localhost:4321` - you should see the homepage!

**Note**: Since it's November 2025, no passages will show yet (release starts Jan 1, 2026). To test with visible content, temporarily change the date in `src/utils/releaseDate.js`:

```javascript
// Change this line temporarily:
const START_DATE = new Date('2025-11-01T00:00:00Z');
```

Then restart dev server. Remember to change it back before deploying!

### 3. Commit & Push
```bash
git add site/
git commit -m "Add Astro daily reader site"
git push
```

### 4. Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click "Add New..." → "Project"
3. Select your `thucydides` repository
4. Click "Edit" next to Root Directory and enter: `site`
5. Framework Preset should auto-detect as "Astro" ✅
6. Click "Deploy"

Wait 2-3 minutes for first deployment.

### 5. Configure Domain

In Vercel dashboard:
1. Go to Settings → Domains
2. Add: `thucydides.caseyjr.org`
3. Follow DNS instructions (add CNAME record)

### 6. Set Up Daily Auto-Rebuild

**In Vercel:**
1. Settings → Git → Deploy Hooks
2. Create hook: "Daily Rebuild" on your main branch
3. Copy the webhook URL

**In GitHub:**
1. Your repo → Settings → Secrets and variables → Actions
2. New repository secret
3. Name: `VERCEL_DEPLOY_HOOK`
4. Value: Paste webhook URL
5. Add secret

**Test it works:**
1. GitHub → Actions tab
2. Select "Daily Site Rebuild"
3. Click "Run workflow"
4. Verify it triggers a Vercel deployment

Done! 🎉

## What Happens Next

### Now (November 2025)
- Site is live but shows "Coming soon" for all passages
- Daily rebuild runs but nothing changes yet

### January 1, 2026
- Day 1 passage automatically appears
- Readers can start following along

### Every Day After
- At 00:05 UTC, GitHub Action triggers Vercel rebuild
- Next passage becomes available
- Completely automated, no manual work needed

### July 2027
- Day 506 (final passage) published
- Complete History available for browsing
- Archive remains online indefinitely

## Troubleshooting

**"Can't find chunks.json"**
- The site expects data at `../data/processed/chunks.json`
- From `site/`, that's `../data/processed/chunks.json`
- If your data is elsewhere, edit `src/utils/chunks.js`

**"Nothing showing on the site"**
- Check the date in `src/utils/releaseDate.js`
- Before Jan 1, 2026, no passages are released
- For testing, temporarily set `START_DATE` to a past date

**"Daily rebuild not working"**
- Verify GitHub secret `VERCEL_DEPLOY_HOOK` is set correctly  
- Check Actions tab for errors
- Test deploy hook with: `curl -X POST "your-webhook-url"`

## Files Included

```
site/
├── .github/workflows/
│   └── daily-build.yml          # GitHub Actions workflow
├── src/
│   ├── layouts/
│   │   └── BaseLayout.astro     # Main layout
│   ├── pages/
│   │   ├── index.astro          # Homepage
│   │   ├── about.astro          # About page
│   │   ├── day/[id].astro       # Daily passages
│   │   └── themes/              # Theme browsing
│   └── utils/
│       ├── releaseDate.js       # Date logic
│       └── chunks.js            # Data loading
├── astro.config.mjs             # Astro config
├── package.json                 # Dependencies
├── vercel.json                  # Vercel config
├── ARCHITECTURE.md              # Technical overview
├── README.md                    # Full documentation
└── SETUP.md                     # Detailed deployment guide
```

## Support

- Full docs: `README.md` and `SETUP.md` inside the site folder
- Architecture: `ARCHITECTURE.md` for technical details
- Issues: Open at https://github.com/miguelito4/thucydides

## Cost

**$0/month forever**
- Vercel free tier: More than enough for this site
- GitHub Actions: Well within free limits
- No database, no API costs

---

**You're ready to deploy!** Follow the 6 steps above and your site will be live.
