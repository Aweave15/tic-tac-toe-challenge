FROM python:3.6

LABEL maintainer="Austin <aweave15@aol.com>"

######################
# Install Dependencies
######################

COPY requirements.txt /req/
RUN cd /req; pip install -r requirements.txt


######################
# Install Application
######################
ENV FLASK_ENV=development
COPY app /app/


EXPOSE 5000

WORKDIR /app
CMD ["python", "app.py"]


 