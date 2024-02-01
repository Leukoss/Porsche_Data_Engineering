# Use an official Python runtime as a parent image
FROM python:3.11.5

WORKDIR /App

COPY Pipfile Pipfile.lock /App/
COPY root.py /App/
COPY AppFlask /App/AppFlask/

# Install any needed packages specified in requirements.txt
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Exposez le port sur lequel votre application Flask s'exécutera
EXPOSE 5000

CMD ["pipenv", "run", "python", "root.py"]