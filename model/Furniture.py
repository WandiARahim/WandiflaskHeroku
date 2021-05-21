from model.DatabasePool import DatabasePool

class Furniture:
    @classmethod
    def getAllFurniture(cls):
        dbConn=DatabasePool.getConnection()
        db_Info = dbConn.connection_id

        cursor = dbConn.cursor(dictionary=True)

        cursor.execute("select * from furniture")
        furniture = cursor.fetchall()
        print(f"Connected to {db_Info}")
        
        dbConn.close()
        return furniture

    @classmethod
    def getFurnitureByCatID(cls,catid):
        dbConn=DatabasePool.getConnection()
        db_Info = dbConn.connection_id

        cursor = dbConn.cursor(dictionary=True)

        sql="select f.*,c.cat_name from furniture f,category c where c.cat_id=f.cat_id and f.cat_id=%s"
        cursor.execute(sql,(catid,))
        furniture = cursor.fetchall()
        print(f"Connected to {db_Info}")
        
        dbConn.close()
        return furniture