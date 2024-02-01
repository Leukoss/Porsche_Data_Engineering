# Use an official Python runtime as a parent image
FROM python:3.11.5

# Set the working directory
WORKDIR .

# Copy the scraper script into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Command to run the scraper script
CMD ["pipenv", "run", "scrapy", "crawl", "porsche_france"]