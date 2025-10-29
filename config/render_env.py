"""
Render-specific environment configuration
This file is used to inject DATABASE_URL when Render's environment variables fail to work
"""
import os
import sys

def setup_render_database():
    """
    Setup DATABASE_URL for Render deployment
    This checks for DATABASE_URL and provides helpful error messages if missing.
    
    SECURITY NOTE: No hardcoded credentials - environment variables only.
    """
    # Check if DATABASE_URL exists
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Check if running on Render platform
        if os.environ.get('RENDER'):
            print("⚠️  WARNING: DATABASE_URL not found on Render!", file=sys.stderr, flush=True)
            print("⚠️  This usually means:", file=sys.stderr, flush=True)
            print("   1. PostgreSQL database not linked to this service", file=sys.stderr, flush=True)
            print("   2. Database connection needs to be configured in Render dashboard", file=sys.stderr, flush=True)
            print("", file=sys.stderr, flush=True)
            print("💡 SOLUTION:", file=sys.stderr, flush=True)
            print("   Go to Render Dashboard → Your Service → Environment", file=sys.stderr, flush=True)
            print("   Add: DATABASE_URL = <your-postgres-connection-string>", file=sys.stderr, flush=True)
            print("", file=sys.stderr, flush=True)
            print("🔄 For now, attempting to continue with SQLite fallback...", file=sys.stderr, flush=True)
            # Don't raise error - let Django settings handle SQLite fallback
        else:
            # Local development - use SQLite (settings.py will handle this)
            print("⚠ DATABASE_URL not set - using SQLite for local development", flush=True)
    else:
        # Mask password in logs for security
        try:
            masked_url = database_url.split('@')[0].split(':')[0] + ':***@' + database_url.split('@')[1]
        except:
            masked_url = database_url[:20] + "..."
        print(f"✓ DATABASE_URL found: {masked_url}", flush=True)

def run_migrations_once():
    """
    Run Django migrations once on Render startup
    This ensures database tables exist before the app starts
    """
    # Only run on Render (check for Render-specific env var)
    if os.environ.get('RENDER'):
        try:
            import django
            from django.core.management import call_command
            
            print("🔄 Running migrations on Render startup...", file=sys.stderr, flush=True)
            
            # Setup Django
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_minimal')
            django.setup()
            
            # Run migrations
            call_command('migrate', '--noinput', verbosity=1)
            print("✓ Migrations completed successfully!", file=sys.stderr, flush=True)
            
            # Run collectstatic
            print("🔄 Collecting static files...", file=sys.stderr, flush=True)
            call_command('collectstatic', '--noinput', '--clear', verbosity=1)
            print("✓ Static files collected!", file=sys.stderr, flush=True)
            
        except Exception as e:
            print(f"⚠ Warning: Could not run migrations: {e}", file=sys.stderr, flush=True)
            # Don't fail - let the app start anyway
