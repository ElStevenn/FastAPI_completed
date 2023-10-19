from database import SessionLocal, Base
from encrypt import EncryptPassword, generate_key
from faker import Faker # This library is used to generate 
import pandas as pd
import numpy as np
import models
import os, random

db = SessionLocal()

dt = pd.read_csv(os.path.join(os.getcwd(), "datasets", "users_emails.csv"))
usernames = np.array(dt.username)
emails = np.array(dt.email)
passwords = np.array(dt.password)


def createUsers_from_datasets():
    key = EncryptPassword.read_key()
    encrypter = EncryptPassword(key)
    print(key)

    for user, email, password in zip(usernames, emails, passwords):
        db_user = models.User(email=email, username=user, hashed_password=encrypter.encrypt_passowrd(password), is_active = True if random.randint(0,10) < 8 else False)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    
    
    


    


if __name__ == "__main__":
    createUsers_from_datasets()
    