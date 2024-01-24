from fastapi import HTTPException, status
from jose import JWTError, jwt
import sqlite3
import bcrypt
import os

SECRET_KEY = "your-secret-key"  # Replace with a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

class TokenData:
    def __init__(self, username: str = None):
        self.username = username

class User:
    username: str
    password: str

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Auth:
    database_path = "/app/db/auth.db"

    def get_user(self, username: str) -> User | None:
        self.check_create_db()
        
        con = sqlite3.connect(self.database_path)
        cur = con.cursor()
        res = cur.execute("SELECT * FROM users WHERE username = ?", [username])
        data = res.fetchone()
        if data is None:
            return None
        
        username = data[0]
        password = data[1]
        con.close()
        return User(username, password)
    
    def check_create_db(self):
        if not os.path.exists('/app/db'):
            os.makedirs('/app/db')
            con = sqlite3.connect(self.database_path)
            cur = con.cursor()
            cur.execute("CREATE TABLE users (username varchar(255) PRIMARY KEY, password varchar(255))")
            con.commit()
            con.close()

    def add_user(self, username: str, password: str):
        self.check_create_db()

        con = sqlite3.connect(self.database_path)
        cur = con.cursor()
        res = cur.execute("INSERT INTO users VALUES (?, ?)", [username, self.salt_hash_pwd(password)])
        con.commit()
        con.close()
    
    def verify_token(self, token: str) -> TokenData:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("uname")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        return token_data
    
    def login_for_access_token(self, username: str, password: str) -> str:
        user = self.get_user(username)
        if user and self.check_hashed_pwd(user.password, password):
            token_data = {"uname": username}
            token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
            return token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    def salt_hash_pwd(pwd: str):
        bytes = pwd.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(bytes, salt)
    
    def check_hashed_pwd(hashed: str, pwd: str):
        pwdBytes = pwd.encode('utf-8')
        return bcrypt.checkpw(pwdBytes, hashed)
