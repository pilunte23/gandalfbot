FROM python:3.10
COPY ./assets/fonts/times-ro.ttf ./
RUN mkdir -p /usr/share/fonts/truetype/
RUN install -m644 times-ro.ttf /usr/share/fonts/truetype/
RUN rm ./times-ro.ttf
RUN adduser --disabled-password gandalf
USER gandalf
WORKDIR /home/gandalf
ENV PATH="/home/gandalf/.local/bin:${PATH}"
RUN pip3 install --upgrade pip
RUN pip install --user pillow\
&& pip install --user nextcord \
&& pip install --user python-dotenv \
&& pip install --user requests \
&& pip install --user unidecode 

COPY --chown=gandalf:gandalf . .

CMD ["python", "./main.py"]