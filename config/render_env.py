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
    """
    # Only set if not already in environment
    if not os.environ.get('DATABASE_URL'):
        # Get from Render's internal database connection
        # Format: postgresql://user:password@host/database
        os.environ['DATABASE_URL'] = 'postgresql://lmsdb_28b7_user:WCL8o8WhiO3RaaNjWBvZv85GwbdQ2zg5@dpg-d40qm7ili9vc73bshqig-a.oregon-postgres.render.com/lmsdb_28b7'
        print("✓ DATABASE_URL injected from render_env.py", flush=True)
    else:
        print(f"✓ DATABASE_URL already in environment: {os.environ['DATABASE_URL'][:50]}...", flush=True)

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
