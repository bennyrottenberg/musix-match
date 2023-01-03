FROM python:3.9.15-alpine
WORKDIR /opt/musix
COPY . ${WORKDIR}
RUN \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt
RUN chmod +x mainAPI.py
EXPOSE 9002
CMD ["uvicorn", "mainAPI:app", "--host", "0.0.0.0", "--port", "9002"]

