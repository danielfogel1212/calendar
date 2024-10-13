import os
from datetime import timedelta

class Config:
    # חיבור לבסיס הנתונים (ברירת מחדל MySQL דרך MySQL Connector)
    # תיקון השם ל- "restaurant"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://root:@localhost/calnder')
    
    # ביטול מעקב אחרי שינויים במבני הטבלאות (משפר ביצועים)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # מפתח סודי לשימוש ב-JWT (בברירת מחדל, מוגדר כערך קבוע)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', "d3f67a8b4c2e19f092c3a5b8d7e6f1a7b0c9d8e7f1a2c3b4d5e6f7a8b9c0d1e2")
    
    # תוקף של טוקן ה-JWT (במקרה הזה, 30 ימים)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
