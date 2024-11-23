FROM python:3.10.15-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY migrations migrations
COPY f4lazylifes.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP f4lazylifes.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]