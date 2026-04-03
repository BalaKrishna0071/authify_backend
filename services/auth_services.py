from config.jwt_handler import JwtService
from config.security import Hashing
from fastapi import HTTPException, status
from repositories.user_repository import (insert_user_details, fetch_user_details,
                                          update_user_details, delete_user_details)

# --- Jwt instances ---
jwt_obj = JwtService()

# --- Hash Instances ---
hashing_obj = Hashing()

# --- Create user Func ---
def register_user(user_details: dict):
    """create user"""

    try:

        # --- Inserting into DB---
        insert_user_details(username=user_details["username"], email=user_details["email"],
                            password=hashing_obj.hash_password(password=user_details["password"]),
                            phone=user_details["phone"])


    except Exception as e:
        print(f"exception occurred while creating user: {e}")
        raise HTTPException(
            status_code=500,
            detail="internal server error"
        )


# --- Fetch user Func ---
def fetch_user(email: str, password: str):
    """fetch user"""

    try:

        # --- Fetching ----
        query_data = fetch_user_details(email=email)

        # --- Query Check ---
        if query_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # --- Check Password ---
        verified = hashing_obj.verify_password(password=password, hashed_password=query_data["password_hash"])
        if not verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # ---  Token Creation ---
        if verified:
            access_token = jwt_obj.create_access_token(user_data=query_data)
            refresh_token = jwt_obj.create_refresh_token(user_data=query_data)

            return query_data, access_token, refresh_token

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )



# --- Update user Func ---
def update_user(email: str, password: str):
    """update user"""

    try:

        update_user_details(email=email , password_hash=hashing_obj.hash_password(password))

    except Exception as e:
        print(f"exception occurred while updating user: {e}")


# --- Delete user Func ---
def remove_user(email: str, password: str):
    """delete user details"""

    try:
        # ---- Email & password Check ---
        if email is None and password is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user phone or password not found"
            )

        # --- Fetching user Details ---
        query_data = fetch_user_details(email=email)


        # ---- Checking Hash Password ----
        verified_user = hashing_obj.verify_password(password=password, hashed_password=query_data["password_hash"])
        if not verified_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # --- Deleting User Data ---
        delete_user_details(email=email)


    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# ---- Validates refresh Token & Creates Access Token -----
def validate_refresh_tkn_create_access_tkn(refresh_token: str):
    """validate refresh token"""

    try:
        payload  = jwt_obj.verify_refresh_token(refresh_token)
        if payload:
            access_token = jwt_obj.create_access_token(user_data=payload)
            return access_token

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

