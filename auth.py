import hashlib
from db import connection, cursor


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password, role):

    if not username or not password or not role:
        return False

    try:

        hashed_password = hash_password(password)

        query = """
        INSERT INTO users (username, hashed_password, role)
        VALUES (%s, %s, %s)
        """

        values = (username, hashed_password, role)

        cursor.execute(query, values)
        connection.commit()

        return True

    except Exception as e:
        print("Error:", e)
        return False

def login_user(username, password):

    hashed_password = hash_password(password)

    query = """
    SELECT * FROM users
    WHERE username = %s
    AND hashed_password = %s
    """

    values = (username, hashed_password)

    cursor.execute(query, values)

    user = cursor.fetchone()

    return user