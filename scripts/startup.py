#!/usr/bin/env python
"""
Render startup script - runs all pre-server tasks
"""
import subprocess
import sys

def run_command(description, command):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ ERROR: {description} failed!")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        sys.exit(1)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    print(f"✅ {description} completed!\n")
    return result

def main():
    print("=" * 60)
    print("🚀 RENDER STARTUP SCRIPT")
    print("=" * 60)
    
    # Run migrations
    run_command(
        "Running migrations",
        "python manage.py migrate --noinput"
    )
    
    # Collect static files
    run_command(
        "Collecting static files",
        "python manage.py collectstatic --noinput --clear"
    )
    
    # Create/ensure superuser exists
    run_command(
        "Creating/checking superuser",
        "python manage.py ensure_superuser"
    )
    
    print("=" * 60)
    print("✅ ALL STARTUP TASKS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
