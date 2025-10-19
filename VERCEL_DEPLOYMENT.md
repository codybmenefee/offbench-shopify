# Vercel Deployment Guide

This guide will help you deploy the Discovery Agent MCP server to Vercel for a stable, production-ready connection to ChatGPT.

## Prerequisites

1. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI** (optional but recommended):
   ```bash
   npm install -g vercel
   ```

## Deployment Steps

### Option 1: Deploy via Vercel CLI (Recommended)

1. **Login to Vercel**:
   ```bash
   vercel login
   ```

2. **Deploy from the project root**:
   ```bash
   cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
   vercel
   ```

3. **Follow the prompts**:
   - Set up and deploy? **Y**
   - Which scope? Choose your account
   - Link to existing project? **N** (first time)
   - What's your project's name? **discovery-agent-mcp**
   - In which directory is your code located? **./
**
   - Want to override settings? **N**

4. **Deploy to production**:
   ```bash
   vercel --prod
   ```

### Option 2: Deploy via Vercel Dashboard

1. **Go to** [vercel.com/new](https://vercel.com/new)

2. **Import Git Repository**:
   - Connect your GitHub/GitLab/Bitbucket account
   - Select this repository
   - Or use "Import Third-Party Git Repository" and paste the repo URL

3. **Configure Project**:
   - **Project Name**: `discovery-agent-mcp`
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: Leave empty (serverless functions don't need build)
   - **Output Directory**: Leave empty

4. **Environment Variables** (if needed):
   - None required for this project

5. **Click "Deploy"**

## After Deployment

### Get Your Production URL

After deployment completes, Vercel will provide a URL like:
```
https://discovery-agent-mcp-xxxxx.vercel.app
```

### Configure ChatGPT

1. **Open ChatGPT** → **Settings** → **Apps**

2. **Add MCP Server**:
   - **Name**: Discovery Agent
   - **URL**: `https://your-deployment-url.vercel.app/mcp`
   - **Protocol**: MCP/Streamable HTTP

3. **Test the connection**:
   ```
   What projects are available?
   ```

## Vercel Configuration Details

### Files Created

- **`vercel.json`** - Vercel configuration
- **`api/index.py`** - Serverless function entry point
- **`requirements.txt`** - Python dependencies
- **`.vercelignore`** - Files to exclude from deployment

### How It Works

1. Vercel runs `api/index.py` as a serverless function
2. The function imports the FastMCP app from `mcp/src/main.py`
3. All MCP requests are routed to `/mcp` endpoint
4. Test data and templates are bundled with the deployment

### Deployment Size

- **Total deployment**: ~2-5 MB (code + templates + test data)
- **Cold start time**: ~2-3 seconds (first request)
- **Warm requests**: <100ms

## Testing Your Deployment

### Test Endpoints

1. **Health Check**:
   ```bash
   curl https://your-deployment-url.vercel.app/
   ```

2. **List Tools** (via MCP):
   Use ChatGPT or MCP Inspector

### View Logs

```bash
vercel logs your-deployment-url.vercel.app
```

Or view in the Vercel Dashboard → Your Project → Logs

## Updating Your Deployment

### Via CLI

```bash
cd /path/to/project
vercel --prod
```

### Via Git

If you connected a Git repository:
1. Push changes to your main branch
2. Vercel auto-deploys on push

## Security Considerations

### ✅ Advantages Over Ngrok

1. **Stable URL**: No random subdomains, permanent URL
2. **HTTPS by default**: Automatic SSL certificates
3. **No tunneling**: Direct HTTPS connection
4. **DDoS protection**: Vercel's edge network
5. **Authentication**: Can add Vercel auth if needed

### 🔒 Additional Security (Optional)

Add authentication by updating `api/index.py`:

```python
from fastapi import Header, HTTPException

async def verify_token(authorization: str = Header(None)):
    if authorization != "Bearer YOUR_SECRET_TOKEN":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

# Then add dependency to routes
```

## Troubleshooting

### Deployment Fails

1. **Check logs**:
   ```bash
   vercel logs
   ```

2. **Common issues**:
   - Python version mismatch → Update `vercel.json`
   - Missing dependencies → Update `requirements.txt`
   - File paths wrong → Check `BASE_PATH` in `api/index.py`

### 500 Internal Server Error

1. **Check Vercel logs** for Python errors
2. **Test locally** first:
   ```bash
   cd mcp
   python src/main.py
   ```

### Cold Starts Slow

This is normal for serverless. Options:
- Use Vercel Pro (keeps functions warm)
- Implement connection pooling
- Add caching layer

## Cost

**Free Tier Includes**:
- 100 GB bandwidth/month
- 100,000 function invocations/month
- Automatic SSL
- DDoS protection

**Estimated Usage** (for MCP server):
- ~10-50 requests per ChatGPT conversation
- ~1-5 KB per request
- Well within free tier limits

## Monitoring

### Vercel Analytics

Enable in dashboard:
1. Go to your project
2. Click "Analytics" tab
3. Enable Web Analytics

### Custom Monitoring

Add logging in `api/index.py`:
```python
import time

@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"[METRICS] {request.method} {request.url.path} - {duration:.2f}s", file=sys.stderr)
    return response
```

## Next Steps

1. ✅ Deploy to Vercel
2. ✅ Configure ChatGPT with production URL
3. ✅ Test all 8 MCP tools
4. 📊 Monitor usage and performance
5. 🔒 Consider adding authentication for production use

## Support

- **Vercel Docs**: https://vercel.com/docs
- **FastMCP Docs**: https://gofastmcp.com
- **MCP Protocol**: https://modelcontextprotocol.io

---

**Ready to deploy?** Run:
```bash
vercel --prod
```

