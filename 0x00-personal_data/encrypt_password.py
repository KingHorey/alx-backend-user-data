#!/usr/bin/env python3

""" hashing passwords usng bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash password """
    password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ checks if a provided passwords is valid """
    result = bcrypt.checkpw(password.encode("utf-8"), hashed_password)
    return result
