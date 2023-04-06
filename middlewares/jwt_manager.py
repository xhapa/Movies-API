from jwt import encode, decode

def create_token(data: dict):
    token: str = encode(payload=data, key="HHJ3k12n1knlaldajk48o*", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data:dict = decode(token, key='HHJ3k12n1knlaldajk48o*', algorithms=['HS256'])
    return data