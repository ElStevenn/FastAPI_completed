from database import SessionLocal, Base
from encrypt import EncryptPassword, generate_key
from faker import Faker # This library is used to generate random users, emails, passwords with sense
import pandas as pd
import numpy as np
import models
import os, random

db = SessionLocal()
fake = Faker()

posible_path_photos = ['perfil_1.png', 'perfil_2.png', 'perfil_3.png', 'perfil_4.png', 'perfil_5.png', 'perfil_6.png', 'perfil_7.png', 'perfil_8.png', 'perfil_9.png', 'perfil_10.png']

dt = pd.read_csv(os.path.join(os.getcwd(), "datasets", "users_emails.csv"))
usernames = np.array(dt.username)
emails = np.array(dt.email)
passwords = np.array(dt.password)


def createUsers_from_datasets():
    key = EncryptPassword.read_key()
    encrypter = EncryptPassword(key)
    print(key)

    for user, email, password in zip(usernames, emails, passwords):
        db_user = models.User(email=email, username=user, hashed_password=encrypter.encrypt_passowrd(password), is_active = True if random.randint(0,10) < 9 else False)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    

book_dg = pd.read_csv(os.path.join(os.getcwd(), "datasets", "Books.csv"), encoding="ISO-8859-1", low_memory=False)
book_pr = pd.read_csv(os.path.join(os.getcwd(), "datasets", "final_book_dataset_kaggle2.csv"), encoding="utf-8")
descrp_dt = ""

def create_books_on_cascade():
    """create books"""
    book_titles = np.array(book_dg.Book_Title)
    prices = np.array(book_pr.price)

    for _ in range(300):
        num_al = random.randint(1,10)
        book_title = book_titles[_]
        content = fake.text()
        photo_path = "/photos/"+ posible_path_photos[random.randint(0,9)]
        description = "" # End this, get descrpitons
        price = prices[_]


    


    


if __name__ == "__main__":
    # create_books_on_cascade()
    print(book_dg.shape)
    print(book_pr.shape)