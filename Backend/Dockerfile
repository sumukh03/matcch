# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

COPY app/script.sh app/script.sh

# Copy the requirements file to the container
COPY app/src/requirements.txt /app/requirements.txt

# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the entire src directory to the container
COPY app /app

# Expose port 5000 to communicate with the Flask app
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask application when the container launches
# CMD ["sh", "app/script.sh"]
RUN flask db init
RUN flask db migrate 
RUN flask db upgrade

CMD ["flask", "run"]


