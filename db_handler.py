import sqlite3
#connect to database table 
db = sqlite3.connect('test.db')

cursor = db.cursor()

db.execute("DROP TABLE IF EXISTS Hashes")
db.execute("DROP TABLE IF EXISTS Collisions")
db.execute("DROP TABLE IF EXISTS Vertex")
db.commit()

try:
    db.execute("CREATE TABLE Hashes(HASH_VAL TEXT PRIMARY KEY NOT NULL, MSG TEXT NOT NULL, fk_TAG INTEGER NOT NULL);")
    db.commit()
except sqlite3.OperationalError:
    print("Table Coudn't be created")


try:
    db.execute("CREATE TABLE Collisions(MSG TEXT NOT NULL, fk_HASH_VAL TEXT NOT NULL, fk_TAG INTEGER NOT NULL);")
    db.commit()
except sqlite3.OperationalError:
    print("Table Coudn't be created")


try:
    db.execute("CREATE TABLE Vertex(TAG INTEGER PRIMARY KEY NOT NULL, IV TEXT NOT NULL);")
    db.commit()
except sqlite3.OperationalError:
    print("Table Coudn't be created")



##generate hashes

def get_collisions(hash_val):
    try:
        return cursor.execute("SELECT Hash_Val, fk_TAG FROM Hashes WHERE Hash_Val= '{}'".format(hash_val))
    except:
        print("coudn't retrieve data")

def insert_hash(hash_val, msg, TAG):
    db.execute("INSERT INTO Hashes (Hash_Val, MSG, fk_TAG) VALUES ('{}', '{}', '{}')".format(hash_val, msg, TAG))
    db.commit()
    
def insert_vertex(TAG, IV):
    db.execute("INSERT INTO Vertex (TAG, IV) VALUES ('{}', '{}')".format(TAG, IV))
    db.commit()


def insert_collision(msg, hash_val, TAG):
    db.execute("INSERT INTO Collisions (MSG,fk_Hash_Val, fk_TAG) VALUES ('{}', '{}', '{}')".format(msg, hash_val, TAG))
    db.commit()


