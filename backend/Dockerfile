FROM python

WORKDIR /backend

COPY . .
RUN pip install -r requirements.txt
RUN openssl rand -hex 32 > ./app/security/secret_key.txt
EXPOSE 8080

CMD python ./run_uvicorn.py