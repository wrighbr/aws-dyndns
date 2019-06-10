# FROM ubuntu:18.04
FROM python:3

ENV AWS_ACCESS_KEY_ID=value
ENV AWS_SECRET_ACCESS_KEY=value
ENV DNS=value
ENV ID=value

ADD aws-dyndns.py /

# RUN apt update \
#     && apt upgrade -y \
#     && apt install -y cron python3 python3-pip

RUN pip3 install awscli boto3 

CMD python aws-dyndns.py --dns ${DNS} --id ${ID} 