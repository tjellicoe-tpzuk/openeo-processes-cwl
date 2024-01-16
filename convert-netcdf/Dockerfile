FROM python:3.12-slim
# standard thing
ENV PYTHONUNBUFFERED 1
# add this directory to the python path so if the file isnt found it looks here. strangely Steven has this as a string
ENV PYTHONPATH "/app"

#ENV PYTHONPATH /app

RUN apt-get update
RUN python3 -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app
RUN python -m pip install -r requirements.txt 

COPY convert_image/ convert_image/
ENTRYPOINT ["python", "-m", "convert_image"]


# FROM python:3.9-slim
 
# ENV PYTHONDONTWRITEBYTECODE 1 # dont compile any pthonC files
# ENV PYTHONUNBUFFERED 1 # standard thing
# ENV PYTHONPATH "/app" # add this directory to the python path so if the file isnt found
 
# RUN apt update
# RUN python -m pip install --upgrade pip # pip not in -slim version of python
 
# WORKDIR /app
# COPY requirements.txt .
# RUN python -m pip install -r requirements.txt 
 
# COPY invert-image/ invert-image/
# ENTRYPOINT [ "python", "-m", "invert-image" ]