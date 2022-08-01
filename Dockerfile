FROM python:latest
WORKDIR /usr/app/src
RUN pip3 install --no-cache --upgrade pip
RUN pip install discord\
&& pip install discord-py-slash-command \
&& pip install python-dotenv \
&& pip install requests \
&& pip install pillow \
&& pip install unidecode \
&& pip install discord-components \
&& pip installbeautifulsoup4
COPY . ./
CMD [ "python", "./main.py"]