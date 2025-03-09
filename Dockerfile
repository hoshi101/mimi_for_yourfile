FROM python:3.9-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create directories if they don't exist
RUN mkdir -p vectorestore
RUN mkdir -p source_data

# Expose the port
EXPOSE 7860

# Command to run the application
CMD ["python", "main.py"]