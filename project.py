import sqlite3
import graphical_interface

def main():
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS Person(id INTEGER PRIMARY KEY NOT NULL, name VARCHAR, age INT)"
    )

    cur.execute(
        "CREATE TABLE IF NOT EXISTS Condition(person_id INTEGER NOT NULL, condition TEXT,"
        " id INTEGER PRIMARY KEY NOT NULL,"
        " FOREIGN KEY(person_id) REFERENCES Person(id))"
    )

    cur.execute(
        "CREATE TABLE IF NOT EXISTS Medicine(condition_id INTEGER NOT NULL, medicine TEXT,"
        " FOREIGN KEY(condition_id) REFERENCES Condition(id))"
    )

    cur.close()
    con.close()


def insert_name(name, age):
    # start the database connection
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    # there is already a check in gui, this one is for unit test
    if not isinstance(name, str) or not isinstance(age, int):
        return None

    # check if the person's name already exists
    check_id = cur.execute("SELECT id FROM Person WHERE name = ?", (name,))

    # if it's a new file, make it
    if check_id.fetchone() is None:
        cur.execute("INSERT INTO Person(name, age) VALUES(?, ?)", (name, age))
        con.commit()
        saved_data = "new file"
    else:
        saved_data = "existing file"

    cur.close()
    con.close()

    return saved_data


def insert_condition(condition, name):
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    # you have to input str in the gui, but this is for unit test
    if not isinstance(condition, (str, list)) or not isinstance(name, str):
        return None
    else:
        # get the id of the person's file in 'person' table to add to 'condition' table
        get_id = cur.execute("SELECT id FROM Person WHERE name = ?", (name,)).fetchone()

    # you can't input wrong name in the gui, but this is for unit test
    if get_id is None:
        return None

    # if we have only one condition
    if isinstance(condition, str):
        # check if the condition is already in the file or not
        repeated_con = cur.execute(
            "SELECT person_id FROM Condition WHERE condition = ? AND person_id = ?",
            (condition, get_id[0]),
        )

        # check_id is the id we got to check if the person has a file in database or not
        if repeated_con.fetchone() is None:
            cur.execute(
                "INSERT INTO Condition(person_id, condition) VALUES(?, ?)",
                (get_id[0], condition),
            )
            con.commit()

            # close the connection
            cur.close()
            con.close()
            return f"{condition} added"

        else:
            cur.close()
            con.close()
            # if this condition already exists in the file
            return False

    # if we have more than one condition
    elif isinstance(condition, list):
        # flatten condition from a list of lists into a list

        # loop over condition
        for c in condition:
            # see if each condition is already in the file or not
            repeated_con = cur.execute(
                "SELECT person_id FROM Condition WHERE condition = ? AND person_id = ?",
                (c, get_id[0]),
            )
            # if condition is not in the file, insert it
            if repeated_con.fetchone() is None:
                cur.execute(
                    "INSERT INTO Condition(person_id, condition) VALUES(?, ?)",
                    (get_id[0], c),
                )
            con.commit()

        # close the connection
        cur.close()
        con.close()

        return "conditions added"


# get all the names to show in the app
def get_all_names():
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    # flattening the list of tuples into a list cause combobox had a bug with words that have space in them in tuples
    names = [
        val for n in cur.execute("SELECT name FROM Person").fetchall() for val in n
    ]

    cur.close()
    con.close()

    return names


def insert_med(name, condition, med):
    """insert medical condition into medicine table"""
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    # get the id of the name from person table
    get_name_id = cur.execute(
        "SELECT id FROM Person WHERE name = ?", (name,)
    ).fetchone()[0]
    # get the unique id of the condition from condition table
    get_id = cur.execute(
        "SELECT id FROM Condition WHERE person_id = ? AND condition = ?",
        (get_name_id, condition),
    ).fetchone()[0]

    # if only one med input:
    if isinstance(med, str):
        # check if there is already such medicine for the condition in database
        get_repeats = cur.execute(
            "SELECT medicine FROM Medicine WHERE condition_id = ? AND medicine = ?",
            (get_id, med),
        ).fetchone()
        # insert if it's a new filing
        if get_repeats is None:
            cur.execute(
                "INSERT INTO Medicine(condition_id, medicine) VALUES(?, ?)",
                (get_id, med),
            )
            con.commit()
            return med

    # if multiple med input:
    elif isinstance(med, list):
        for m in med:
            # check for repeats
            get_repeats = cur.execute(
                "SELECT medicine FROM Medicine WHERE condition_id = ? AND medicine = ?",
                (get_id, m),
            ).fetchone()
            # insert if new filing
            if get_repeats is None:
                cur.execute(
                    "INSERT INTO Medicine(condition_id, medicine) VALUES(?, ?)",
                    (get_id, m),
                )
                con.commit()
        return med

    else:
        return None

    cur.close()
    con.close()


