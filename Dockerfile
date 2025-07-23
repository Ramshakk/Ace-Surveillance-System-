# Base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files to the working directory
COPY . /app

# Install the required Python dependencies
RUN pip install -r requirements.txt

# Expose the desired port for your application
EXPOSE 80

# Specify the command to run your application
CMD ["python", "login.py"]
