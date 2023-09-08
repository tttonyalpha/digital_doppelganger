FROM python:3.7


COPY requirements.txt ./
RUN pip3 install -r requirements.txt

RUN mkdir /digital_copy
WORKDIR /digital_copy

COPY tg_bot_beta.py /digital_copy

ENTRYPOINT [ "python", "tg_bot_beta.py" ]


