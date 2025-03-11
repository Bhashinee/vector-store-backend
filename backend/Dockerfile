# ------------------------------
# Stage 1: Build dependencies
# ------------------------------
    # Use the official Ubuntu base image
    FROM ubuntu:22.04

    # Set environment variables to prevent interactive prompts during package installation
    ENV DEBIAN_FRONTEND=noninteractive

    # Update package list and install dependencies
    RUN apt-get update && \
        apt-get install -y \
        software-properties-common \
        curl \
        gnupg2 \
        lsb-release \
        ca-certificates && \
        # Add the deadsnakes PPA for Python 3.11
        add-apt-repository ppa:deadsnakes/ppa && \
        apt-get update && \
        # Install Python 3.11 and pip
        apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip && \
        # Clean up unnecessary packages
        rm -rf /var/lib/apt/lists/*

    # Verify the installation
    RUN python3.11 --version && \
        pip3 --version

    # Set the default Python version
    RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

    # Set the default pip version
    RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

    # Set environment variables for NLTK
    ENV NLTK_DATA=/tmp/usr/local/share/nltk_data
    
    # Ensure nltk_data directory exists and has permissions
    RUN mkdir -p tmp/usr/local/share/nltk_data && \
        chmod -R 777 tmp/usr/local/share/nltk_data
    
    # Install pip and NLTK before downloading data
    RUN python3 -m ensurepip --upgrade && \
        python3 -m pip install --no-cache-dir nltk
    
    # Download necessary NLTK data
    RUN python3 -m nltk.downloader -d tmp/usr/local/share/nltk_data punkt_tab
    
    # Set working directory
    WORKDIR /app

    # Install required system dependencies for OpenCV and libGL
    RUN apt-get update
    RUN apt-get install -y \
        libgl1-mesa-glx \
        libglu1-mesa \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
        && rm -rf /var/lib/apt/lists/*
    
    # Install dependencies (using pip cache for faster builds)
    COPY requirements.txt .
    
    RUN python3 -m venv /app/venv
    
    RUN --mount=type=cache,target=/root/.cache/pip . /app/venv/bin/activate && \
        python3 -m pip install -r /app/requirements.txt  
    
    # Copy application source code
    COPY . .
    
    # Set environment variables
    ENV PYTHONUNBUFFERED=1 \
        PYTHONDONTWRITEBYTECODE=1 \
        NLTK_DATA=/tmp/usr/local/share/nltk_data
    
    # Expose application port (modify as needed)
    EXPOSE 9000
    
    # Create a user with a known UID/GID within range 10000-20000.
    RUN adduser \
        --disabled-password \
        --gecos "" \
        --home "/nonexistent" \
        --shell "/sbin/nologin" \
        --no-create-home \
        --uid 10014 \
        "choreo"
    
    # Use the above created unprivileged user
    USER 10014
    
    # Start the Python backend (modify for Flask, FastAPI, or Django)
    CMD ["/bin/sh", "-c", ". /app/venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 9000"]
