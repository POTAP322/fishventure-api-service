from jose import JWTError, jwt
from datetime import datetime
from fastapi import HTTPException
from config import settings
def verify_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Проверка времени истечения
        exp = payload.get("exp")
        if exp is None or datetime.utcnow() > datetime.utcfromtimestamp(exp):
            raise HTTPException(status_code=401, detail="Token expired")

        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



if __name__ == '__main__':
    # Пример использования
    token_to_test = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMSIsImV4cCI6MTc0NTc5MzkwM30.09atYg46s_KUZaG-aTSheIItkTkMDXZq3M0Zx_tJ_0g'

    try:
        user_id = verify_token(token_to_test)
        print(f"Token is valid. User ID: {user_id}")
    except HTTPException as e:
        print(f"Token verification failed: {e.detail}")