# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory

COPY ./requirements.txt .

COPY ./django_web_app /app/django_web_app

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code to the working directory
WORKDIR /app/django_web_app
# Expose the port on which your Django application will run (if applicable)
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

