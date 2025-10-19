# 🚂 Railway Deployment Guide

Your Discovery Agent MCP server is configured and ready to deploy to Railway!

## What is Railway?

Railway is a modern deployment platform that provides:
- ✅ **Permanent URLs** - Your URL never changes
- ✅ **Automatic HTTPS** - SSL certificates included
- ✅ **Global CDN** - Fast performance worldwide
- ✅ **99.9% Uptime** - Production-ready reliability
- ✅ **Generous Free Tier** - $5 of free usage monthly
- ✅ **GitHub Integration** - Auto-deploy on push

## Prerequisites

- A Railway account (sign up at [railway.app](https://railway.app))
- Git repository (optional, for auto-deploy)

## 🚀 Quick Deploy

### Method 1: Deploy from GitHub (Recommended)

This method enables automatic deployments whenever you push code.

1. **Push your code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Create a new project on Railway**:
   - Go to [railway.app/new](https://railway.app/new)
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Python and deploy

3. **Configure environment variables** (if needed):
   - In Railway dashboard, go to your service
   - Click "Variables" tab
   - Add any required environment variables
   - Railway automatically provides `PORT`

4. **Get your deployment URL**:
   - Click on your service in Railway dashboard
   - Go to "Settings" → "Networking"
   - Click "Generate Domain"
   - Your URL will be: `https://your-app.up.railway.app`

### Method 2: Deploy from Local Directory

If you don't want to use GitHub, deploy directly from your terminal.

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   # or
   brew install railway
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize and deploy**:
   ```bash
   cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
   railway init
   railway up
   ```

4. **Generate a domain**:
   ```bash
   railway domain
   ```

## 📋 Configuration Files

The following files are configured for Railway:

### 1. `Procfile`
Tells Railway what command to run:
```
web: cd mcp && python src/main.py
```

### 2. `railway.json`
Railway-specific configuration:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "sleepApplication": false,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 3. `runtime.txt`
Specifies Python version:
```
python-3.11.9
```

### 4. `requirements.txt`
Python dependencies that Railway will install automatically.

### 5. `.railwayignore`
Files and directories excluded from deployment (similar to `.gitignore`).

## 🔧 How It Works

1. **Automatic Detection**: Railway detects Python and reads `runtime.txt`
2. **Install Dependencies**: Runs `pip install -r requirements.txt`
3. **Start Server**: Executes the command in `Procfile`
4. **Port Binding**: Railway provides `PORT` environment variable (auto-detected by your app)
5. **HTTPS**: Railway automatically provisions SSL certificates

## 📊 What Gets Deployed

- ✅ MCP Server (`mcp/src/main.py`)
- ✅ All 8 MCP tools
- ✅ 5 test scenarios (`test-data/`)
- ✅ All templates (`templates/`)
- ✅ Core analysis engine
- ✅ State management

**Excluded** (via `.railwayignore`):
- ❌ Virtual environments (`venv/`)
- ❌ Python cache (`__pycache__/`)
- ❌ Development configs
- ❌ Vercel-specific files

## 🧪 Testing Your Deployment

### 1. Health Check
Visit your deployment URL in a browser:
```
https://your-app.up.railway.app
```

You should see the MCP server running (it will respond with JSON or MCP protocol info).

### 2. Test with ChatGPT

Configure ChatGPT to use your Railway URL:

1. Open ChatGPT
2. Configure custom MCP server
3. URL: `https://your-app.up.railway.app`
4. Protocol: MCP/HTTP

Then test with:
```
What projects are available?
```

### 3. Test with HTTP Client

Using `curl`:
```bash
curl https://your-app.up.railway.app
```

## 🎯 Post-Deployment

### Monitor Your Application

1. **View Logs**:
   - Railway Dashboard → Your Service → "Deployments" tab
   - Or via CLI: `railway logs`

2. **Monitor Resources**:
   - Dashboard shows CPU, memory, and network usage
   - Free tier includes $5/month of resources

3. **Check Build Status**:
   - Dashboard shows build and deployment status
   - Successful builds are marked with ✓

### Custom Domain (Optional)

Add your own domain name:

1. In Railway dashboard, go to your service
2. Click "Settings" → "Networking"
3. Click "Custom Domain"
4. Add your domain (e.g., `api.yourdomain.com`)
5. Update your DNS with the provided CNAME record

## 🔒 Security Best Practices

### Environment Variables

Store sensitive data as environment variables:

```bash
# Via CLI
railway variables set API_KEY=your-secret-key

# Or via Dashboard
Settings → Variables → Add Variable
```

Access in your code:
```python
import os
api_key = os.getenv("API_KEY")
```

### Rate Limiting

Consider adding rate limiting for production:
```python
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

## 📈 Scaling

### Horizontal Scaling
Add more replicas in `railway.json`:
```json
{
  "deploy": {
    "numReplicas": 2
  }
}
```

### Vertical Scaling
Upgrade to a paid plan for more resources:
- More CPU and RAM
- Higher bandwidth
- Longer deployment builds

## 🐛 Troubleshooting

### Build Fails

**Issue**: "Could not find Python version"
- **Solution**: Verify `runtime.txt` has a valid Python version (e.g., `python-3.11.9`)

**Issue**: "Module not found"
- **Solution**: Ensure all dependencies are in `requirements.txt`

### Application Crashes

**Issue**: "Port already in use"
- **Solution**: Check that your app uses `os.getenv("PORT", 8123)` to read the port

**Issue**: "Module import errors"
- **Solution**: Check your `Procfile` path and ensure `cd mcp` is correct

### Logs

View detailed logs:
```bash
# Via CLI
railway logs

# Or in Dashboard
Your Service → Deployments → Click on deployment → View logs
```

## 💰 Pricing

### Free Tier
- $5 of usage per month
- Includes:
  - 512 MB RAM
  - Shared CPU
  - Community support
  - All core features

### Hobby Plan ($5/month)
- $5 credit + pay for what you use
- Includes:
  - 8 GB RAM per service
  - Shared CPU
  - Email support

### Pro Plan ($20/month)
- $20 credit + pay for what you use
- Priority support
- Custom infrastructure

For this MCP server, the **free tier is sufficient** for development and light production use.

## 🔄 Continuous Deployment

### Automatic Deployment

If you deployed from GitHub, Railway automatically:
1. Watches for commits to your default branch
2. Builds and deploys on every push
3. Rolls back if deployment fails

### Manual Deployment

Force a redeploy:
```bash
# Via CLI
railway up

# Or via Dashboard
Deployments → Click "Deploy" on latest build
```

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Railway CLI Reference](https://docs.railway.app/develop/cli)
- [Railway Community](https://discord.gg/railway)
- [Python Deployment Guide](https://docs.railway.app/guides/python)

## 🎉 Success Checklist

- ✅ Code pushed to repository (if using GitHub method)
- ✅ Railway project created
- ✅ Domain generated
- ✅ Application is running
- ✅ Health check passes
- ✅ Tested with ChatGPT or HTTP client
- ✅ Logs show successful requests
- ✅ No errors in Railway dashboard

## 🚀 Next Steps

1. **Configure ChatGPT**: Use your Railway URL in ChatGPT Actions
2. **Test All Tools**: Run through test scenarios to verify functionality
3. **Set Up Monitoring**: Enable Railway metrics and alerts
4. **Add Custom Domain** (optional): Point your domain to Railway
5. **Enable Auto-Deploy**: Connect GitHub for automatic deployments
6. **Share with Team**: Distribute your permanent Railway URL

---

**Your Railway URL**: `https://your-app.up.railway.app`

**Need Help?**
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Documentation: [docs.railway.app](https://docs.railway.app/)

Happy deploying! 🚂✨

