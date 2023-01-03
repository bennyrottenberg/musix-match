FROM python:3.9.15-alpine
WORKDIR /opt/musix
COPY . ${WORKDIR}
RUN \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "main.py"]
CMD ["-l car"]
