####  import files  ####
from model import Register, Login, Settings
import databases
from fastapi import FastAPI, status, HTTPException, Depends, Request
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from passlib.context import CryptContext
from db import engine, metadata, database
from fastapi.responses import JSONResponse


metadata.create_all(engine)
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()

# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )




@app.get('/', tags=['testing'])  ####  path operation decorator  ####
def index():   ##### function  is called path operation function ##### 
	return {"message": "Hello Company"}



pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
@app.post('/registration', status_code=status.HTTP_201_CREATED, tags=['users'])
async def user_registration(register:Register):
	# querying database to check if user already exist
	res = await database.fetch_one('select * from USER_CRED where email='+"'"+str(register.email)+"'")
	if res is not  None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Email ID already exists")

	hashedPassword = pwd_cxt.hash(register.password)

	await database.execute("INSERT INTO USER_CRED (firstname,lastname, city,email,password) VALUES ("+"'"+str(register.firstname)+"'"+",'"+str(register.lastname)+"'"+",'"+str(register.city)+"'"+",'"+str(register.email)+"'"+",'"+str(hashedPassword)+"'"+")")
	return{"status":"HTTP_201_CREATED",
			"data": f"Hello {register.firstname} {register.lastname}, thanks for registration. "
		}


# provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token to use authorization
# later in endpoint protected
@app.post('/login/', tags=['login'])
async def login(login:Login, Authorize: AuthJWT = Depends()):
	
	user = await database.fetch_one('select * from USER_CRED where email='+"'"+str(login.email)+"'")
	if user is None:
		HTTPException(status_code=401, detail = "Bad email or password")

	hashed_pass = pwd_cxt.verify(login.password, user['password'])
	print('>>>>', hashed_pass)
	if hashed_pass is False:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Password is not correct")

	access_token = Authorize.create_access_token(subject=user.email)
	refresh_token = Authorize.create_refresh_token(subject=user.email)
	return {"access_token" : access_token, "refresh_token" : refresh_token, "msg" : "Successfully Login"}


@app.post('/refresh', tags=['login'])
def refresh(Authorize: AuthJWT = Depends()):
	Authorize.jwt_refresh_token_required()

	current_user = Authorize.get_jwt_subject()
	print('current_user')
	new_access_token = Authorize.create_access_token(subject=current_user)
	print('new_access_token')
	return {"access_token": new_access_token}


@app.delete('/logout', tags=['login'])
def logout(Authorize: AuthJWT = Depends()):
	Authorize.jwt_required()

	Authorize.unset_jwt_cookies()
	return {"msg": "Successfully Logout"}


@app.get('/login/user', tags=['login'])
def user(Authorize: AuthJWT = Depends()):
	Authorize.jwt_required()

	current_user = Authorize.get_jwt_subject()
	return {"user": current_user}




