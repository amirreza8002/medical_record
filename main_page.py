import tkinter as tk
from tkinter import ttk, Tk
from tkinter.messagebox import showinfo
from ctypes import windll
import sql_funcs
import pyttsx3

windll.shcore.SetProcessDpiAwareness(1)

# start the app
root = Tk()
root.title("medical record")
root.resizable(0, 0)

# set up the voice to speach
engine = pyttsx3.init()
engine.setProperty("rate", 170)


def main():
    root.geometry("320x300")
    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", padx=10)

    # make a database
    sql_funcs.make_db()

    # opens the page where you can add new files
    def open_add_page():
        main_frame.destroy()
        adding_page()

    # opens the page where you can see the files
    def open_file_page():
        main_frame.destroy()
        open_file()

    def open_e_d_page():
        main_frame.destroy()
        edit_delete_page()

    ttk.Label(main_frame, text="welcome").pack()
    ttk.Label(main_frame, text="add a new file or condition").pack()

    # the button that gets you to adding new file page
    add_button = ttk.Button(main_frame, text="add a new file/condition", command=open_add_page)
    add_button.pack(pady=(5, 10))

    ttk.Separator(main_frame, orient="horizontal").pack(fill="x")

    ttk.Label(main_frame, text="see an existing file").pack(pady=(10, 10))

    # a button that gets you to see the file page
    open_button = ttk.Button(main_frame, text="see an existing file", command=open_file_page)
    open_button.pack(pady=(0, 10))

    ttk.Separator(main_frame, orient="horizontal").pack(fill="x")

    ttk.Label(main_frame, text="delete a file/condition").pack(pady=(10, 10))

    # a button to a page for editing/deleting
    edit_delete_button = ttk.Button(main_frame, text="Edit/Delete", command=open_e_d_page)
    edit_delete_button.pack()


main()


# the page where you can add new files
def adding_page():
    root.geometry("350x400")
    adding_frame = ttk.Frame(root, height=400, width=350)
    adding_frame.pack(fill="both", padx=10)

    # go back to main page
    def back_button():
        adding_frame.destroy()
        main()

    # save the new info
    def save_info():
        name = name_var.get()
        age = age_var.get()
        condition = condition_var.get()

        # check that the data isn't empty
        if len(name) <= 0 or len(age) <= 0 or len(condition) <= 0:
            showinfo(title="error", message="please input the data")
            return

        # check that age is a number
        if age.isnumeric():
            age = int(age)
        else:
            age_label["text"] = "please use numbers for age"
            age_label["foreground"] = "red"
            return

        # check if condition is in the right format
        if ", " in condition:
            conditions = [condition.split(", ")]
            # call sql with a list of conditions
            # insert name and age
            save_file = sql_funcs.insert_name(name, age)

            # insert a list of conditions
            save_condition = sql_funcs.insert_condition(conditions, name)

            saving_info(save_file, save_condition)

        elif "," in condition:
            condition_label["text"] = "please use comma and a space afterwards"
            condition_label["foreground"] = "red"
            return

        else:
            # if none of the if and elifs work, call sql normally
            # insert age and name and check if file already exists or it's new
            save_file = sql_funcs.insert_name(name, age)
            # insert conditions and check if they are new or not
            save_condition = sql_funcs.insert_condition(condition, name)

            saving_info(save_file, save_condition)

    # function that tells you if the saving worked or not
    def saving_info(save_file, save_condition):
        if save_file == "new file":
            showinfo(title="saved", message="saved the data")

        # if file already existed:
        elif save_file == "new condition":
            # if condition was saved successfully:
            if save_condition:
                showinfo(title="added", message="added data to existing file")
            else:
                # if this person's file already has this condition in it:
                showinfo(title="file exists", message="this condition is already in this file")
                return

        # reloading the page and cleaning it
        adding_frame.destroy()
        adding_page()

    # the button that gets you to main page
    ttk.Button(adding_frame, text="<", command=back_button, width=5, takefocus=1).pack(pady=(2, 5), anchor="w")

    ttk.Label(adding_frame, text="adding a new file/condition").pack(pady=(0, 15))

    # getting the name
    ttk.Label(adding_frame, text="please enter/choose the name").pack(pady=(0, 7))

    # get all the names from database to show for selection
    names_list = sql_funcs.get_all_names()

    name_var = tk.StringVar()
    name_combo = ttk.Combobox(adding_frame, textvariable=name_var, values=names_list)
    name_combo.pack(pady=(0, 10))

    # separator
    ttk.Separator(adding_frame, orient="horizontal").pack(fill="x")

    # getting the age
    age_label = ttk.Label(adding_frame, text="please enter the age (with numbers)")
    age_label.pack(pady=(10, 7))

    age_var = tk.StringVar()
    age_entry = ttk.Entry(adding_frame, textvariable=age_var)
    age_entry.pack(pady=(0, 10))

    # separator
    ttk.Separator(adding_frame, orient="horizontal").pack(fill="x", pady=(0, 10))

    # get the condition(s)
    ttk.Label(adding_frame, text="please enter/choose the condition(s)").pack()
    condition_label = ttk.Label(adding_frame, text="separate with a comma and a space (, )")
    condition_label.pack(pady=(3, 7))

    condition_var = tk.StringVar()
    condition_entry = ttk.Entry(adding_frame, textvariable=condition_var)
    condition_entry.pack()

    # save the information
    save_button = ttk.Button(adding_frame, text="save", command=save_info)
    save_button.pack(pady=(15, 0))


