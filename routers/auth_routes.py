

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import APIRouter, HTTPException, status, Depends
from dependencies.auth_dependencies import access_token_validation
from services.auth_services import (register_user, fetch_user, update_user, remove_user,
                                    validate_refresh_tkn_create_access_tkn)
from models.auth_models import (UserRegisterResponse, UserRegisterRequest, FetchUserDataResponse, UserUpdateResponse,
                                UpdateUserResponse, DeleteUserRequest, UserLoginRequest,
                                UserValidateRefreshTokenResponse)

# ---- Security instances ---
security = HTTPBearer()


# --- Auth Router ---
router = APIRouter(prefix="/api/v1/auth", tags=["users"])



# ----  API 1  ----
@router.get("/")
def server_status():
    """Server Running Status"""

    return {
        "status": "Success",
        "message": "server running",
        "code": 200
    }



# ---- API 2 ----
@router.post("/login", response_model=FetchUserDataResponse)
def login_user(user_details: UserLoginRequest):
    """Fetch Users Data"""

    try:
        # --- User Details Check ---
        if user_details.email is None or user_details.password is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email and password required"
            )

        # --- Fetching ---
        db_data, access_token, refresh_token = fetch_user(user_details.email, user_details.password)

        # --- Db Query Check ---
        if db_data is None or access_token is None or refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email & password"
            )

        return {
            "status": "success",
            "message": "user data",
            "code": 200,
            "user_data": {
                "users": db_data,
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }
    except Exception as e:
        print("exception occurred while creating user", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal server error"
        )



# ---- API 3 ----
@router.post("/user", response_model=UserRegisterResponse)
def create_user(user_details: UserRegisterRequest):
    """Create User Data"""

    try:
        # --- Check ---
        if user_details is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user details required"
            )

       # --- inserting into DB ---
        register_user(user_details=user_details.model_dump())

        return {
            "status": "success",
            "message": "user created",
            "code": 201,
        }

    except Exception as e:
        print("exception occurred while creating user", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal server error"
        )



# ---- API 4 ----
@router.patch("/user", response_model=UserUpdateResponse)
def update_user_password(user_details: UpdateUserResponse, username = Depends(access_token_validation)):
    """Updates Users Data"""

    try:
        if user_details is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="password not found"
            )

        update_user(email=user_details.email, password=user_details.password)
        return {
            "status": "success",
            "message": f"{username} password updated",
            "code": 200
        }

    except Exception as e:
        print("exception occurred while updating user", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal server error"
        )



# ---- API 5 ----
@router.delete("/user")
def delete_user(user_details: DeleteUserRequest, username = Depends(access_token_validation)):
    """Delete User Data"""

    try:
        if user_details is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="user details not found"
            )

        remove_user(email=user_details.email, password=user_details.password)
        return {
            "status": "success",
            "message": f"{username} logout",
            "code": 200
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal server error"
        )

# ----- API 6 -----
@router.get("/refresh_token", response_model=UserValidateRefreshTokenResponse)
def validate_refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validates Refresh Token & create new Access Token"""

    try:
        refresh_token = credentials.credentials

        # ---- Refresh Token Check -----
        if refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="refresh token required"
            )

        # --- Validating Refresh Token & Creating Access Token
        access_token = validate_refresh_tkn_create_access_tkn(refresh_token=refresh_token)

        # ---- Token  Check ----
        if access_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        return {
            "status": "success",
            "message": "Access token created",
            "code": 201,
            "access_token": access_token
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal server error"
        )
