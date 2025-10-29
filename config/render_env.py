"""
Render-specific environment configuration
This file is used to inject DATABASE_URL when Render's environment variables fail to work
"""
import os
import sys

def setup_render_database():
    """
    Setup DATABASE_URL for Render deployment
    This is a workaround for Render's environment variable injection issues
    
    SECURITY NOTE: We check environment first before any fallback.
    In production, DATABASE_URL MUST be set in Render dashboard.
    """
    # Only set if not already in environment
    if not os.environ.get('DATABASE_URL'):
        # SECURITY: Check if running on Render platform
        if os.environ.get('RENDER'):
            # On Render, DATABASE_URL should be available from dashboard
            # If not found, it means configuration issue - fail loudly
            print("✗✗✗ CRITICAL: DATABASE_URL not found on Render!", file=sys.stderr, flush=True)
            print("✗ Please set DATABASE_URL in Render dashboard", file=sys.stderr, flush=True)
            # Raise error to prevent app from starting with wrong database
            raise EnvironmentError(
                "DATABASE_URL environment variable is required for Render deployment. "
                "Please set it in the Render dashboard."
            )
        else:
            # Local development - use SQLite (settings.py will handle this)
            print("⚠ DATABASE_URL not set - using SQLite for local development", flush=True)
    else:
        # Mask password in logs for security
        db_url = os.environ['DATABASE_URL']
        masked_url = db_url.split('@')[0].split(':')[0] + ':***@' + db_url.split('@')[1] if '@' in db_url else db_url[:20]
        print(f"✓ DATABASE_URL found: {masked_url}...", flush=True)

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
