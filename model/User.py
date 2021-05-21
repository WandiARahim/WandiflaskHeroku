from model.DatabasePool import DatabasePool
from config.Settings import Settings
import bcrypt
import datetime
import jwt


class User:

    @classmethod
    def getUser(cls,userid):
        try:
            dbConn=DatabasePool.getConnection()

            cursor = dbConn.cursor(dictionary=True)
            sql="select * from user where userid=%s"

            cursor.execute(sql,(userid,))
            users = cursor.fetchall() 

            return users

        finally:
            dbConn.close()
            print("release connection")

    @classmethod
    def getAllUsers(cls):
        dbConn=DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)
        sql="select * from user"
        cursor.execute(sql)
        users = cursor.fetchall()

        dbConn.close()

        return users

    @classmethod
    def insertUser(cls,userJson):
        dbConn=DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)

        password = userJson["password"].encode()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        sql="insert into user(username,email,role,password) Values(%s,%s,%s,%s)"
        users = cursor.execute(sql,(userJson["username"],userJson["email"],userJson["role"],hashed))
        
        dbConn.commit()
        rows=cursor.rowcount

        dbConn.close()

        return rows

    
    @classmethod
    def updateUser(cls,userid,email,password):
        dbConn=DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)

        #password need to be hash for new version with hashing
        sql="update user set email=%s,password=%s where userid=%s"
        users = cursor.execute(sql,(email,password,userid))
        dbConn.commit()
        rows=cursor.rowcount

        dbConn.close()

        return rows

    @classmethod
    def deleteUser(cls,userid):
        dbConn=DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)

        sql="delete from user where userid=%s"
        users = cursor.execute(sql,(userid,))
        dbConn.commit()
        rows=cursor.rowcount

        dbConn.close()

        return rows

    @classmethod
    def loginUser(cls,userJSON):
        try:
            dbConn=DatabasePool.getConnection()
            
            print(userJSON)
            cursor = dbConn.cursor(dictionary=True)
            sql="select * from user where email=%s"

            cursor.execute(sql,(userJSON["email"],))
            user = cursor.fetchone() #at most 1 record since email is supposed to be unique
            if user==None:
                return {"jwt":""}

            else:
                
                password=userJSON["password"].encode()
                hashed=user['password'].encode()
                
                if bcrypt.checkpw(password, hashed):#True means valid password 
                    payload={"userid":user["userid"],"role":user["role"],"exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=7200)}

                    jwtToken=jwt.encode(payload,Settings.secretKey,algorithm="HS256")
                    return {"jwt":jwtToken}
                else:
                    return {"jwt":""}
        finally:
            dbConn.close()
