import sqlite3


def make_db():
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS Person(id INTEGER PRIMARY KEY NOT NULL, name VARCHAR, age INT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Condition(person_id INTEGER NOT NULL, condition TEXT,"
        " FOREIGN KEY(person_id) REFERENCES Person(id))")

    cur.close()
    con.close()


def insert_name(name, age):
    # start the database connection
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    # check if the person's name already exists
    check_id = cur.execute("SELECT id FROM Person WHERE name = ?", (name,))

    # if it's a new file, make it
    if check_id.fetchone() is None:
        cur.execute("INSERT INTO Person(name, age) VALUES(?, ?)", (name, age))
        con.commit()
        saved_data = "new file"
    else:
        saved_data = "new condition"

    cur.close()
    con.close()

    return saved_data


def insert_condition(condition, name):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    # get the id of the person's file in 'person' table to add to 'condition' table
    get_id = cur.execute("SELECT id FROM Person WHERE name = ?", (name,)).fetchone()[0]

    # if we have only one condition
    if isinstance(condition, str):
        # check if the condition is already in the file or not
        repeated_con = cur.execute("SELECT person_id FROM Condition WHERE condition = ? AND person_id = ?", (condition, get_id))

        # check_id is the id we got to check if the person has a file in database or not
        if repeated_con.fetchone() is None:
            cur.execute("INSERT INTO Condition VALUES(?, ?)", (get_id, condition))
            con.commit()

            # close the connection
            cur.close()
            con.close()

        else:
            cur.close()
            con.close()
            # if this condition already exists in the file
            return False

    # if we have more than one condition
    else:
        # flatten condition from a list of lists into a list
        condition = [val for c in condition for val in c]

        # loop over condition
        for c in condition:
            # see if each condition is already in the file or not
            repeated_con = cur.execute("SELECT person_id FROM Condition WHERE condition = ? AND person_id = ?", (c, get_id))
            # if condition is not in the file, insert it
            if repeated_con.fetchone() is None:
                cur.execute("INSERT INTO Condition VALUES(?, ?)", (get_id, c))
            con.commit()

        # close the connection
        cur.close()
        con.close()

    return True


# get all the names to show in the app
def get_all_names():
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    # flattening the list of tuples into a list cause combobox had a bug with words that have space in them in tuples
    names = [val for n in cur.execute("SELECT name FROM Person").fetchall() for val in n]

    cur.close()
    con.close()

    return names


# get the file for the selected person
def get_files(name):
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    age = cur.execute("SELECT age FROM Person WHERE name =?", (name,)).fetchone()[0]

    files = cur.execute("SELECT condition FROM Person LEFT JOIN Condition "
                        "ON Person.id = Condition.person_id WHERE name = ?", (name,)).fetchall()
    return age, files


# update a name
def update_name(old_name, new_name):
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    get_id = cur.execute("SELECT id FROM Person WHERE name = ?", (old_name,)).fetchone()[0]

    cur.execute("UPDATE Person SET name = ? WHERE id = ?", (new_name, get_id))
    con.commit()

    cur.close()
    con.close()


# update age
def update_age(name, new_age):
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    cur.execute("UPDATE Person SET age = ? WHERE name = ?", (new_age, name))
    con.commit()

    cur.close()
    con.close()


# update a condition
def update_condition(old_condition, new_condition, name):
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    get_id = cur.execute("SELECT id FROM Person WHERE name = ?", (name,)).fetchone()[0]

    cur.execute("UPDATE Condition SET condition = ? WHERE condition = ? AND person_id = ?", (new_condition, old_condition, get_id))
    con.commit()

    cur.close()
    con.close()


# delete the file completely
def full_file_delete(name):
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    get_id = cur.execute("SELECT id FROM Person WHERE name = ?", (name,)).fetchone()[0]

    cur.execute("DELETE FROM Person WHERE name = ?", (name,))
    cur.execute("DELETE FROM Condition WHERE person_id = ?", (get_id,))
    con.commit()

    cur.close()
    con.close()

    return "file deleted"

# delete a condition
def condition_delete(name, condition):
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    get_id = cur.execute("SELECT id FROM Person WHERE name = ?", (name,)).fetchone()[0]
    cur.execute("DELETE FROM Condition WHERE person_id = ? AND condition = ?", (get_id, condition))
    con.commit()

    cur.close()
    con.close()

    return "condition deleted"
