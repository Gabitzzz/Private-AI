import os
import sys

# Add the current directory to sys.path so we can import open_webui
sys.path.append(os.getcwd())

try:
    from open_webui.models.auths import Auths
    from open_webui.utils.auth import get_password_hash
    from open_webui.internal.db import get_db_context
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

email = 'admin@1.com'
password = 'admin123'
name = 'Admin'
role = 'admin'

def create_user():
    print(f"Attempting to create user: {email}")
    hashed = get_password_hash(password)
    
    # Check if user already exists
    from open_webui.models.users import Users
    with get_db_context() as db:
        existing_user = Users.get_user_by_email(email.lower(), db=db)
        if existing_user:
            print(f"User {email} already exists. Skipping creation.")
            return

        user = Auths.insert_new_auth(
            email=email.lower(),
            password=hashed,
            name=name,
            role=role,
            db=db
        )

        if user:
            print(f"User {email} created successfully with role {role}!")
        else:
            print(f"Failed to create user {email}.")

if __name__ == "__main__":
    create_user()
