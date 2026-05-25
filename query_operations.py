from db import connection, cursor
from datetime import datetime
import re

def validate_email(email):

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(pattern, email)


def validate_mobile(mobile):

    return mobile.isdigit() and len(mobile) == 10

def insert_query(
    mail_id,
    mobile_number,
    query_heading,
    query_description
):

    # EMPTY VALIDATION
    if (
        not mail_id or
        not mobile_number or
        not query_heading or
        not query_description
    ):

        return "All fields are required"

    # EMAIL VALIDATION
    if not validate_email(mail_id):

        return "Invalid Email Format"

    # MOBILE VALIDATION
    if not validate_mobile(mobile_number):

        return "Mobile Number must contain 10 digits"

    try:

        query = """
        INSERT INTO queries
        (
            mail_id,
            mobile_number,
            query_heading,
            query_description,
            status,
            query_created_time
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            mail_id,
            mobile_number,
            query_heading,
            query_description,
            "Open",
            datetime.now()
        )

        cursor.execute(query, values)

        connection.commit()

        return "Success"

    except Exception as e:

        print("Error:", e)

        return "Database Error"

def get_all_queries():

    query = """
    SELECT * FROM queries
    ORDER BY query_created_time DESC
    """

    cursor.execute(query)

    return cursor.fetchall()


def close_query(query_id):

    try:

        query = """
        UPDATE queries
        SET
            status = %s,
            query_closed_time = %s
        WHERE query_id = %s
        """

        values = (
            "Closed",
            datetime.now(),
            query_id
        )

        cursor.execute(query, values)

        connection.commit()

        return True

    except Exception as e:

        print("Error:", e)

        return False