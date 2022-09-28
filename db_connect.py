from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser
import string

db_klasse= "klasse_5_d"
def read_db_config(filename='src/config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db
def connect():
    """ Connect to MySQL database """

    db_config = read_db_config()
    conn = None
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('Connection established.')
        else:
            print('Connection failed.')

    except Error as error:
        print(error)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print('Connection closed.')
def query_with_fetchall(table):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM " + table)

        res = cursor.fetchall()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return res
def search_id_name(table, id):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM " + table + " WHERE id = " + id)
        res_all = cursor.fetchone()[0]
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return res_all
def query_name_num(table, fach):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        fach = int_to_fach_amount(fach)
        cursor.execute("SELECT name, "+ fach + " FROM " + table)

        res = cursor.fetchall()
        print(res)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return res
def insert_row(table, fach, fach_amount, name, email):
    query = "INSERT INTO " + table + "(name,email,fach_"+ str(fach) +"," + int_to_fach_amount(fach)+") " \
            "VALUES(%s,%s,%s,%s)"
    args = ( name, email,'0',str(fach_amount))
    print(query % args)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query  % args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
def update_row(table, id, fach, fach_amount):
    # read database configuration
    db_config = read_db_config()
    fach = int_to_fach_amount(fach)
    # prepare query and data
    query = "UPDATE " + table +" SET "+ fach +" = " + str(fach_amount) + " WHERE id = " + str(id)
    print(query)
    try:
        conn = MySQLConnection(**db_config)

        # update book title
        cursor = conn.cursor()
        cursor.execute(query)

        # accept the changes
        conn.commit()

    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
def delete_row(table,id):
    db_config = read_db_config()

    query = "DELETE FROM "+ table +" WHERE id = %s"

    try:
        # connect to the database server
        conn = MySQLConnection(**db_config)

        # execute the query
        cursor = conn.cursor()
        cursor.execute(query, (id,))

        # accept the change
        conn.commit()

    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
def show_tables():
    db_config = read_db_config()

    query = "Show Tables;"

    try:
        # connect to the database server
        conn = MySQLConnection(**db_config)

        # execute the query
        cursor = conn.cursor()
        cursor.execute(query)
        res_all = cursor.fetchall()
        res = []
        for x in res_all:
            res.append(x[0])

        # accept the change
        conn.commit()
        
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
        return list(res)
def get_fach_amount_by_id(table, id):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    try:
        query = "SELECT fach_1_amount FROM "+ table + " WHERE id = "+ str(id)
        print(query)
        cursor.execute(query)
        res  = cursor.fetchone()[0]
    
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        return res
def _get_faecher(table):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    try:
        query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + table + "'"
        cursor.execute(query)
        res  = cursor.fetchall()
        ls = []
        for elm in res:
          ls.append(elm[0]) 
    
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        return ls
def get_fach_name(table, column_name):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    try:
        query = "SELECT "+ column_name +" FROM "+ table +" WHERE id = 1"
        cursor.execute(query)
        res  = cursor.fetchone()[0] 
    
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        return res
def get_faecher_ls(db_klasse):
        ls = []
        for fach in _get_faecher(db_klasse):
            if 'fach_' in fach and 'amount' not in fach:
                ls.append(get_fach_name(db_klasse, fach))
        return list(ls)
def int_to_fach_amount(fach):
    return str("fach_" + str(fach) +"_amount")

def selc_dict(ls, str):
    print(ls['name'])
    newls = []
    for x in range(len(ls)):
        newls.append(ls[x][str])
    return newls


if __name__ == '__main__':
    insert_row(db_klasse, 1 ,1, 'Helga Scholzs', 'bud@wolke7.net')
    print(query_with_fetchall(db_klasse))