"""
important note:
these tests perform correctly only if database is empty
"""
import project
import sqlite3

# project.main() makes the database which is a requirement for other codes
project.main()


def main():
    test_insert_name()
    test_insert_condition()
    test_get_all_names()
    test_insert_med()
    test_get_files()
    test_get_med()
    test_update_name()
    test_update_age()
    test_update_condition()
    test_update_med()
    test_full_file_delete()
    test_condition_delete()
    test_delete_medicine()


def test_insert_name():
    """
    insert_name() is a function that has two parameter, name and age,

    it is designed to stop the user from inputting non integer values for age
    or inputting  non string values for name

    it returns None if wrong input is presented
    it returns 'new file' if inputted name is a new name and not saved in database before
    it returns 'existing file' if inputted name is already in the file
    """
    assert project.insert_name("john", 22) == "new file"
    assert project.insert_name("john", 22) == "existing file"
    assert project.insert_name(1, 1) is None
    assert project.insert_name("abe", "two") is None
    assert project.insert_name(7, "three") is None


def test_insert_condition():
    """
    insert_condition is a function that has two parameters, condition and name,

    it is designed to stop the user from inputting non string/list values for condition
    or inputting a name that is not in the database (this part is only for unit test because you can't do otherwise in gui)
    it does not allow duplicate conditions for the same name

    it returns None if the input for condition is not a str/list
    it returns None if name is not in the database
    it returns False if the condition is already registered under the inputted name
    """

    # make dummy data
    project.insert_name("joe", 2)
    project.insert_name("david", 35)

    assert project.insert_condition("cold", "john") == "cold added"
    assert project.insert_condition("headache", "joe") == "headache added"

    # inputting multiple conditions will turn it into a list of lists
    assert project.insert_condition(["cold", "headache"], "david") == "conditions added"
    assert project.insert_condition(["backache", "cold"], "joe")

    # if name is not in the database
    assert project.insert_condition("headache", "jim") is None

    # if condition already exists
    assert project.insert_condition("cold", "john") is False

    # if condition is not str/list
    assert project.insert_condition(5, "david") is None

    # if name is not str
    assert project.insert_condition("cold", 5) is None


def test_get_all_names():
    """a simple function that gets all the names from database and returns them"""
    assert project.get_all_names() == ["john", "joe", "david"]


def test_insert_med():
    """
    a function that inserts medicine data into database
    it has three parameters, name, condition, med

    it insures that the inputted name is a str/list
    it returns None if input is wrong

    inserting into med table will return the name of the med
    """

    assert project.insert_med("john", "cold", "diphenhydramine") == "diphenhydramine"
    assert project.insert_med("david", "headache", ["codeine", "aspirin"]) == ["codeine", "aspirin"]

    # if inputted med is not str
    assert project.insert_med("david", "headache", 5) is None


def test_get_files():
    """
    a function that has a parameter, name,
    it returns the age related to that name
    plus all the conditions registered under it.
    it insures that inputted name is in the database (again, only added for unit test)
    returns None if wrong input
    """
    assert project.get_files("john") == (22, ["cold"])

    assert project.get_files("david") == (35, ["cold", "headache"])
    project.insert_condition("backache", "david")
    assert project.get_files("david") == (35, ["backache", "cold", "headache"])

    # if name is not in the database
    assert project.get_files("jim") is None


def test_get_med():
    """
    a function that has two parameters, condition and name
    it gets the medicine used for the said condition for the name from database

    it returns a list of the medicine
    """
    assert project.get_med("cold", "john") == ["diphenhydramine"]
    assert project.get_med("headache", "david") == ["codeine", "aspirin"]

    project.insert_med("david", "backache", "yoga")
    assert project.get_med("backache", "david") == ["yoga"]


def test_update_name():
    """
    a function that has two parameters, old_name and new_name
    it changes the old name to new name
    """
    project.insert_name("jan", 26)
    project.update_name("jan", "jane")

    assert project.get_all_names() == ["john", "joe", "david", "jane"]


