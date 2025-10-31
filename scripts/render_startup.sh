#!/usr/bin/env bash
# Render startup script - runs migrations, collectstatic, and creates superuser

set -e  # Exit on error

echo "🔄 Running migrations..."
python manage.py migrate --noinput
echo "✅ Migrations completed!"

echo "🔄 Collecting static files..."
python manage.py collectstatic --noinput --clear
echo "✅ Static files collected!"

echo "🔐 Creating/checking superuser..."
python manage.py ensure_superuser
echo "✅ Superuser check complete!"

echo "🚀 All startup tasks completed successfully!"
