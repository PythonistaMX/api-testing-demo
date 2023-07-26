"""Schemas for the auth module."""

from apiflask import Schema
from apiflask.fields import String


class LoginSchema(Schema):
    username = String(required=True)
    password = String(required=True)
