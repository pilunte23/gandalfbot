FROM python:3.10
RUN adduser --disabled-password gandalf
USER gandalf
WORKDIR /home/gandalf
ENV PATH="/home/gandalf/.local/bin:${PATH}"
RUN pip3 install --upgrade pip
RUN pip install --user discord\
&& pip install --user discord-py-interactions \
&& pip install --user python-dotenv \
&& pip install --user requests \
&& pip install --user pillow \
&& pip install --user unidecode

COPY --chown=gandalf:gandalf . .

CMD ["python", "./main.py"]