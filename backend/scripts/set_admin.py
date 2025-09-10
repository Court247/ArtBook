import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("firebase-service-account.json")
firebase_admin.initialize_app(cred)

def set_admin(uid):
    auth.set_custom_user_claims(uid, {"admin": True})
    print(f"✅ User {uid} is now an admin.")

if __name__ == "__main__":
    uid = input("Enter the Firebase UID: ").strip()
    set_admin(uid)
