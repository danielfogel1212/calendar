import os

class Config:
     
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://root:@localhost/calnder')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', "d3f67a8b4c2e19f092c3a5b8d7e6f1a7b0c9d8e7f1a2c3b4d5e6f7a8b9c0d1e2")
 
