# Use an official Python image as the base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install system dependencies for OpenGL, EGL, and SDL
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libegl1-mesa \
    libgles2-mesa \
    libglu1-mesa \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    mesa-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir pygame PyOpenGL pywavefront Pillow

# Expose the port if the app uses networking (optional)
# EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]