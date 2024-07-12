#!/usr/bin/python3
""" Check response
"""


if __name__ == "__main__":
    from models.user_session import UserSession

    user_id = "User10"
    session_id = "The User 10 session ID"

    user_session = UserSession()
    user_session.user_id = user_id
    user_session.session_id = session_id
    user_session.save()

    from api.v1.auth.session_db_auth import SessionDBAuth
    sbda = SessionDBAuth()

    user_id_r = sbda.user_id_for_session_id(session_id)
    if user_id_r is None:
        print("user_id_for_session_id should return the User ID linked to the Session ID")
        exit(1)
    if user_id_r != user_id:
        print("user_id_for_session_id should return the User ID linked to the Session ID")
        exit(1)

    print("OK", end="")
if __name__ == "__main__":
    try:
        from api.v1.auth.session_db_auth import SessionDBAuth
        sbda = SessionDBAuth()
        session_id = "Session doesn't exist"
        user_id = sbda.user_id_for_session_id(session_id)
        if user_id is not None:
            print("user_id_for_session_id should return None if session_id doesn't exist")
            exit(1)

        print("OK", end="")
    except:
        import sys
        print("Error: {}".format(sys.exc_info()))
