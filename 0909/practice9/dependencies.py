from fastapi import Header, HTTPException


def verify_token(x_token: str = Header()):
    if x_token != "secret":
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    return x_token
