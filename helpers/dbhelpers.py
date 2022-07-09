import mariadb
from dbcreds import *

def connect_db():
    conn=None
    cursor=None

    try:
        conn= mariadb.connect(host=host,port=port,database=database,user=user, password=password)
        cursor = conn.cursor()
        return (conn, cursor)
    except mariadb.OperationalError as e:
        print("Got an operational error")
        if ("Access denied" in e.msg):
            print("Failed to log in")
        disconnect_db()
    


def disconnect_db(conn,cursor):
    if (cursor != None):
        cursor.close()
    if (conn != None):
        conn.rollback()
        conn.close()
    

def run_query(statement, args=[]):
    try:
        (conn, cursor) = connect_db()
        if statement.startswith("SELECT"):
            cursor.execute(statement, args)
            result = cursor.fetchall()
            return result
        else:
            cursor.execute(statement,args)
            if cursor.rowcount == 1:
                conn.commit()
                print("Query successful")
            else:
                print("Query failed")
            
    except mariadb.OperationalError as e:
        print("Got an operational error")
        if ("Access denied" in e.msg):
            print("Failed to log in")

    except mariadb.IntegrityError as e:
        print("Integrity error")

    except mariadb.ProgrammingError as e:
        if ("SQL syntax" in e.msg):
            print("SQL syntax error, please try again")
        else:
            print("a different programming error occurred other than SQL syntax")
        print(e.msg)

    except RuntimeError as e:
        print("Caught a runtime error")
        e.with_traceback

    except Exception as e:
        print(e.with_traceback)
        print(e.msg)

    finally:
        disconnect_db(conn,cursor)