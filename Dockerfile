FROM python:3.7

# Set the working directory in the container
WORKDIR /opt/assignment

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port (if needed)
EXPOSE 5000

# Command to run the application
ENTRYPOINT ["python3", "server.py"]
