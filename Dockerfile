FROM python:3

ENV AWS_ACCESS_KEY_ID=value
ENV AWS_SECRET_ACCESS_KEY=value
ENV DNS=value
ENV ID=value

ADD aws-dyndns.py /

RUN pip install awscli boto3 

CMD python aws-dyndns.py --dns ${DNS} --id ${ID} 