# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file first for caching
COPY requirements.txt /app/

# Install required system packages and Python dependencies
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . /app

# Collect static files for serving
RUN python manage.py collectstatic --noinput

# Expose port 80
EXPOSE 80

# Use Gunicorn with more workers and threads for faster response
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--timeout", "30", "--workers", "2", "--threads", "4", "malaria_project.wsgi:application"]
