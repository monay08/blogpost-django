# Use official Python image
FROM python:3.12

# Set environment variables
ENV DJANGO_ALLOWED_HOSTS="0.0.0.0,127.0.0.1,localhost"

# Set working directory inside container
WORKDIR /views

# Copy the project files into the container
COPY . /views/

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
