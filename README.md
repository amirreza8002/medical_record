# medical_recoed
#### Video Demo:
## Description:

### an overview of the things this app does:
##### medical record is a gui app that saves the medical record of any number of users and displays it to them if they want, edits the data in a file and deletes data.
##### the records may contain a name (must be unique), an age, any number of conditions for each name, and any number of medication for each condition.
##### records can be seen via text and can be heard via a text to voice engine.
##### any part of a record (name, age, condition, medication) can be edited in the page designed for data editing.
##### and user has three delete options: full file delete, condition delete and medicine delete.


### adding data:
##### there is two paged designed for adding new data, a page for making a file, in which the user inputs name, age, and any number of conditions they want (separated with a comma and a space).
##### to lower the complixity of design making file and adding new condition to existing files is done in the same page, which can be updated for better user experience.
##### and a page for adding medication, in which the user chooses a name and a condition and adds any number of medicine related to the specified condition.


### display data:
##### there is two page designed for displaying the saved records to user.
##### a condition page in which user will choose a name and then will see the name, age and all the conditions saved under that name.
##### a medicine page in which the user will choose a name and a condition then will see the name, age, chosen condition and all the medication saved under that condition.
##### there is a button that activates text to voice and reads the file for the user in both pages.


### edit data:
##### in the Edit page, user will choose a name and then select a page for the kind of data that needs editing; there is four pages in total.
##### first page is for editing the name, it simply displays the name chosen, and asks user for a new name
##### second page is for editing age, it displays the age already saved, and asks for a new age.
##### third page is for editing conditions, it asks the user to chose which one of the conditions saved under that name he wants to edit, then asks for a new condition.
##### the fourth page is for editing medications, it asks the user to choose one of the conditions saved under chosen name, and then to choose a medicine saved under that condition, then input a new medicine.


### delete data:
##### in the delete page, user first chooses what kinf of deletation he want to perform, there are three types of deleting: full file delete, condition delete, medicine delete.
##### if the user chooses full file delete, he only inputs a name and all the data saved under that name will be deleted.
##### if the user chooses condition delete, he inputs a name and a condition that is saved under that name and deletes that condition and all the medicine saved under it.
##### if the user chooses medicine delete, he inputs a name and a condition saved under that name and a medicine saved under that condition, then deletes that one data.


## explroing the code
##### medical record project contains four .py , one requirments.txt and one icon.ico files

### .py files:

#### project.py
##### project.py is the main functionality of medical record.
##### it contains all the code running the sql database, from making the database to deleting files, everything is done in this file.
##### the main function of project.py creates the database and is ran as soon as the gui starts running.
##### other functions run when the corresponding buttons are clicked or options have been chosen.


#### test_project.py
##### test_project.py is the unittest of this project.
##### it is designed to check if all the sql queries work properly and only take suitable data.
##### this unit test only works if the databse is empty, due to some test adding, removing and calling data.
##### for the sake of this test, some code has been added to the project.py file, which weren't necessary due to gui design stopping a lot of wrong data being inputted.


#### graphical_interface.py
##### acting as the face of the project, graphical_interface.py is a tkinter based oop code that gives the user an easy interface to work with.
##### due to the nature of this app, using a gui seemed inevitable.
##### but due to the nature of me not being a graphic designer, i have made a simple but easy to use interface so any user can benifit from this kind of app.
##### graphical_interface.py also contains some code that stop the user from inputting wrong or empty data.
##### it also contains the code for the text to voice engine.
##### it might be worth knowing that i first wrote the gui using functions, cause i like functions more and have a better understanding of them. but due to suggestions i changed the code to oop, plus added more stuff that it can do.


#### main.py
##### main.py is simply a excute the project file, it import the graphical_interface.py file and runs it, this action could also be performed by running graphical_interface.py.
##### but i didn't like the idea of running the app through the gui file.


### .ico file
##### icon.ico (i gave it that name) it's just an icon being used inside graphical_interface.py.









