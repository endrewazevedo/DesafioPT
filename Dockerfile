# Base image
FROM python:3.9

# Define working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install requirements
RUN pip install -r requirements.txt

# Copy application code
COPY app/ .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "main.py"]
