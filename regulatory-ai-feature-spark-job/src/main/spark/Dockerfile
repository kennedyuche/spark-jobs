# FROM gcr.io/datamechanics/spark:3.2.0-hadoop-3.3.1-java-11-scala-2.12-python-3.8-dm16
# FROM gcr.io/datamechanics/spark:3.1.1-hadoop-3.2.0-java-11-scala-2.12-python-3.8-dm17
FROM gcr.io/datamechanics/spark:3.1.1-hadoop-3.2.0-java-11-scala-2.12-python-3.8-latest

USER root:root

ENV PYSPARK_MAJOR_PYTHON_VERSION=3
WORKDIR /opt/application/

# USER ${spark_uid}

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py .
COPY sparkjob.py .
COPY config.cfg.template .

RUN python3 sparkjob.py 

#ENTRYPOINT [ "/opt/entrypoint.sh" ]
