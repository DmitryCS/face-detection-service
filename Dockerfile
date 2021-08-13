FROM ubuntu:20.04
RUN apt update -y
RUN DEBIAN_FRONTEND="noninteractive" apt install -y libgl1-mesa-glx libgtk2.0-dev
RUN apt install -y python3-pip python3-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN alembic upgrade head
ENTRYPOINT ["python3"]
CMD ["main.py"]