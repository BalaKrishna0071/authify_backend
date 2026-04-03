import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv

# --- Env ---
load_dotenv()


# --- JWT Class ---
class JwtService:

    # --- Default Constructor ---
    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")


    # ---- Create Access Token  Func ----
    def create_access_token(self, user_data: dict):
        """Create JWT Token"""

        try :
            payload = {
                "username": user_data["username"],
                "email": user_data["email"],
                "phone": user_data["phone"],
                "exp": datetime.utcnow() + timedelta(minutes=15),
                "type": "access",
            }
            jwt_token = jwt.encode(payload=payload, key=self.SECRET_KEY, algorithm=self.ALGORITHM)
            return jwt_token

        except Exception as e:
            print(f"exception occurred while creating jwt access token: {e} !")


    # ---- Create Refresh Token  Func ----
    def create_refresh_token(self, user_data: dict):
        """Create JWT Token"""

        try:
            payload = {
                "username": user_data["username"],
                "email": user_data["email"],
                "phone": user_data["phone"],
                "exp": datetime.utcnow() + timedelta(days=7 ),
                "type": "refresh",
            }
            jwt_token = jwt.encode(payload=payload, key=self.SECRET_KEY, algorithm=self.ALGORITHM)
            return jwt_token

        except Exception as e:
            print(f"exception occurred while creating jwt refresh token: {e} !")


    # ---- Verify Access Token Func ----
    def verify_refresh_token(self, token: str):
        """Verify JWT Token"""

        try:
            decoded = jwt.decode(token, key=self.SECRET_KEY, algorithms=self.ALGORITHM)
            return decoded
        except jwt.ExpiredSignatureError:
            print("expired signature !")

        except jwt.InvalidTokenError:
            print("invalid token !")

        except Exception as e:
            print(f"exception occurred while verifying access token: {e} !")