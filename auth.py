# auth.py

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fido2.server import Fido2Server, RelyingParty
from fido2.webauthn import (
    PublicKeyCredentialRpEntity,
    UserVerificationRequirement,
)
from fido2 import cbor
from .models import WebAuthnCredential, User
from typing import List
from .config import settings
from jose import jwt, JWTError
from datetime import timedelta, datetime
from .logging import logger

router = APIRouter()

rp = RelyingParty(settings.origin, settings.rp_id)
fido2_server = Fido2Server(rp)


@router.post("/register/options")
async def register_options(request: Request):
    data = await request.json()
    username = data.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")
    existing_user = await User.find_one(User.username == username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user_id = username.encode("utf-8")
    registration_data, state = fido2_server.register_begin(
        {
            "id": user_id,
            "name": username,
            "displayName": username,
        },
        user_verification=UserVerificationRequirement.PREFERRED,
    )

    # Store state in session
    request.session["state"] = state
    request.session["username"] = username
    return JSONResponse(
        content=cbor.encode(registration_data), media_type="application/octet-stream"
    )


@router.post("/register/complete")
async def register_complete(request: Request):
    data = await request.body()
    state = request.session.get("state")
    username = request.session.get("username")
    if not state or not username:
        raise HTTPException(status_code=400, detail="No registration in progress")

    existing_user = await User.find_one(User.username == username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    client_data = cbor.decode(data)
    auth_data = fido2_server.register_complete(
        state,
        client_data["clientDataJSON"],
        client_data["attestationObject"],
    )

    # Save user and credential to database
    user_data = {"username": username}
    for field_name, field_type in settings.custom_user_fields.items():
        user_data[field_name] = request.session.get(field_name)

    user = User(**user_data)
    credential = WebAuthnCredential(
        credential_id=auth_data.credential_id,
        public_key=auth_data.public_key,
        sign_count=auth_data.sign_count,
        transports=auth_data.transports,
    )
    user.credentials.append(credential)
    await user.create()
    logger.info(f"User {username} registered successfully")
    return {"status": "ok"}


@router.post("/authenticate/options")
async def authenticate_options(request: Request):
    data = await request.json()
    username = data.get("username")
    user = await User.find_one(User.username == username)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    credentials = [
        {
            "id": cred.credential_id,
            "transports": cred.transports,
        }
        for cred in user.credentials
    ]

    auth_data, state = fido2_server.authenticate_begin(credentials)
    request.session["state"] = state
    request.session["username"] = username
    return JSONResponse(
        content=cbor.encode(auth_data), media_type="application/octet-stream"
    )


@router.post("/authenticate/complete")
async def authenticate_complete(request: Request):
    data = await request.body()
    state = request.session.get("state")
    username = request.session.get("username")
    if not state or not username:
        raise HTTPException(status_code=400, detail="No authentication in progress")

    user = await User.find_one(User.username == username)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    credentials = {cred.credential_id: cred for cred in user.credentials}

    client_data = cbor.decode(data)
    credential_id = client_data["credentialId"]

    auth_data = fido2_server.authenticate_complete(
        state,
        credentials,
        credential_id,
        client_data["clientDataJSON"],
        client_data["authenticatorData"],
        client_data["signature"],
    )

    # Update sign count
    credential = credentials[credential_id]
    credential.sign_count = auth_data.new_sign_count
    await user.save()
    logger.info(f"User {username} authenticated successfully")

    # Generate JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = (
        datetime.utcnow() + expires_delta
        if expires_delta
        else datetime.utcnow() + timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


async def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = await User.find_one(User.username == username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
