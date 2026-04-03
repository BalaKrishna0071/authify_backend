from pydantic import BaseModel, EmailStr, Field, field_validator


# ----- Request Models ------


# ----- Update Model ----
class UpdateUserResponse(BaseModel):
    email: str
    password: str
    


# ------ Login Model -----
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


# ------ Delete Model ------
class DeleteUserRequest(BaseModel):
    email: str
    password: str


# ---- Register Model ----
class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    phone: int = Field(...)
    password: str = Field(..., min_length=8, max_length=30)

    # --- Password Check ---
    @field_validator("password")
    def validate_password(cls, value):
        """validating password"""

        if len(value) <8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain one number")
        if not any(char.upper() for char in value):
            raise ValueError("Password must contain one uppercase letter")
        return value

    # --- Email Check ---
    @field_validator("email")
    def validate_email(cls, value):
        """validating email"""
        if not value.endswith("@gmail.com"):
            raise ValueError("Email must end with ")
        return value

    # --- Phone Check ---
    @field_validator("phone")
    def validate_phone(cls, value):
        """validating phone"""

        if not value != 10:
            raise ValueError("Phone must contain 10 digits")
        return value



# ------ Response Models -------

# ---- Fetch Model ----
class FetchUserDataResponse(BaseModel):
    status: str
    message: str
    code: int
    user_data: dict



# ---- Register Model ----
class UserRegisterResponse(BaseModel):
    status: str
    message: str
    code: int



# ----- Update Model -----
class UserUpdateResponse(BaseModel):
    status: str
    message: str
    code: int

# ------- Refresh Token ------
class UserValidateRefreshTokenResponse(BaseModel):
    status: str
    message: str
    code: int
    access_token: str