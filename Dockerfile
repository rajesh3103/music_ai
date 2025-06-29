# Use a slim version of Python 3.10 as base image
FROM python:3.10-slim

# Install required system libraries including ffmpeg and build tools
RUN apt-get update && apt-get install -y \
    ffmpeg \
    pkg-config \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libavfilter-dev \
    libswscale-dev \
    libswresample-dev \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy rest of the app
COPY . .

# Expose the port your app will run on (Flask default is 5000)
EXPOSE 5000

# Start the app using waitress (replace with your actual start command)
CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "5000", "app:app"]
