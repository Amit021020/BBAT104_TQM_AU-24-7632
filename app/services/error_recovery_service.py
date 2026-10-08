from app.database.db import get_connection


def run_database_operation(operation, *args):
    conn = get_connection()

    try:
        result = operation(conn, *args)

        conn.commit()

        return {
            "success": True,
            "result": result,
            "error": None,
        }

    except Exception as error:
        conn.rollback()

        return {
            "success": False,
            "result": None,
            "error": str(error),
        }

    finally:
        conn.close()


def handle_database_error(error):
    return {
        "success": False,
        "message": "Database operation failed.",
        "error": str(error),
    }