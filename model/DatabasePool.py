from mysql.connector import Error
from mysql.connector import pooling
from config.Settings import Settings


class DatabasePool:
    #class of variables
    connection_pool = pooling.MySQLConnectionPool(pool_name="ws_pool",
                                                  pool_size=5,
                                                  #host='localhost',
                                                  #database='furniture',
                                                  #user='root',
                                                  #password='root',
                                                  host=Settings.host,
                                                  database=Settings.database,
                                                  user=Settings.user,
                                                  password=Settings.password
)


    @classmethod
    def getConnection(cls):
        dbConn = cls.connection_pool.get_connection()
        return dbConn