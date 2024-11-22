FROM python:3.9-slim

WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose Flask on port 8080
EXPOSE 8080

# Run Flask app
CMD ["python", "app.py"]
