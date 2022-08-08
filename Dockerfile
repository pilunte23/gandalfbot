FROM python:3.6
WORKDIR /usr/app/src
RUN pip3 install --no-cache --upgrade pip
RUN pip install discord.py \
&& pip install discord-py-slash-command \
&& pip install python-dotenv \
&& pip install requests \
&& pip install pillow \
&& pip install unidecode \
&& pip install discord-components

COPY . ./
CMD [ "python", "./main.py"]