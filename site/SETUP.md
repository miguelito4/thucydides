# Setting Up the Thucydides Daily Reader Site

## Quick Start

This guide walks you through adding the Astro site to your existing `thucydides` repository and deploying to Vercel.

## Step 1: Add Site Files to Your Repository

```bash
# Navigate to your thucydides repository
cd ~/path/to/thucydides

# Create the site directory
mkdir -p site

# Copy all site files from this temporary directory to site/
# (You'll receive these files as a download)
```

Your repository structure should now look like:

```
thucydides/
├── data/
│   └── processed/
│       └── chunks.json
├── site/                        # NEW
│   ├── .github/
│   │   └── workflows/
│   │       └── daily-build.yml
│   ├── src/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── utils/
│   │   └── ...
│   ├── astro.config.mjs
│   ├── package.json
│   └── README.md
├── src/                         # Your existing Python scripts
├── config.yaml
└── ...
```

## Step 2: Test Locally

```bash
cd site
npm install
npm run dev
```

Open `http://localhost:4321` to preview the site.

**Note**: The site expects enriched data at `../data/processed/chunks.json`. If your data is elsewhere, update the path in `src/utils/chunks.js`.

## Step 3: Deploy to Vercel

### 3.1 Create Vercel Account
- Go to [vercel.com](https://vercel.com)
- Sign up with your GitHub account

### 3.2 Import Project
1. Click "Add New..." → "Project"
2. Select your `thucydides` repository
3. Configure project:
   - **Framework Preset**: Astro
   - **Root Directory**: `site` (click "Edit" and specify this)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Click "Deploy"

### 3.3 Configure Custom Domain
1. In Vercel dashboard → Settings → Domains
2. Add domain: `thucydides.caseyjr.org`
3. Vercel will provide DNS instructions

### 3.4 Update DNS at caseyjr.org
Add the DNS records Vercel specifies. Typically:
```
Type: CNAME
Name: thucydides
Value: cname.vercel-dns.com
```

DNS propagation takes 5-60 minutes.

## Step 4: Set Up Automated Daily Builds

### 4.1 Create Vercel Deploy Hook
1. Vercel dashboard → Settings → Git → Deploy Hooks
2. Create hook:
   - **Name**: Daily Rebuild
   - **Branch**: main (or your default branch)
3. Copy the webhook URL

### 4.2 Add GitHub Secret
1. GitHub repository → Settings → Secrets and variables → Actions → New repository secret
2. Name: `VERCEL_DEPLOY_HOOK`
3. Value: Paste the webhook URL from step 4.1
4. Click "Add secret"

### 4.3 Enable GitHub Actions
The workflow file is already in `.github/workflows/daily-build.yml`. GitHub Actions should automatically detect it.

To verify:
1. Go to Actions tab in your GitHub repository
2. You should see "Daily Site Rebuild" workflow
3. It will run automatically at 00:05 UTC daily
4. You can also trigger it manually: Actions → Daily Site Rebuild → Run workflow

## Step 5: Verify Everything Works

### Check Build
- Vercel should show successful deployment
- Visit `https://thucydides.caseyjr.org`

### Check Daily Automation
- Manually trigger the GitHub Action to test
- Verify it triggers a Vercel rebuild
- Check Vercel deployments to confirm

### Test Date Logic
Currently (November 2025), no passages should be released yet. 

To test with released passages:
1. Temporarily edit `src/utils/releaseDate.js`
2. Change START_DATE to a past date (e.g., yesterday)
3. Redeploy
4. Verify passages appear
5. Change START_DATE back to `'2026-01-01T00:00:00Z'`

## Step 6: Launch Day Checklist (January 1, 2026)

- [ ] Verify enrichment is 100% complete (all 506 chunks)
- [ ] Test site builds successfully with complete data
- [ ] Confirm first passage appears at midnight UTC
- [ ] Check automated rebuild runs successfully
- [ ] Share link with readers!

## Troubleshooting

### "Cannot find module '../data/processed/chunks.json'"
- Verify your data file location
- Update path in `src/utils/chunks.js` if needed
- Ensure chunks.json is committed to git

### Pages showing "Coming soon" when they shouldn't
- Check `src/utils/releaseDate.js` START_DATE
- Verify your local time vs UTC
- Try `npm run build` again

### Daily rebuild not triggering
- Verify GitHub secret `VERCEL_DEPLOY_HOOK` is set correctly
- Check GitHub Actions permissions (Settings → Actions → General)
- Test deploy hook manually with: `curl -X POST "your-webhook-url"`

### Site not updating with new passages
- Confirm GitHub Action ran successfully
- Check Vercel deployments show new build
- Clear browser cache and hard refresh

## Cost

### Vercel Free Tier Includes:
- Unlimited static page deployments
- 100GB bandwidth/month
- Automatic SSL
- Preview deployments
- More than sufficient for this project

### GitHub Actions Free Tier:
- 2,000 minutes/month
- Daily rebuild takes <1 minute
- Well within free limits

**Total monthly cost: $0**

## Next Steps

After launch, consider:
- Adding search functionality
- Creating an RSS feed
- Building a mobile app
- Adding reader annotations/discussions
- Translating to other languages

## Support

Questions? Open an issue at [github.com/miguelito4/thucydides](https://github.com/miguelito4/thucydides)
