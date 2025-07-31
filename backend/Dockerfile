# Use a slim Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy all backend files to the container
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port where FastAPI will run
EXPOSE 8000

# Command to start FastAPI app using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
