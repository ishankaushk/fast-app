from sqlalchemy import create_engine, MetaData
import databases

####  Database config  ####
host_server ="localhost"
db_server_port ="5432" 
database_name ="habrie"
db_username ="root1"
db_password ="password"
ssl_mode ="prefer"

my_database_connection = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)
engine = create_engine(my_database_connection)
metadata = MetaData()
database = databases.Database(my_database_connection)
