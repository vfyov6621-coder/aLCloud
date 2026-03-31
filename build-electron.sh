#!/usr/bin/env bash
set -e

echo "=== aLCloud Build Script ==="
echo ""

# 1. Build Next.js
echo "[1/4] Building Next.js..."
NODE_ENV=production bun run build

# 2. Prepare Electron app directory
echo "[2/4] Preparing Electron package..."
DIST_DIR="electron-dist"
APP_DIR="$DIST_DIR/app"
rm -rf "$DIST_DIR"
mkdir -p "$APP_DIR"

# 3. Copy standalone server + prisma + db
echo "[3/4] Copying standalone server..."
cp -r .next/standalone/* "$APP_DIR/"
cp -r public "$APP_DIR/public"
cp -r prisma "$APP_DIR/prisma"
mkdir -p "$APP_DIR/node_modules/.prisma"
cp -r node_modules/.prisma/* "$APP_DIR/node_modules/.prisma/" 2>/dev/null || true
cp -r node_modules/@prisma "$APP_DIR/node_modules/@prisma" 2>/dev/null || true

# Ensure db folder exists
mkdir -p "$APP_DIR/db"

# 4. Build Electron app
echo "[4/4] Building Electron app..."
npx electron-builder \
  --config.electronDist="$DIST_DIR" \
  --config.directories.output="$DIST_DIR/installer" \
  --config.files="[\"electron/**/*\",\"app/**/*\"]" \
  --config.extraResources="[{\"from\":\"app\",\"to\":\"app\"}]" \
  --publish never

echo ""
echo "=== Build complete! ==="
echo "Installers are in: $DIST_DIR/installer/"
ls -la "$DIST_DIR/installer/" 2>/dev/null || echo "(no installers found)"
