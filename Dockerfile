# Use the official Python base image
FROM python:3.9

LABEL maintainer="Ferdinand Berger <ferdy@berger-em.de>" \ 
      description="Personal Zoo - visit: https://personal-zoo.com"

# Add rust for arm7 build required
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Set the working directory inside the container
WORKDIR /app

# Copy the required files into the container
COPY . ./

# Install the dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose the port your application is running on
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]
