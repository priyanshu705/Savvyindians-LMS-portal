"""
Render-specific environment configuration
This file is used to inject DATABASE_URL when Render's environment variables fail to work
"""
import os

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