# the page where you can see the files
def open_file():
    root.geometry("350x250")
    opening_frame = ttk.Frame(root, height=250, width=250)
    opening_frame.pack(fill="both", padx=10)

    # go back to main page
    def back_button():
        opening_frame.destroy()
        main()

    # open the file and see the content
    def opening_file():
        if len(selected_name.get()) > 0:
            db_age, db_file = sql_funcs.get_files(selected_name.get())
            opening_frame.destroy()
            see_file(db_age, selected_name.get(), db_file)

    # the button that gets you back to main page
    ttk.Button(opening_frame, text="<", width=5, command=back_button).pack(pady=(2, 10), anchor="w")

    ttk.Label(opening_frame, text="select the person's name").pack(pady=(0, 10))

    # get all the names from database for selection
    names_list = sql_funcs.get_all_names()

    # chose a name
    selected_name = tk.StringVar()
    chose_name = ttk.Combobox(opening_frame, textvariable=selected_name, state="readonly", values=names_list)
    chose_name.pack()

    # see the info
    see_button = ttk.Button(opening_frame, text="open file", command=opening_file)
    see_button.pack(pady=(15, 0))


# a text widget that shows you the files and has a text to voice too
def see_file(file_age, file_name, file):
    root.geometry("600x600")
    text_frame = ttk.Frame(root, height=600, width=600)
    text_frame.pack()

    # go back one page
    def back_button():
        text_frame.destroy()
        open_file()

    # the button that gets you back a page
    tk.Button(text_frame, text="<", width=5, border=2, command=back_button).pack(anchor="w", pady=3, padx=10)

    # text widget that shows you the files
    record_text = tk.Text(text_frame, height=25, border=5)
    record_text.pack()

    # insert a header into the text saying name and age of the person
    record_text.insert(1.0, f"name: {file_name}, age: {file_age}\nconditions:\n")
    # loop over the conditions and insert them on separate lines
    for i, conditions in enumerate(file):  # enumerate is for testing another possibility
        record_text.insert(f"{i+3}.0", f"{conditions[0]}\n")

    # disable the text so user can't alter it
    record_text["state"] = "disabled"

    # text to voice function
    def text_to_speach():
        engine.say(record_text.get(1.0, "end"))
        engine.runAndWait()

    # text to speach button
    tk.Button(text_frame, text="hear the text", border=3, command=text_to_speach).pack(side="left", pady=(7, 5))


# edit a file like updating something or correcting typos, etc...
# deleting a file deletes everything on it, or deleting a certain condition
def edit_delete_page():
    root.geometry("352x250")
    edit_delete_frame = ttk.Frame(root)
    edit_delete_frame.pack(fill="both", padx=10)

    # go back to main page
    def back_button():
        edit_delete_frame.destroy()
        main()

    # open the page for editing
    def open_edit_page():
        edit_delete_frame.destroy()
        edit_page()

    # open the page for deleting
    def open_delete_page():
        edit_delete_frame.destroy()
        del_page()

    # back button
    tk.Button(edit_delete_frame, text="<", width=5, border=2, command=back_button).pack(anchor="w", pady=3, padx=10)

    ttk.Label(edit_delete_frame, text="Edit a file (update a condition, correct a typo, etc)").pack(pady=10)

    # button to go to edit page
    edit_button = ttk.Button(edit_delete_frame, text="Edit files", command=open_edit_page)
    edit_button.pack(pady=(0, 10))

    ttk.Separator(edit_delete_frame, orient="horizontal").pack(fill="x")

    ttk.Label(edit_delete_frame, text="Delete a file or a condition").pack(pady=10)

    # button to go to delete page
    delete_button = ttk.Button(edit_delete_frame, text="Delete files/conditions", command=open_delete_page)
    delete_button.pack()


