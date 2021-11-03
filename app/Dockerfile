FROM python:3.10

# Install ODBC
RUN apt-get update --assume-yes
RUN apt-get install unixodbc-dev --assume-yes

# Install Oracle Instant Client
WORKDIR /opt/oracle
RUN wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip && \
    unzip instantclient-basiclite-linuxx64.zip && rm -f instantclient-basiclite-linuxx64.zip && \
    cd /opt/oracle/instantclient* && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci && \
    echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && ldconfig

# pip Install Requirements
WORKDIR /usr/app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt