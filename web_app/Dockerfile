FROM python
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8080
ENTRYPOINT [ "python" ]
CMD [ "app2.py" ] 