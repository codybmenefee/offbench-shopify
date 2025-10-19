#!/bin/bash
# Quick deployment test script

echo "🔍 Testing MCP Server Deployment..."
echo ""

# Test 1: Check if we can import
echo "Test 1: Checking imports..."
cd mcp
python -c "from src.main import mcp; print('✅ Imports work')" 2>&1
IMPORT_STATUS=$?
cd ..

if [ $IMPORT_STATUS -ne 0 ]; then
    echo "❌ Import failed - check dependencies"
    exit 1
fi

# Test 2: Check if server starts
echo ""
echo "Test 2: Starting server (will run for 3 seconds)..."
cd mcp
timeout 3s python src/main.py &
SERVER_PID=$!
sleep 2

# Check if process is still running
if ps -p $SERVER_PID > /dev/null 2>&1; then
    echo "✅ Server is running"
    kill $SERVER_PID 2>/dev/null
else
    echo "❌ Server crashed on startup"
    cd ..
    exit 1
fi
cd ..

# Test 3: Check Railway deployment
echo ""
echo "Test 3: Testing Railway deployment..."
RESPONSE=$(curl -s -w "\n%{http_code}" https://offbench-shopify-production.up.railway.app)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" == "502" ]; then
    echo "❌ Railway returns 502 - app not responding"
    echo ""
    echo "Next steps:"
    echo "1. Run: railway logs"
    echo "2. Check for error messages"
    echo "3. Fix the error and redeploy"
elif [ "$HTTP_CODE" == "200" ]; then
    echo "✅ Railway deployment working!"
else
    echo "⚠️  Got HTTP $HTTP_CODE"
fi

echo ""
echo "📋 Summary:"
echo "  Local imports: $([ $IMPORT_STATUS -eq 0 ] && echo '✅' || echo '❌')"
echo "  Local server: ✅"
echo "  Railway deployment: $([ "$HTTP_CODE" == "200" ] && echo '✅' || echo '❌')"

if [ "$HTTP_CODE" != "200" ]; then
    echo ""
    echo "🔧 To fix:"
    echo "  1. railway logs (check for errors)"
    echo "  2. git add . && git commit -m 'Fix deployment'"
    echo "  3. git push (Railway auto-redeploys)"
fi

