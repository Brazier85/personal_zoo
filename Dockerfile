# Use the official Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Install git
RUN apt-get update
RUN apt-get install -y git

#RUN git clone https://github.com/Brazier85/personal_zoo.git /app

# Copy the required files into the container
COPY config.py .
COPY functions.py .
COPY main.py .
COPY momentjs.py .
COPY requirements.txt .

# Folders
COPY blueprints blueprints
COPY data data
COPY static static
COPY templates templates

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your application is running on
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]
