#Bootstrap Firebase Admin SDK and set admin privileges for a user.

import os
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin._auth_utils import UserNotFoundError

# Load service account from env var or fallback
cred_path = os.getenv("FIREBASE_CRED_PATH", "firebase-service-account.json")
cred = credentials.Certificate(cred_path)

# Initialize Firebase app
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

def set_admin(uid: str, is_admin: bool = True):
    """Assign or remove admin privileges for a user by UID."""
    try:
        user = auth.get_user(uid)
        custom = user.custom_claims or {}
        if custom.get("creator", False):
            print("❌ Cannot modify creator account")
            return
        # preserve existing creator flag (safe when custom is {})
        creator_flag = custom.get("creator", False)
        auth.set_custom_user_claims(uid, {"admin": is_admin, "creator": creator_flag})
        status = "admin" if is_admin else "regular user"
        print(f"✅ User {uid} is now an {status} in Firebase claims.")

        # Optional: propagate change to your backend DB so routers (DB source-of-truth) stay in sync.
        # Requires an API endpoint (creator-only) or admin token. Configure BACKEND_URL and ADMIN_API_KEY env vars.
        backend_url = os.getenv("BACKEND_URL")
        admin_key = os.getenv("ADMIN_API_KEY")
        if backend_url and admin_key:
            import requests
            role_payload = {"is_admin": is_admin}
            try:
                resp = requests.put(
                    f"{backend_url}/api/users/{uid}/roles",
                    json=role_payload,
                    headers={"Authorization": f"Bearer {admin_key}"},  # or use your auth scheme
                    timeout=5,
                )
                if resp.ok:
                    print("✅ DB roles synced.")
                else:
                    print(f"⚠️ DB sync failed: {resp.status_code} {resp.text}")
            except Exception as e:
                print(f"⚠️ DB sync request failed: {e}")

    except UserNotFoundError:
        print(f"❌ No user found with UID: {uid}")
    except Exception as e:
        print(f"❌ Failed to update claims: {e}")


if __name__ == "__main__":
    uid = input("Enter the Firebase UID: ").strip()
    action = input("Grant admin? (y/n): ").strip().lower()
    set_admin(uid, is_admin=(action == "y"))
