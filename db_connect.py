from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser

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
def _send_query_none(query):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def _send_query_one(query):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        res  = cursor.fetchone()[0]
        return res   
    
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
def _send_query_all(query):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        res  = cursor.fetchall()
        return res        
    
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    

def search_id_name(table, id):
    try:
        query = "SELECT name FROM " + table + " WHERE id = " + id
        res_all = _send_query_one(query)
        return res_all
    except Error as e:
        print(e)

def query_name_num(table, fach):
    try:
        query = "SELECT name, "+ int_to_fach_amount(fach) + " FROM " + table
        print(query)
        res = _send_query_all(query)
        print(res)
        return res
    except Error as e:
        print(e)
def insert_row(table, fach, fach_amount, name, email):
    query = "INSERT INTO " + table + "(name,email,fach_"+ str(fach) +"," + int_to_fach_amount(fach)+") " \
            "VALUES(%s,%s,%s,%s)"
    args = ( name, email,'0',str(fach_amount))
    print(query % args)
    query = query % args
    try:
        _send_query_none(query)
    except Error as error:
        print(error)
def update_row(table, id, fach, fach_amount):
    query = "UPDATE " + table +" SET "+ int_to_fach_amount(fach) +" = " + str(fach_amount) + " WHERE id = " + str(id)
    print(query)
    try:
        _send_query_none(query)

    except Error as error:
        print(error)
def delete_row(table,id):
    query = "DELETE FROM "+ table +" WHERE id =" + str(id)
    try:
        _send_query_none(query)
    except Error as error:
        print(error)
def show_tables():
    query = "Show Tables;"
    try:
        res_all = _send_query_all(query)
        res = []
        for x in res_all:
            res.append(x[0])
        # accept the change
        return list(res)
        
    except Error as error:
        print(error)
def get_fach_amount_by_id(table, id):
    try:
        query = "SELECT fach_1_amount FROM "+ table + " WHERE id = "+ str(id)
        res = _send_query_one(query)
        return res
    except Error as e:
        print(e)
def _get_faecher(table):
    try:
        query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + table + "'"
        res = _send_query_all(query)
        ls = []
        for elm in res:
          ls.append(elm[0]) 
        return ls
    
    except Error as e:
        print(e)
def get_fach_name(table, column_name):
    try:
        query = "SELECT "+ column_name +" FROM "+ table +" WHERE id = 1"
        res = _send_query_one(query) 
        return res
    except Error as e:
        print(e)
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
    print(connect())