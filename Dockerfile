FROM python:3.10.8-slim-buster

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install pip && pip3 install -r requirements.txt
RUN mkdir /TheMovieProviderBot
WORKDIR /TheMovieProviderBot
COPY start.sh /start.sh
CMD ["/bin/bash", "/start.sh"]
