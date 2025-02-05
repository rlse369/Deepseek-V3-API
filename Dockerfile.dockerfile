# Use an official lightweight Python image
FROM python:3.10-slim

WORKDIR /app

# Install required packages including nginx
RUN apt update && apt install -y nginx && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80

# Set the entrypoint script
CMD ["bash", "start.sh"]