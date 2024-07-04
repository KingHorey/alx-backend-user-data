#!/usr/bin/env python3

""" hashing passwords usng bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash password """
    password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return password
