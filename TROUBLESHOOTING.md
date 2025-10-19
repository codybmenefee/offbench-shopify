# 🔧 Railway Deployment Troubleshooting

## Current Issue: 502 Application Failed to Respond

The deployment was successful, but the application isn't starting. Let's diagnose and fix it.

---

## 🔍 Step 1: Check Railway Logs

**Via Railway Dashboard:**
1. Go to your Railway project
2. Click on your service
3. Click "Deployments" tab
4. Click on the latest deployment
5. View the logs

**Via CLI:**
```bash
railway logs
```

---

## 🐛 Common Issues & Solutions

### Issue 1: Port Binding Error

**Symptom**: Logs show "Address already in use" or "Port not available"

**Solution**: Verify the code reads PORT correctly
```python
# In mcp/src/main.py (should already be there)
port = int(os.getenv("PORT", 8123))
```

### Issue 2: Module Import Errors

**Symptom**: Logs show "ModuleNotFoundError" or "ImportError"

**Common causes**:
- Missing dependencies in `requirements.txt`
- Path issues with imports

**Solution**: Check if all imports are working
```bash
# Test locally first
cd mcp
python -c "from src.main import mcp"
```

### Issue 3: Path/Directory Issues

**Symptom**: Logs show "FileNotFoundError" or "No such file or directory"

**Solution**: Verify the Procfile path is correct

Current `Procfile`:
```
web: cd mcp && python src/main.py
```

Alternative if that doesn't work:
```
web: python mcp/src/main.py
```

### Issue 4: Python Version Mismatch

**Symptom**: Logs show "SyntaxError" or version-related errors

**Solution**: Check `runtime.txt` matches your code
```
python-3.11.9
```

If your code needs 3.14, update to:
```
python-3.14.0
```

### Issue 5: Missing Environment Variables

**Symptom**: App starts but crashes immediately

**Solution**: Check if app needs any env vars
```bash
# Set via CLI
railway variables set KEY=value

# Or via Dashboard
Settings → Variables → Add Variable
```

### Issue 6: Uvicorn Not Starting

**Symptom**: No "Uvicorn running" message in logs

**Solution**: Test the FastMCP HTTP server locally
```bash
cd mcp
python src/main.py
# Should show: "Uvicorn running on http://0.0.0.0:8123"
```

---

## 🎯 Quick Diagnostic Checklist

Run through these checks in order:

### 1. Check Build Logs
```bash
railway logs --build
```
- ✅ Should show successful dependency installation
- ✅ Should complete without errors

### 2. Check Runtime Logs
```bash
railway logs
```
Look for:
- ❌ Error messages (ModuleNotFoundError, etc.)
- ❌ Traceback/stack traces
- ❌ Port binding errors
- ✅ "Uvicorn running on..." message (this is what we want!)

### 3. Test Locally
```bash
cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
cd mcp
python src/main.py
```
- Should start without errors
- Should show Uvicorn running

### 4. Check File Structure
```bash
ls -la mcp/src/
```
Should show:
- main.py
- core/ directory
- models/ directory
- __init__.py files

---

## 🔧 Likely Fix: Update Procfile

The most common issue is the working directory. Try this alternative:

**Option A** (current):
```
web: cd mcp && python src/main.py
```

**Option B** (try if A fails):
```
web: python mcp/src/main.py
```

**Option C** (if imports fail):
```
web: cd mcp && python -m src.main
```

To update:
1. Edit `Procfile`
2. Commit and push
3. Railway will auto-redeploy

---

## 🧪 Test Local First

Before redeploying, verify locally:

```bash
# Test 1: Can we import?
cd mcp
python -c "from src.main import mcp; print('✅ Import works')"

# Test 2: Can we run?
python src/main.py
# Wait 2 seconds, then Ctrl+C
# Should see: "Uvicorn running on..."

# Test 3: Can we make requests?
# (In another terminal while server is running)
curl http://localhost:8123
```

---

## 📊 Expected Log Output

When working correctly, Railway logs should show:

```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:$PORT (Press CTRL+C to quit)
```

---

## 🔍 Debugging Steps

### Step 1: Get the actual error
```bash
railway logs --tail 100
```

### Step 2: Identify the issue
Look for:
- Module import errors → Missing dependency or path issue
- Port errors → PORT env var not being read
- File not found → Procfile path issue
- Syntax errors → Python version mismatch

### Step 3: Fix and redeploy
```bash
# Make your fix
git add .
git commit -m "Fix: [describe the fix]"
git push

# Railway auto-deploys
# Or manually: railway up
```

### Step 4: Verify
```bash
# Wait 30-60 seconds for deployment
curl https://offbench-shopify-production.up.railway.app
```

---

## 🚨 Nuclear Option: Fresh Deploy

If nothing works, try a clean slate:

```bash
# 1. Remove Railway project
railway unlink

# 2. Delete and recreate
railway init
railway up

# 3. Generate new domain
railway domain
```

---

## 📞 Get Help

**Share your logs here:**
```bash
railway logs --tail 50 > railway-logs.txt
```

Then we can diagnose the specific error.

**Or check Railway community:**
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app/

---

## ✅ Success Indicators

When fixed, you'll see:
- ✅ Railway dashboard shows "Running" (green)
- ✅ Logs show "Uvicorn running on..."
- ✅ `curl https://your-url` returns a response (not 502)
- ✅ No error messages in logs

---

## 💡 Next: Share Your Logs

Please run:
```bash
railway logs
```

And share the output so we can see the specific error and fix it!

