from database import SessionLocal, Base, inspector
from encrypt import EncryptPassword, generate_key
from sqlalchemy.dialects.postgresql import UUID
from faker import Faker # This library is used to generate random users, emails, passwords with sense
import pandas as pd
import numpy as np
import models
import os, random, uuid

#os.system('cls')
db = SessionLocal()
fake = Faker() 

posible_path_photos = ['perfil_1.png', 'perfil_2.png', 'perfil_3.png', 'perfil_4.png', 'perfil_5.png', 'perfil_6.png', 'perfil_7.png', 'perfil_8.png', 'perfil_9.png', 'perfil_10.png']

base_dir = os.path.dirname(os.path.abspath(__file__))
dt = pd.read_csv(os.path.join(base_dir, "datasets", "users_emails.csv"))
usernames = np.array(dt.username)
emails = np.array(dt.email)
passwords = np.array(dt.password)

dt2 = pd.read_csv(os.path.join(base_dir, "datasets", "books_dataset.csv"))


"""
def createUsers_from_datasets():
    key = EncryptPassword.read_key()
    encrypter = EncryptPassword(key)
    print(key)

    for user, email, password in zip(usernames, emails, passwords):
        db_user = models.User(email=email, username=user, hashed_password=encrypter.encrypt_passowrd(password), is_active = True if random.randint(0,10) < 9 else False)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
"""

"""book_dg = pd.read_csv(os.path.join(os.getcwd(), "test_datasets", "Books.csv"), encoding="ISO-8859-1", low_memory=False)
book_pr = pd.read_csv(os.path.join(os.getcwd(), "test_datasets", "final_book_dataset_kaggle2.csv"), encoding="utf-8")
descrp_dt = pd.read_csv(os.path.join(os.getcwd(), "test_datasets", "books_with_desc.csv"))

def create_books_dataset():
    '''script to create books dataset'''
    book_titles = np.array(descrp_dt.title)
    prices = np.array(book_pr.price)
    descriptions = np.array(descrp_dt.description)

    books_dataframe = pd.DataFrame(columns=['book_title','description','photo_path','price','content'])

    for _ in range(300):
        # num_al = random.randint(1,10)

        book_title = book_titles[_]
        # Owner id? or directly when i'll create the databse
        photo_path = "/photos/"+ posible_path_photos[random.randint(0,9)]
        description = descriptions[_]
        price = prices[_]
        content = fake.text()

        books_dataframe = books_dataframe._append({'book_title':book_title,
                                'description':description, 
                                'photo_path':photo_path, 
                                'price': price,
                                'content':content}, ignore_index=True)

    return books_dataframe
"""

def get_all_users():
    try:
        users = db.query(models.Users).all()
        return [user.to_dict for user in users]
    finally:
        db.close()


AllUsers = pd.DataFrame(get_all_users())
def create_books_to_table():
    '''From the dataset, pass to a dataset'''

    user_count = -1
    for _ in range(300):
        if _ % 3 == 0:
            user_count += 1  
        owner_id = uuid.UUID(AllUsers.iloc[user_count].id)
        book_name = str(dt2.iloc[_].book_title)
        description = str(dt2.iloc[_].description)[:1000]
        photo_path = str(dt2.iloc[_].photo_path)
        price_value = str(dt2.iloc[_].price)
        if isinstance(price_value, str):
            price = float(price_value.replace(",", "."))
        else:
            price = float(price_value)
        content = str(dt2.iloc[_].content)[:1000]
        
        print(owner_id)

        db_book = models.Books_(owner_id=owner_id, book_title=book_name, description=description, photo_path=photo_path, price=price, content=content)
        
        try:
            db.add(db_book)
            db.commit()
            db.refresh(db_book)
        except Exception as e:
            print(f"Error inserting book: {e}")
            db.rollback()
      


if __name__ == "__main__":
    # print(dt2.iloc[1].description[:1000])
    create_books_to_table()
    print(inspector.get_table_names())

    #create_books_dataset().to_csv("datasets/books_dataset.csv", index=False)
    # print(book_dg.shape)
    # print(book_pr.shape)
    # print(descrp_dt.shape)