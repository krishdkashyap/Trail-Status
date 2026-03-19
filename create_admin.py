"""
create_admin.py — Create the admin user

Run once to set up your admin login:
    python3 create_admin.py

You'll be prompted to enter a username and password.
The password is hashed before storing — it's never saved as plain text.
"""

from app import app
from models import db, User

def create_admin():
    with app.app_context():
        db.create_all()

        username = input("Admin username: ").strip()
        password = input("Admin password: ").strip()

        if User.query.filter_by(username=username).first():
            print(f"User '{username}' already exists.")
            return

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"Admin user '{username}' created successfully.")

if __name__ == "__main__":
    create_admin()
