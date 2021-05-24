import os
class Settings:
    secretKey="a12nc)238OmPq#cxOlm*a"

    #Dev
    #host='localhost'
    #database='furniture'
    #user='root'
    #password='root'

    #Staging on Heroku
    host=os.environ['HOST']
    database=os.environ['DATABASE']
    user=os.environ['USERNAME']
    password=os.environ['PASSWORD']
