from passlib.context import CryptContext



# ---- Class Hashing ----
class Hashing:

    # --- Default Constructor ---
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


    # --- Hashing Func ---
    def hash_password(self, password) -> str | None:
        """Hash password"""

        try:
            if password:
                return self.pwd_context.hash(password)
            else:
                print("password is None")

        except Exception as e:
            print(f"exception occurred while hashing: {e} !")
            return None


    # ---- Verify Hashing Func -----
    def verify_password(self, password: str, hashed_password: str) -> bool | None:
        """Verify password"""

        try:

            if password and hashed_password:
                return self.pwd_context.verify(secret=password , hash=hashed_password)
            else:
                print("password is None")
                return  None

        except Exception as e:
            print(f"exception occurred while verifying password: {e} !")
            return None