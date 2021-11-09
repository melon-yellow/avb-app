
FROM python:3.10

#################################################################################################################################################
# Install ODBC

RUN mkdir /opt/odbc
WORKDIR /opt/odbc
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

#Ubuntu 20.04
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN exit
RUN apt-get update -y
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
# optional: for bcp and sqlcmd
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN eval "$(cat ~/.bashrc | tail -n +10)"
# optional: for unixODBC development headers
RUN apt-get install -y unixodbc-dev

#################################################################################################################################################
# Install Oracle Instant Client

WORKDIR /opt/oracle
RUN apt-get update && apt-get install -y --no-install-recommends alien libaio1 wget && \
    wget https://download.oracle.com/otn_software/linux/instantclient/185000/oracle-instantclient18.5-basiclite-18.5.0.0.0-3.x86_64.rpm && \
    wget https://download.oracle.com/otn_software/linux/instantclient/185000/oracle-instantclient18.5-devel-18.5.0.0.0-3.x86_64.rpm && \
    alien -i oracle-instantclient18.5-basiclite-18.5.0.0.0-3.x86_64.rpm && \
    alien -i oracle-instantclient18.5-devel-18.5.0.0.0-3.x86_64.rpm
ENV LD_LIBRARY_PATH="/usr/lib/oracle/18.5/client64/lib:${LD_LIBRARY_PATH}"

#################################################################################################################################################

# pip Install Requirements
WORKDIR /usr/app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

#################################################################################################################################################
