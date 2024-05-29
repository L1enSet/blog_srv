FROM python

WORKDIR /blog_server

COPY . ./

RUN pip3 install -r requirements.txt

CMD ["python3", "manage.py", "runserver"]