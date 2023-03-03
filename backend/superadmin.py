import argparse
from models.admin import Admin
from fastapi import Body
from passlib.context import CryptContext

hash_helper = CryptContext(schemes=["bcrypt"])

arg = argparse.ArgumentParser()
arg.add_argument("-u", "--user", help="Username")
arg.add_argument("-p", "--password", help="Password")
arg.add_argument("-e", "--email", help="Email")

args = arg.parse_args()

def main():
    password = hash_helper.encrypt(args.password)
    if args.user and args.password and args.email:
        new_superadmin:Admin = Body(Admin(fullname=args.user, email=args.email, password=password, role="superadmin"))
        superadmin_exists = Admin.find_one(Admin.email == new_superadmin.email)
        if superadmin_exists:
            print("SuperAdmin with email supplied already exists")
        else:
            new_superadmin.save()
            print("SuperAdmin created successfully")
    else:
        print("Please provide all the required arguments")


if __name__ == "__main__":
    main()