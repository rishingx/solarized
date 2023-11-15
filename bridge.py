#========== IMPORT ==========#

import mariadb

#========== GLOBALS ==========#

host = "localhost"
user = "rishi"
passwd = "rishi123"
database = "grid"

#========== CONNECTION FUNCTIONS ==========#

def connect():
    global mycon, cur
    mycon = mariadb.connect(host=host, user=user, passwd=passwd, database=database)
    if mycon.is_connected():
        cur = mycon.cursor()
    else:
        print("Error connecting...")

def disconnect():
    mycon.close()

#========== TABLE FUNCTIONS ==========#

def create_tables():
    cur.execute("create table if not exists houses (acc integer primary key, name char(20) not null, ph bigint not null, rate integer not null);")
    mycon.commit()

#========== DATA HANDLING ==========#

def add_house(acc, name, ph, rate):
    cur.execute("insert into houses values({}, '{}', {}, {})".format(acc, name, ph, rate))
    mycon.commit()

def get_houses(col="*"):
    cur.execute("select %s from houses" % col)
    return cur.fetchall()

def remove_house(acc):
    cur.execute("delete from houses where acc = %s" % acc)
    mycon.commit()

def remove_all():
    cur.execute("delete from houses;")
    mycon.commit()

#========== OTHER FUNCTIONS ==========#

def search_house(col, query):
    cur.execute("select * from houses where {} like \"%{}%\"".format(col, query))
    return cur.fetchall()
