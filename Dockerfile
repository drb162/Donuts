FROM python:3

WORKDIR /usr/src/app

COPY crypto.py .

RUN pip install pandas==0.25.3
RUN pip install requests==2.22.0
RUN pip install matplotlib==3.1.2

CMD ["python", "./crypto.py"]