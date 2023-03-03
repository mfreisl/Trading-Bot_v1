# FROM python:3.9

# COPY . .
# COPY requirements.txt /requirements.txt

# # install app dependencies
# RUN pip install -r requirements.txt
# RUN pip install flask==2.1.*

# # final configuration
# ENV FLASK_APP=main
# EXPOSE 8000
# CMD

FROM ubuntu
CMD echo "This is a test." | wc -

# FROM python:3.9
# EXPOSE 8080

# WORKDIR /app

# COPY requirements.txt requirements.txt
# COPY . ./

# RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# CMD main.py