# the page to edit files
def edit_page():
    root.geometry("400x400")
    edit_frame = ttk.Frame(root)
    edit_frame.pack(fill="both")

    def back_button():
        edit_frame.destroy()
        edit_delete_page()

    def edit_name():
        if len(selected_name.get()) > 0:
            edit_frame.destroy()
            edit_name_page(selected_name.get())

    def edit_age():
        if len(selected_name.get()) > 0:
            edit_frame.destroy()
            edit_age_page(selected_name.get())

    def edit_condition():
        if len(selected_name.get()) > 0:
            edit_frame.destroy()
            edit_condition_page(selected_name.get())

    # back button
    tk.Button(edit_frame, text="<", width=5, border=2, command=back_button).pack(anchor="w", pady=3, padx=10)

    # get the names
    names_list = sql_funcs.get_all_names()

    ttk.Label(edit_frame, text="choose a name and proceed").pack(pady=10)

    # chose a name
    selected_name = tk.StringVar()
    chose_name = ttk.Combobox(edit_frame, textvariable=selected_name, state="readonly", values=names_list)
    chose_name.pack()

    ttk.Label(edit_frame, text="choose a name and edit it (for misspell and...)").pack(pady=10)
    # button to go to the page to edit the name
    name_button = ttk.Button(edit_frame, text="edit the name", command=edit_name)
    name_button.pack(pady=10)

    ttk.Separator(edit_frame, orient="horizontal").pack(fill="x")

    ttk.Label(edit_frame, text="choose the name then edit it's age").pack(pady=10)
    # button to go the page to change the age
    age_button = ttk.Button(edit_frame, text="edit the age", command=edit_age)
    age_button.pack(pady=(0, 10))

    ttk.Separator(edit_frame, orient="horizontal").pack(fill="x")

    ttk.Label(edit_frame, text="choose the name and edit one it's conditions").pack(pady=10)
    # button to go to the page to edit a condition
    condition_button = ttk.Button(edit_frame, text="edit a condition", command=edit_condition)
    condition_button.pack(pady=10)


def edit_name_page(old_name):
    root.geometry("300x250")
    edit_name_frame = ttk.Frame(root)
    edit_name_frame.pack(fill="both")

    def back_button():
        edit_name_frame.destroy()
        edit_page()

    def save_name():
        if len(new_name.get()) > 1:
            sql_funcs.update_name(old_name, new_name.get())
            showinfo(title="name change", message="name updated")
            edit_name_frame.destroy()
            edit_page()

    # back button
    tk.Button(edit_name_frame, text="<", width=5, border=2, command=back_button).pack(anchor="w", pady=3, padx=10)

    ttk.Label(edit_name_frame, text="the name you are changing is: ").pack(pady=(10, 0))
    ttk.Label(edit_name_frame, text=f"{old_name}", foreground="red").pack(pady=(0, 20))

    ttk.Separator(edit_name_frame, orient="horizontal").pack(fill="x")


    ttk.Label(edit_name_frame, text="enter the new name:").pack(pady=10)
    # get the new name
    new_name = tk.StringVar()
    get_name = ttk.Entry(edit_name_frame, textvariable=new_name)
    get_name.pack()

    # save the new name
    save_button = ttk.Button(edit_name_frame, text="Save", command=save_name)
    save_button.pack(pady=15)


def edit_age_page(name):
    root.geometry("300x250")
    edit_age_frame = ttk.Frame(root)
    edit_age_frame.pack(fill="both")

    def back_button():
        edit_age_frame.destroy()
        edit_page()

    def save_age():
        if new_age.get().isnumeric():
            sql_funcs.update_age(name, new_age.get())
            showinfo(title="age changed", message="age updated")
            edit_age_frame.destroy()
            edit_page()

    # back button
    tk.Button(edit_age_frame, text="<", width=5, border=2, command=back_button).pack(anchor="w", pady=3, padx=10)

    # get the old age to display
    old_age, _ = sql_funcs.get_files(name)

    # showing the info user is trying to change
    ttk.Label(edit_age_frame, text="the age you are changing is: ").pack(pady=(10, 0))
    ttk.Label(edit_age_frame, text=f"{old_age}", foreground="red").pack(pady=(0, 20))

    ttk.Separator(edit_age_frame, orient="horizontal").pack(fill="x")

    ttk.Label(edit_age_frame, text="enter the new age:").pack(pady=10)
    # new age
    new_age = tk.StringVar()
    get_age = ttk.Entry(edit_age_frame, textvariable=new_age)
    get_age.pack()

    save_button = ttk.Button(edit_age_frame, text="Save", command=save_age)
    save_button.pack(pady=15)


