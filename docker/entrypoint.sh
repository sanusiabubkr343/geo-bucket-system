#!/bin/bash
set -e

# Find and set GDAL library paths dynamically
# Look for GDAL library
GDAL_PATH=$(find /usr -name "libgdal.so*" -type f 2>/dev/null | head -1)
if [ -n "$GDAL_PATH" ]; then
    # If it's a symlink, get the actual file
    if [ -L "$GDAL_PATH" ]; then
        GDAL_PATH=$(readlink -f "$GDAL_PATH")
    fi
    export GDAL_LIBRARY_PATH="$GDAL_PATH"
    echo "GDAL_LIBRARY_PATH set to: $GDAL_LIBRARY_PATH"
else
    echo "WARNING: libgdal.so not found!" >&2
    # Try common locations
    if [ -f "/usr/lib/x86_64-linux-gnu/libgdal.so" ]; then
        export GDAL_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu/libgdal.so"
    elif [ -f "/usr/lib/libgdal.so" ]; then
        export GDAL_LIBRARY_PATH="/usr/lib/libgdal.so"
    fi
fi

# Look for GEOS library
GEOS_PATH=$(find /usr -name "libgeos_c.so*" -type f 2>/dev/null | head -1)
if [ -n "$GEOS_PATH" ]; then
    # If it's a symlink, get the actual file
    if [ -L "$GEOS_PATH" ]; then
        GEOS_PATH=$(readlink -f "$GEOS_PATH")
    fi
    export GEOS_LIBRARY_PATH="$GEOS_PATH"
    echo "GEOS_LIBRARY_PATH set to: $GEOS_LIBRARY_PATH"
else
    echo "WARNING: libgeos_c.so not found!" >&2
    # Try common locations
    if [ -f "/usr/lib/x86_64-linux-gnu/libgeos_c.so.1" ]; then
        export GEOS_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu/libgeos_c.so.1"
    elif [ -f "/usr/lib/libgeos_c.so.1" ]; then
        export GEOS_LIBRARY_PATH="/usr/lib/libgeos_c.so.1"
    fi
fi

# Run database migrations if needed
if [ "$1" = "gunicorn" ] || { [ "$1" = "python" ] && [ "$2" = "manage.py" ]; }; then
    echo "Checking for new migrations..."
    python manage.py makemigrations --check --dry-run || echo "No new migrations detected or makemigrations check failed"

    echo "Making migrations..."
    python manage.py makemigrations --no-input || echo "Makemigrations failed, continuing..."

    echo "Running database migrations..."
    python manage.py migrate --no-input || echo "Migrations failed, continuing..."
fi

# Execute the command passed to the container
exec "$@"