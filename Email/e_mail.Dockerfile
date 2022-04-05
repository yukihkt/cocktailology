FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./e_mail.py ./amqp_setup.py ./
CMD [ "python", "./e_mail.py" ]