# get the file for the selected person
def get_files(name):
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    # you can't input wrong name in the gui, but this is for unit test
    get_id = cur.execute("SELECT id FROM Person WHERE name = ?", (name,)).fetchone()
    if get_id is None:
        return None

    age = cur.execute("SELECT age FROM Person WHERE name =?", (name,)).fetchone()[0]

    files = cur.execute(
        "SELECT condition FROM Person LEFT JOIN Condition "
        "ON Person.id = Condition.person_id WHERE name = ?",
        (name,),
    ).fetchall()

    files = [val for c in files for val in c]

    cur.close()
    con.close()
    return age, files


def get_med(condition, name):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    name_id = cur.execute("SELECT id FROM Person WHERE name = ?", (name,)).fetchone()[0]
    con_id = cur.execute(
        "SELECT id FROM Condition WHERE condition = ? AND person_id = ?",
        (condition, name_id),
    ).fetchone()[0]
    meds = cur.execute(
        "SELECT medicine FROM Medicine WHERE condition_id = ?", (con_id,)
    ).fetchall()
    meds = [val for m in meds for val in m]

    cur.close()
    con.close()
    return meds


# update a name
def update_name(old_name, new_name):
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    get_id = cur.execute(
        "SELECT id FROM Person WHERE name = ?", (old_name,)
    ).fetchone()[0]

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

    cur.execute(
        "UPDATE Condition SET condition = ? WHERE condition = ? AND person_id = ?",
        (new_condition, old_condition, get_id),
    )
    con.commit()

    cur.close()
    con.close()


def update_med(name, condition, old_med, new_med):
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    get_id = cur.execute("SELECT id FROM Person WHERE name = ?", (name,)).fetchone()[0]
    con_id = cur.execute(
        "SELECT id FROM Condition WHERE Person_id = ? AND condition = ?",
        (get_id, condition),
    ).fetchone()[0]

    cur.execute(
        "UPDATE Medicine SET medicine = ? WHERE condition_id = ? AND medicine = ?",
        (new_med, con_id, old_med),
    )
    con.commit()

    cur.close()
    con.close()


# delete the file completely
def full_file_delete(name):
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    get_id = cur.execute("SELECT id FROM Person WHERE name = ?", (name,)).fetchone()[0]
    con_id = cur.execute(
        "SELECT id FROM Condition WHERE person_id = ?", (get_id,)
    ).fetchall()
    con_id = [val for i in con_id for val in i]

    # delete the name
    cur.execute("DELETE FROM Person WHERE name = ?", (name,))

    # delete the conditions related to the name
    cur.execute("DELETE FROM Condition WHERE person_id = ?", (get_id,))

    # delete all the medicine for all the conditions related to the name
    for i in con_id:
        cur.execute("DELETE FROM Medicine WHERE condition_id = ?", (i,))
    con.commit()

    cur.close()
    con.close()

    return "file deleted"


# delete a condition
def condition_delete(name, condition):
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    get_id = cur.execute("SELECT id FROM Person WHERE name = ?", (name,)).fetchone()[0]
    con_id = cur.execute(
        "SELECT id FROM Condition WHERE person_id = ?", (get_id,)
    ).fetchone()[0]

    cur.execute(
        "DELETE FROM Condition WHERE person_id = ? AND condition = ?",
        (get_id, condition),
    )
    con.commit()

    cur.execute("DELETE FROM Medicine WHERE condition_id = ?", (con_id,))
    con.commit()

    cur.close()
    con.close()

    return "condition deleted"


def delete_medicine(name, condition, med):
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    get_id = cur.execute("SELECT id FROM Person WHERE name = ?", (name,)).fetchone()[0]
    con_id = cur.execute(
        "SELECT id FROM Condition WHERE person_id = ? AND condition = ?",
        (get_id, condition),
    ).fetchone()[0]
    cur.execute(
        "DELETE FROM Medicine WHERE condition_id = ? AND medicine = ?", (con_id, med)
    )
    con.commit()

    cur.close()
    con.close()

    return "medicine deleted"


if __name__ == "__main__":
    graphical_interface.main()
