#
FROM roboflow/roboflow-inference-server-cpu:0.50.4

WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip uninstall numpy -y
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["/bin/sh", "-c"]
#