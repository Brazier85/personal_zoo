# Use the official Python base image
FROM python:3.9 AS base

LABEL maintainer="Ferdinand Berger <ferdy@berger-em.de>" \ 
      description="Personal Zoo - visit: https://personal-zoo.com"

# Set the working directory inside the container
WORKDIR /app

# Setings for ARM7
FROM base AS base-arm
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
# Copy the required files into the container
COPY . ./

# Settings for amd64
FROM base AS base-amd64
# Copy the required files into the container
COPY . ./

# Settings for arm64
FROM base AS base-arm64
# Copy the required files into the container
COPY . ./

# Main build procress
FROM base-${TARGETARCH}
WORKDIR /app

# Install the dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose the port your application is running on
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]
