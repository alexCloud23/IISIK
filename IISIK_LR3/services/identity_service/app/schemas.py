from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    full_name: str
    is_active: bool
    created_at: datetime


class RoleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str | None


class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenRequest(BaseModel):
    token: str


class AuthPayloadDTO(BaseModel):
    token: str
    user: UserDTO
    roles: list[str]


class IntrospectDTO(BaseModel):
    user_id: str
    email: str
    full_name: str
    roles: list[str]
