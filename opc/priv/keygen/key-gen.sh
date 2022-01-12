# Create directory to store CA's files
mkdir ca
# Create CA key
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out ca/ca.key
# Create self-signed CA cert
openssl req -new -x509 -days 3600 -key ca/ca.key -subj "/CN=elixir-opex62541-client@uavbsrv/O=GUSA NORDESTE SA" -out ca/ca.crt
# Convert cert to der format
openssl x509 -in ca/ca.crt -inform pem -out ca/ca.crt.der -outform der
# Create cert revocation list CRL file 
# NOTE : might need to create in relative path
#        - File './demoCA/index.txt' (Empty)
#        - File './demoCA/crlnumber' with contents '1000'
openssl ca -crldays 3600 -keyfile ca/ca.key -cert ca/ca.crt -gencrl -out ca/ca.crl
# Convert cert to der format
openssl pkcs8 -topk8 -outform DER -in ca/ca.key -out ca/ca.key.der -nocrypt
# Convert CRL to der format
openssl crl -in ca/ca.crl -inform pem -out ca/ca.der.crl -outform der
