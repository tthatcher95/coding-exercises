# 
FROM python:3.8-bullseye

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip config --user set global.progress_bar off
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
CMD ["fastapi", "run", "app/main.py", "--port", "80"]