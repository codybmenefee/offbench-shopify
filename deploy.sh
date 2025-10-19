#!/bin/bash

# Discovery Agent MCP - Vercel Deployment Script

echo "🚀 Discovery Agent MCP - Vercel Deployment"
echo "=========================================="
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found"
    echo ""
    echo "Install it with:"
    echo "  npm install -g vercel"
    echo ""
    echo "Or deploy manually via https://vercel.com/new"
    exit 1
fi

echo "✅ Vercel CLI found"
echo ""

# Check if logged in
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please login to Vercel..."
    vercel login
fi

echo ""
echo "📦 Deploying to Vercel..."
echo ""

# Deploy to production
vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Copy your deployment URL from above"
echo "  2. Add '/mcp' to the end (e.g., https://your-app.vercel.app/mcp)"
echo "  3. Configure in ChatGPT → Settings → Apps"
echo "  4. Test with: 'What projects are available?'"
echo ""
echo "📚 For detailed instructions, see VERCEL_DEPLOYMENT.md"
echo ""

