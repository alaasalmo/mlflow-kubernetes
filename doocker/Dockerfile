FROM python:3.10

USER root:root
WORKDIR /usr/app

RUN pip install --no-cache-dir --upgrade pip
RUN apt-get -y upgrade
RUN pip install --upgrade pip
RUN pip --version
USER root:root
RUN useradd --user-group --system --no-log-init --create-home user
RUN apt-get update && apt-get install -y sqlite3
RUN chown -R user:user /home/user
WORKDIR /home/user
ENV MLFLOW_TRACKING_URI=file:/home/user
COPY requirements.txt .
COPY runmlflow.sh .
#COPY basic_auth.ini 
RUN chown user:user runmlflow.sh
RUN chmod a+x runmlflow.sh
RUN chown user:user requirements.txt
EXPOSE 5050
USER user:user
ENV PATH=$PATH:/home/user/.local/bin
COPY meta.yaml .
RUN pip install --no-cache-dir -r requirements.txt --user
#ENTRYPOINT ["sh"]
SHELL ["/bin/bash", "-c"]
CMD ["./runmlflow.sh"]
#CMD ["tail", "-f", "/dev/null"]