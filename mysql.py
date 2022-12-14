import mysql.connector

cnx = mysql.connector.connect(
        host="mysql.ocio.monash.edu",
        user="pokedb",
        database="pokedb",
        password="Po*l6K12e-2208-15",
        ssl_ca="ca-key.pem",
        ssl_cert="client-cert.pem",
        ssl_key="client-key.pem",
        )

print(cnx)