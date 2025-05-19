# Use official Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Prevent pyppeteer from auto-downloading Chromium
ENV PYPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
# Set working directory
WORKDIR /app

# Install system dependencies required for Chromium and Poetry
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    ca-certificates \
    build-essential \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    libxcb-dri3-0 \
    libdrm2 \
    libxss1 \
    libglib2.0-0 \
    libgtk-3-0 \
    chromium \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy dependency files first (layer caching)
COPY pyproject.toml poetry.lock ./

# Install dependencies without installing the local package
RUN poetry install --no-root

# Copy the rest of your code
COPY . .

# Expose port
EXPOSE 8000

# Default command
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]