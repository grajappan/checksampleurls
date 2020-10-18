FROM python:3
COPY ["checkurls_service.py", "/opt/checkurls_service/"]
COPY ["requirements.txt", "/opt/checkurls_service"]
RUN pip install --no-cache-dir -r /opt/checkurls_service/requirements.txt
WORKDIR /opt/checkurls_service/
CMD [ "python", "/opt/checkurls_service/checkurls_service.py" ]