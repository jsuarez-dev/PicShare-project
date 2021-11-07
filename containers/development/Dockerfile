FROM python:3

# Set environment variables
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /
# Install dependencies.
RUN pip install -r /requirements.txt

COPY containers/development/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

# Set work directory.
RUN mkdir /code
WORKDIR /code

# Copy project code.
COPY . /code/
