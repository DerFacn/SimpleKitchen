#!/bin/bash

set -e  # Stopping on errors

# 📥 Pull latest changes
echo "📥 Pulling latest changes..."
git fetch origin main
git checkout main
git reset --hard origin/main

# 🛑 Stop running containers
echo "🛑 Stopping running containers..."
docker compose down

# 🧹 Remove old images
echo "🧹 Removing old images..."
docker image prune -f

# 🚀 Rebuild and start new container
echo "🚀 Rebuilding and starting new container..."
docker compose up -d --build --force-recreate

# ✅ Deployment complete
echo "✅ Deployment complete!"
docker ps