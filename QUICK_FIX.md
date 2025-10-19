# 🚨 Quick Fix for Railway 502 Error

## What I Found
Your deployment is returning **502 - Application failed to respond**. This means the code deployed, but the app isn't starting.

## What I Fixed
1. ✅ Updated `mcp/requirements.txt` with all dependencies
2. ✅ Updated `runtime.txt` to Python 3.11.10 (stable version)

## 🎯 Next Steps

### Step 1: Check Your Logs (DO THIS FIRST!)

```bash
railway logs
```

**Share the error message you see.** This will tell us exactly what's wrong.

### Step 2: Test Locally FIRST

Before redeploying, let's make sure it works locally:

```bash
# Test the server starts
cd mcp
python src/main.py
```

**Expected output:**
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8123
```

If you see that, press `Ctrl+C` and continue to Step 3.

**If it fails locally:**
- Share the error message
- We need to fix it locally before Railway will work

### Step 3: Redeploy to Railway

```bash
# Commit the fixes
git add .
git commit -m "Fix: Update dependencies and Python version"
git push origin main
```

Railway will auto-redeploy. Wait ~1-2 minutes, then test:

```bash
curl https://offbench-shopify-production.up.railway.app
```

---

## 🔍 Common Issues & What to Look For

### Issue 1: Import Errors
**Log shows:** `ModuleNotFoundError: No module named 'xyz'`

**Fix:** That module is missing from `requirements.txt`

### Issue 2: Path Errors
**Log shows:** `FileNotFoundError` or `cannot find module`

**Fix:** The `Procfile` command needs adjustment:
```
# Try this instead:
web: python -m mcp.src.main
```

### Issue 3: Port Binding
**Log shows:** `Address already in use` or port errors

**Fix:** Check that `main.py` has:
```python
port = int(os.getenv("PORT", 8123))
```

### Issue 4: FastMCP HTTP Mode Not Working
**Log shows:** FastMCP errors or transport issues

**Fix:** Verify FastMCP is installed and HTTP transport works

---

## 📋 Checklist Before Redeploying

- [ ] Tested locally: `cd mcp && python src/main.py` ✅
- [ ] See "Uvicorn running" message ✅
- [ ] No import errors ✅
- [ ] Check Railway logs: `railway logs` ✅
- [ ] Committed changes: `git add . && git commit` ✅
- [ ] Pushed to GitHub: `git push` ✅

---

## 🆘 If Still Broken

### Option A: Try Alternative Procfile

Edit `Procfile` to:
```
web: python -m mcp.src.main
```

Or:
```
web: cd mcp && PYTHONPATH=/app python src/main.py
```

### Option B: Add Nixpacks Config

Create `nixpacks.toml`:
```toml
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "cd mcp && python src/main.py"
```

### Option C: Simplify Structure

Move everything out of `mcp/` subdirectory:
- Could be a path/import issue
- Railway might prefer flat structure

---

## 💬 Share Your Logs

**Most helpful thing you can do:**

Run this and share the output:
```bash
railway logs --tail 50
```

This will show the actual error, and we can fix it immediately.

---

## ✅ Success Looks Like

When fixed, you'll see:

**In Railway logs:**
```
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

**In curl test:**
```bash
curl https://offbench-shopify-production.up.railway.app
# Returns: JSON response (not 502 error)
```

**In Railway dashboard:**
- Status: "Running" (green circle)
- No crash loops
- Deployment shows ✓

---

## 🎯 Action Items

1. **RIGHT NOW:** Run `railway logs` and check for errors
2. **Test locally:** `cd mcp && python src/main.py`
3. **If local works:** Push the fixes and redeploy
4. **Share logs:** If still broken, share the Railway logs

Let's get this working! 🚀

