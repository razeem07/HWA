# Use Python 3.12 as per your pycache versions
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies for psycopg2 and general health
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy entrypoint script OUTSIDE of /app to protect it from volume mounts
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create a directory for static files (used by collectstatic)
RUN mkdir -p /app/staticfiles

# Port for Gunicorn
EXPOSE 8000

# Set the ENTRYPOINT
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# We use a shell form to allow environment variable expansion if needed
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--pythonpath", "/app", "--workers", "2", "--timeout", "120", "elister.wsgi:application"]