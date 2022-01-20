
FROM python:3.10

#################################################################################################################################################
# Install ODBC

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# Ubuntu 20.04
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > \
    /etc/apt/sources.list.d/mssql-release.list
RUN exit

# Install Deps
RUN apt-get update -y
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

# optional: for bcp and sqlcmd
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN eval "$(cat ~/.bashrc | tail -n +10)"

# optional: for unixODBC development headers
RUN apt-get install -y unixodbc-dev

# Lower Minimum TLS Version
RUN echo 'MinProtocol = TLSv1.0' >> /etc/ssl/openssl.cnf
RUN echo 'CipherString = DEFAULT@SECLEVEL=1' >> /etc/ssl/openssl.cnf

#################################################################################################################################################

# pip Install Requirements
WORKDIR /usr/app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

#################################################################################################################################################
