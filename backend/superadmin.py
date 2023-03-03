import argparse
from passlib.context import CryptContext
import pymongo
import os

hash_helper = CryptContext(schemes=["bcrypt"])

arg = argparse.ArgumentParser()
arg.add_argument("-f", "--user", help="Username")
arg.add_argument("-p", "--password", help="Password")
arg.add_argument("-e", "--email", help="Email")

args = arg.parse_args()

def main():
    client = pymongo.MongoClient(os.getenv("DATABASE_URL"))
    if args.user and args.password and args.email:
        collection = client.get_default_database().admin
        password = hash_helper.encrypt(args.password)

        collection.insert_one({
            "fullname": args.user,
            "password": password,
            "email": args.email,
            "role": "superadmin"
        })
        
    else:
        print("Please provide all the required arguments")


if __name__ == "__main__":
    main()