def test_update_age():
    """
    a function that has two parameters, name and new_age
    it get a name from database and a new input for age
    then updates the age related to that name
    """
    project.update_age("jane", 27)
    assert project.get_files("jane") == (27, [None])


def test_update_condition():
    """
    a function that has three parameters, old_condition and new_condition and name
    it changes the old condition to new condition for the specified name
    """
    project.insert_condition("col", "jane")
    project.update_condition("col", "cold", "jane")
    assert project.get_files("jane") == (27, ["cold"])


def test_update_med():
    """
    a function that has four parameters, name and condition and old_med and new_med
    it changes the old medicine to new medicine for the specified name and condition
    """
    project.insert_med("jane", "cold", "diphenhydramene")
    project.update_med("jane", "cold", "diphenhydramene", "diphenhydramine")
    assert project.get_med("cold", "jane") == ["diphenhydramine"]


def test_full_file_delete():
    """
    a function that has one parameter, name
    it deletes the name and all the data related to it
    it returns a string saying that the file deleted
    """
    # to check if full delete was successful we need to connect to database
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    # get the id of the name from database
    get_id = cur.execute("SELECT id FROM Person WHERE name = ?", ("jane",)).fetchone()[0]

    # get the id of all the conditions that name has
    con_id = cur.execute(
        "SELECT id FROM Condition WHERE person_id = ?", (get_id,)
    ).fetchall()

    assert project.full_file_delete("jane") == "file deleted"

    # name isn't in the database anymore
    assert project.get_all_names() == ["john", "joe", "david"]
    assert cur.execute("SELECT id FROM Person WHERE name = ?", ("jane",)).fetchone() is None

    # no condition registered under the id of the deleted name
    assert cur.execute("SELECT id FROM Condition WHERE person_id = ?", (get_id,)).fetchall() == []

    # flatten the list of lists to a list, we got this data a few lines above
    con_id = [val for i in con_id for val in i]
    # loop over the condition id and see if the medicine related to them are still available
    for c in con_id:
        assert cur.execute("SELECT medicine FROM Medicine WHERE condition_id = ?", (c,)).fetchone() is None

    cur.close()
    con.close()


def test_condition_delete():
    """
    a function that has two parameters, name and condition
    it deletes the specified condition related to the specified name
    plus all the medicine registered under that condition
    it returns a string saying that the condition deleted
    """
    # make a mock example
    project.insert_name("jane", 26)
    project.insert_condition(["cold", "headache"], "jane")
    project.insert_med("jane", "cold", "diphenhydramine")

    # get sql connection
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    # get id of condition for further check
    name_id = cur.execute("SELECT id FROM Person WHERE name = ?", ("jane",)).fetchone()[0]
    con_id = cur.execute(
        "SELECT id FROM Condition WHERE condition = ? AND person_id = ?",
        ("cold", name_id),
    ).fetchone()[0]

    assert project.get_files("jane") == (26, ["cold", "headache"])
    assert project.get_med("cold", "jane") == ["diphenhydramine"]
    assert project.condition_delete("jane", "cold") == "condition deleted"
    assert project.get_files("jane") == (26, ["headache"])

    # checking if the medicine is deleted as well
    assert cur.execute(
        "SELECT medicine FROM Medicine WHERE condition_id = ?", (con_id,)
    ).fetchall() == []


def test_delete_medicine():
    """
    a function that has three parameters, name and condition and med
    it deletes the specified med that is related to the specified condition for the name
    it returns a string saying that the medicine deleted
    """
    project.insert_med("jane", "headache", ["codeine", "aspirin"])
    assert project.get_med("headache", "jane") == ["codeine", "aspirin"]

    assert project.delete_medicine("jane", "headache", "codeine") == "medicine deleted"
    assert project.get_med("headache", "jane") == ["aspirin"]


if __name__ == '__main__':
    main()
