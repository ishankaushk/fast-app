from pydantic import BaseModel, EmailStr, Field



class Register(BaseModel):
	firstname: str=Field(title="Enter Your First name..", max_length=100)
	lastname: str=Field(title="Enter Your Last name..", max_length=100)
	city: str=Field(title="Enter Your City name where you located..", max_length=100)
	email: EmailStr
	password: str



class Login(BaseModel):
	email: EmailStr
	password: str


# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
    authjwt_secret_key: str = "secret"