import argparse

from firebase_admin import auth
from firebase_admin.auth import UserRecord

from initialise_firebase_admin import app


def get_args():
    parser = argparse.ArgumentParser(description="Update user details in Firebase")

    parser.add_argument("--user-id", required=True, help="The user id of the user whose details are to be updated.")
    parser.add_argument("--email", required=False, help="The new email address to replace the existing email.")

    return parser.parse_args()


def update_email(user_id: str, email: str) -> UserRecord:
    return auth.update_user(user_id, email=email)


if __name__ == "__main__":
    args = get_args()

    if args.email:
        updated_user = update_email(args.user_id, args.email)
        print(f"Updated user email to {updated_user.email}")