def edit_condition_page(name):
    root.geometry("300x250")
    edit_condition_frame = ttk.Frame(root)
    edit_condition_frame.pack(fill="both")

    def back_button():
        edit_condition_frame.destroy()
        edit_page()

    def save_condition():
        if len(selected_condition.get()) > 1 and len(new_condition.get()) > 1:
            sql_funcs.update_condition(selected_condition.get(), new_condition.get(), name)
            showinfo(title="condition changed", message="condition updated")
            edit_condition_frame.destroy()
            edit_page()

    # back button
    tk.Button(edit_condition_frame, text="<", width=5, border=2, command=back_button).pack(anchor="w", pady=5, padx=10)

    # get the conditions
    _, conditions = sql_funcs.get_files(name)

    ttk.Label(edit_condition_frame, text="select the condition you want to update").pack()
    # select the condition you want to update
    selected_condition = tk.StringVar()
    chose_condition = ttk.Combobox(edit_condition_frame, textvariable=selected_condition, state="readonly", values=conditions)
    chose_condition.pack(pady=(5, 15))

    ttk.Separator(edit_condition_frame, orient="horizontal").pack(fill="x")

    ttk.Label(edit_condition_frame, text="enter the new condition:").pack(pady=(15, 5))
    # new condition
    new_condition = tk.StringVar()
    get_condition = ttk.Entry(edit_condition_frame, textvariable=new_condition)
    get_condition.pack()

    # save button
    save_button = ttk.Button(edit_condition_frame, text="Save", command=save_condition)
    save_button.pack(pady=15)


# the page that deletes files or conditions
def del_page():
    root.geometry("360x300")
    del_frame = ttk.Frame(root)
    del_frame.pack(fill="both", padx=10)

    # button command: go to main page
    def back_button():
        del_frame.destroy()
        edit_delete_page()

    # a function that works if an option was selected
    def option_selected():
        # check if user wants to delete a condition or a file
        if selected_option.get() == "condition":
            # if user wants to delete a condition, activate the combobox for selection
            condition_options["state"] = "readonly"

        # if user wants to delete a file, disable the combobox for 'condition'
        else:
            condition_options["state"] = "disabled"

    # get data to put in the combobox for 'condition'
    def file_selected(event=None):
        # check if a name was selected
        if len(chosen_name.get()) > 1:
            # get the data that belongs to the chosen name
            a, c = sql_funcs.get_files(chosen_name.get())
            # delete the age
            del a

            # put the conditions in the combobox
            condition = [val for t in c for val in t]
            condition_options["values"] = condition

    # if delete button is clicked, check if it should delete a file or a condition then call the right deleting function
    def delete_fuc():
        if selected_option.get() == "file":
            delete_file()
        elif selected_option.get() == "condition":
            delete_condition()

    # delete the file, if deleting file is selected
    def delete_file():
        del_info = sql_funcs.full_file_delete(chosen_name.get())
        if del_info == "file deleted":
            del_frame.destroy()
            showinfo(title="deleted file", message="your file has been deleted")
            del_page()

    def delete_condition():
        del_info = sql_funcs.condition_delete(chosen_name.get(), chosen_condition.get())
        if del_info == "condition deleted":
            del_frame.destroy()
            showinfo(title="deleted condition", message="your file has been updated")
            del_page()

    tk.Button(del_frame, text="<", width=5, border=2, command=back_button).pack(anchor="w", pady=3, padx=10)

    # just a label
    ttk.Label(del_frame, text="delete a file or delete a condition in a file").pack(anchor="w", pady=15)

    # radiobuttons for deciding if we are deleting a file or a condition
    selected_option = tk.StringVar()
    # first radiobutton (delete a file)
    del_option1 = ttk.Radiobutton(del_frame, text="delete a file", value="file", variable=selected_option, command=option_selected)
    del_option1.pack(anchor="w", pady=(5, 5))

    # second radiobutton (delete a condition)
    del_option2 = ttk.Radiobutton(del_frame, text="delete a condition", value="condition", variable=selected_option, command=option_selected)
    del_option2.pack(anchor="w")

    # get all the names we have in database
    names_list = sql_funcs.get_all_names()

    # a combobox that gets all the names from database and shows the user for choosing
    chosen_name = tk.StringVar()
    name_options = ttk.Combobox(del_frame, textvariable=chosen_name, state="readonly", values=names_list)
    name_options.pack(pady=10)

    # when a name is chosen, a function is called that gets all the conditions related to that name
    name_options.bind("<<ComboboxSelected>>", file_selected)

    # -------
    ttk.Separator(del_frame, orient="horizontal").pack(fill="x")

    # a combobox that show the conditions to user, default to disabled
    chosen_condition = tk.StringVar()
    condition_options = ttk.Combobox(del_frame, textvariable=chosen_condition, state="disable")
    condition_options.pack(pady=(0, 10))

    delete_button = ttk.Button(del_frame, text="delete", command=delete_fuc)
    delete_button.pack(anchor="s", pady=10)


root.mainloop()
