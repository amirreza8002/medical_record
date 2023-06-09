import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, askokcancel, WARNING
from ctypes import windll
import project
import pyttsx3

windll.shcore.SetProcessDpiAwareness(1)


def main():
    # tts is an object of TextToSpeach class, it activates the engine in the background (see line 20)
    tts = TextToSpeach()

    # app is an object of App class, it starts the gui app (see line 32)
    app = App()
    app.mainloop()


class TextToSpeach:
    def __init__(self):
        """initiate the engine for text to speach"""
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)

    def voice_activated(self, texts):
        """activate the voice"""
        self.engine.say(texts)
        self.engine.runAndWait()


class App(tk.Tk):
    """make the root and start the app"""

    def __init__(self):
        super().__init__()

        self.title("medical record")
        self.resizable(False, False)
        self.style = ttk.Style()
        self.style.theme_use("xpnative")
        self.iconbitmap("./icon.ico")

        # make the database
        project.main()

        # make the main page
        main_frame = MainFrame(self)


class MainFrame(ttk.Frame):
    """
    first page of the app
    just a bunch of buttons to go to other pages
    """

    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("320x300")

        self.pack(fill="both", padx=10)

        self.create_widgets()

    def create_widgets(self):
        """buttons to open other pages, instructions on what each button does, and separator lines"""
        welcome = ttk.Label(self, text="welcome")
        welcome.pack(pady=(10, 0))

        inst_1 = ttk.Label(self, text="add a new file or condition")
        inst_1.pack()

        add_button = ttk.Button(
            self, text="add a new file/condition", command=self.open_add_page
        )
        add_button.pack(pady=(5, 10))

        sep_1 = ttk.Separator(self, orient="horizontal")
        sep_1.pack(fill="x")

        inst_2 = ttk.Label(self, text="see an existing file")
        inst_2.pack(pady=(10, 10))

        open_button = ttk.Button(
            self, text="see an existing file", command=self.open_file_page
        )
        open_button.pack(pady=(0, 10))

        sep_2 = ttk.Separator(self, orient="horizontal")
        sep_2.pack(fill="x")

        inst_3 = ttk.Label(self, text="delete a file/condition")
        inst_3.pack(pady=(10, 10))

        edit_delete_button = ttk.Button(
            self, text="Edit/Delete", command=self.open_e_d_page
        )
        edit_delete_button.pack()

    def open_add_page(self):
        """opens a page for adding new data"""
        self.pack_forget()
        adding_page = AddingPage(self.root)

    def open_file_page(self):
        """opens a page for seeing data"""
        self.pack_forget()
        open_file = OpenFile(self.root)

    def open_e_d_page(self):
        """opens a page for editing data"""
        self.pack_forget()
        edit_delete_page = EditDelete(self.root)


class AddingPage(ttk.Frame):
    """a page that instructs on how to add new data"""

    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("270x250")
        self.pack(fill="both", padx=10)

        self.create_widgets()

    def create_widgets(self):
        """
        buttons to go to a page for adding files
        and to go to a page for adding medicine
        """
        self.back_button = ttk.Button(self, text="<", command=self.back_button, width=5)
        self.back_button.pack(pady=(2, 3), anchor="w")

        self.inst_1 = ttk.Label(self, text="add a condition file:")
        self.inst_1.pack()

        self.open_condition_file = ttk.Button(
            self, text="condition file", command=self.open_con_file
        )
        self.open_condition_file.pack(pady=(5, 13))

        sep_1 = ttk.Separator(self, orient="horizontal")
        sep_1.pack(fill="x")

        self.inst_2 = ttk.Label(self, text="add medicine for conditions:")
        self.inst_2.pack(pady=(13, 5))

        self.open_medicine_file = ttk.Button(
            self, text="medicine", command=self.open_medicine
        )
        self.open_medicine_file.pack()

    def back_button(self):
        """a back button to go to previous page"""
        self.pack_forget()
        main_frame = MainFrame(self.root)

    def open_con_file(self):
        """goes to a page to make a file with name, age, condition"""
        self.pack_forget()
        condition_file = ConditionFile(self.root)

    def open_medicine(self):
        """goes to a page to add medication used for a condition"""
        self.pack_forget()
        medicine_file = MedicineFile(self.root)


class ConditionFile(ttk.Frame):
    """
    a page to make new files
    by adding name, age and conditions
    """

    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("360x390")
        self.pack(fill="both", padx=10)

        self.get_data()

    def get_data(self):
        """gets all the names in database to display on a combobox"""
        self.names_list = project.get_all_names()

        self.create_widgets()

    def create_widgets(self):
        """combobox for choosing/adding name, entrys for adding age and condition(s)"""
        self.back_button = ttk.Button(
            self, text="<", command=self.back_button, width=5, takefocus=1
        )
        self.back_button.pack(pady=(2, 5), anchor="w")

        self.intro = ttk.Label(self, text="adding a new file/condition")
        self.intro.pack(pady=(0, 15))

        self.name_label = ttk.Label(self, text="please enter/choose the name")
        self.name_label.pack(pady=(0, 7))

        self.name_var = tk.StringVar()
        self.name_combo = ttk.Combobox(
            self, textvariable=self.name_var, values=self.names_list
        )
        self.name_combo.pack(pady=(0, 10))

        self.sep_1 = ttk.Separator(self, orient="horizontal")
        self.sep_1.pack(fill="x")

        self.age_label = ttk.Label(self, text="please enter the age (with numbers)")
        self.age_label.pack(pady=(10, 7))

        self.age_var = tk.StringVar()
        self.age_entry = ttk.Entry(self, textvariable=self.age_var)
        self.age_entry.pack()

        self.sep_2 = ttk.Separator(self, orient="horizontal")
        self.sep_2.pack(fill="x", pady=10)

        self.inst_1 = ttk.Label(self, text="please enter the condition(s)")
        self.inst_1.pack()
        self.condition_label = ttk.Label(
            self, text="separate with a comma and a space (, )"
        )
        self.condition_label.pack(pady=(3, 7))

        self.condition_var = tk.StringVar()
        self.condition_entry = ttk.Entry(self, textvariable=self.condition_var)
        self.condition_entry.pack()

        self.save_button = ttk.Button(self, text="Save", command=self.save_info)
        self.save_button.pack(pady=(15, 0))

    def back_button(self):
        """a button to go to previous page"""
        self.pack_forget()
        adding_page = AddingPage(self.root)

    def save_info(self):
        """save the information in database by passing in the name and age and condition(s)"""
        name = self.name_var.get().strip()
        age = self.age_var.get().strip()
        condition = self.condition_var.get().strip()

        # checking that the information is provided
        if len(name) <= 0 or len(age) <= 0 or len(condition) <= 0:
            showinfo(title="error", message="please input data")
            return

        if name.isnumeric():
            self.name_label["text"] = "please use words for name"
            self.name_label["foreground"] = "red"

        if age.isnumeric():
            age = int(age)
        else:
            self.age_label["text"] = "please use numbers for age"
            self.age_label["foreground"] = "red"
            return

        if ", " in condition:
            # if there is more than one condition
            condition = condition.split(", ")

        elif "," in condition:
            # checking for mistakes
            self.condition_label["text"] = "please use comma and a space afterwards"
            self.condition_label["foreground"] = "red"
            return

        # if no error
        save_file = project.insert_name(name, age)
        save_condition = project.insert_condition(condition, name)

        if save_file is not None and save_condition is not None:
            self.saving_info(save_file, save_condition)

    def saving_info(self, save_file, save_condition):
        """shows messages on whether the saving was successful"""
        if save_file == "new file":
            showinfo(title="saved", message="saved the data")

        elif save_file == "existing file":
            if save_condition is not False:
                showinfo(title="added", message="added data to existing file")
            else:
                showinfo(
                    title="file exists",
                    message="this condition is already in this file",
                )
                return
        self.destroy()
        condition_file = ConditionFile(self.root)


class MedicineFile(ttk.Frame):
    """
    a page to add new medication for a condition,
    condition needs to exist in database
    """

    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("370x370")
        self.pack(fill="both", padx=10)

        self.get_data()

    def get_data(self):
        """get all the names from database and shows them in a combobox"""
        self.names_list = project.get_all_names()
        self.create_widgets()

    def create_widgets(self):
        """two combobox to show name and condition, one entry to get the medication(s)"""
        self.back_button = ttk.Button(self, text="<", width=5, command=self.back_button)
        self.back_button.pack(pady=(2, 10), anchor="w")

        self.inst_1 = ttk.Label(self, text="select the person's name")
        self.inst_1.pack(pady=(0, 5))

        self.selected_name = tk.StringVar()
        self.choose_name = ttk.Combobox(
            self,
            textvariable=self.selected_name,
            state="readonly",
            values=self.names_list,
        )
        self.choose_name.pack(pady=(0, 10))
        self.choose_name.bind("<<ComboboxSelected>>", self.file_selected)

        self.sep_1 = ttk.Separator(self, orient="horizontal")
        self.sep_1.pack(fill="x")

        self.inst_2 = ttk.Label(self, text="select the condition you have medicine for")
        self.inst_2.pack(pady=(10, 0))

        self.selected_condition = tk.StringVar()
        self.choose_condition = ttk.Combobox(
            self,
            textvariable=self.selected_condition,
            state="readonly",
        )
        self.choose_condition.pack(pady=(5, 10))

        self.sep_2 = ttk.Separator(self, orient="horizontal")
        self.sep_2.pack(fill="x")

        self.inst_3 = ttk.Label(
            self, text="enter the medicine you have for the above condition"
        )
        self.inst_3.pack(pady=(10, 0))
        self.inst_4 = ttk.Label(
            self, text="(use a comma and a space for multiple input(', '))"
        )
        self.inst_4.pack()

        self.med = tk.StringVar()
        self.med_entry = ttk.Entry(self, textvariable=self.med)
        self.med_entry.pack()

        self.save_button = ttk.Button(self, text="save", command=self.save_med)
        self.save_button.pack(pady=(25, 0))

    def back_button(self):
        """go to previous page"""
        self.pack_forget()
        adding_page = AddingPage(self.root)

    def file_selected(self, event=None):
        """when a name is selected, get all the conditions related to that name"""
        if len(self.selected_name.get()) > 1:
            _, self.conditions = project.get_files(self.selected_name.get())
            del _

            self.choose_condition["value"] = self.condition

    def save_med(self):
        """save the medicine in database, related to the condition specified"""
        self.med = self.med.get()
        self.selected_name = self.selected_name.get()
        self.selected_condition = self.selected_condition.get()
        if len(self.med) <= 0:
            showinfo(title="missing data", message="please enter a medicine")
            return
        if ", " in self.med:
            self.meds = self.med.split(", ")
            med_info: list = project.insert_med(
                self.selected_name, self.selected_condition, self.meds
            )

            if med_info == self.meds:
                showinfo(title="data saved", message="medicines saved into database")
            self.pack_forget()
            medicine_file = MedicineFile(self.root)

        elif "," in self.med:
            self.inst_4["text"] = "please use comma and a space afterwards"
            self.inst_4["foreground"] = "red"
            return

        else:
            med_info: str = project.insert_med(
                self.selected_name, self.selected_condition, self.med
            )
            if med_info == self.med:
                showinfo(title="data saved", message=f"{self.med} saved into database")
            self.pack_forget()
            medicine_file = MedicineFile(self.root)


class OpenFile(ttk.Frame):
    """a base page that opens other pages for seeing the data"""

    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("350x260")

        self.pack(fill="both", padx=10)

        self.create_widgets()

    def create_widgets(self):
        """two button, one opens a page to see conditions, one opens a page to see medication"""
        self.back_button = ttk.Button(self, text="<", width=5, command=self.back_button)
        self.back_button.pack(pady=(2, 10), anchor="w")

        self.inst_1 = ttk.Label(self, text="see the conditions")
        self.inst_1.pack()

        self.open_con = ttk.Button(self, text="conditions", command=self.open_condition)
        self.open_con.pack()

        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.pack(fill="x", pady=15)

        self.inst_2 = ttk.Label(self, text="see medication")
        self.inst_2.pack()

        self.open_med = ttk.Button(self, text="medicine", command=self.open_medication)
        self.open_med.pack()

    def back_button(self):
        self.pack_forget()
        main_frame = MainFrame(self.root)

    def open_condition(self):
        """opens a page for seeing the condition files"""
        self.pack_forget()
        open_condition_file = OpenConditionFile(self.root)

    def open_medication(self):
        """opens a page for seeing the medication for a condition"""
        self.pack_forget()
        open_medication_file = OpenMedicationFile(self.root)


class OpenConditionFile(ttk.Frame):
    """a page that gets needed data and shows conditions a user has"""

    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("350x250")

        self.pack(fill="both", padx=10)

        self.get_data()

    def get_data(self):
        """get a list of all names in database and shows them in a combobox"""
        self.names_list = project.get_all_names()

        self.create_widgets()

    def create_widgets(self):
        """
        a combobox shows all the names, when a name is chosen user can see the conditions related to that name
        """

        self.back_button = ttk.Button(self, text="<", width=5, command=self.back_button)
        self.back_button.pack(pady=(2, 10), anchor="w")

        self.inst = ttk.Label(self, text="select the person's name")
        self.inst.pack(pady=(0, 10))

        self.selected_name = tk.StringVar()
        self.choose_name = ttk.Combobox(
            self,
            textvariable=self.selected_name,
            state="readonly",
            values=self.names_list,
        )
        self.choose_name.pack()

        self.see_button = ttk.Button(self, text="open file", command=self.opening_file)
        self.see_button.pack(pady=(15, 0))

    def back_button(self):
        """go to previous page"""
        self.pack_forget()
        open_file = OpenFile(self.root)

    def opening_file(self):
        """
        when button is hit, if a name is chosen, get all the data related to that name and send it to
        `SeeFile()`
        """
        if len(self.selected_name.get()) > 0:
            db_age, db_file = project.get_files(self.selected_name.get())

            self.pack_forget()
            see_file = SeeFile(self.root, db_age, self.selected_name.get(), db_file)
        else:
            showinfo(title="missing data", message="please select a name")
            return


class OpenMedicationFile(ttk.Frame):
    """a page that gets needed data and shows medication related to a condition"""

    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("300x300")

        self.pack(fill="both", padx=10)

        self.get_data()

    def get_data(self):
        """gets all the names in database and shows them in a combobox"""
        self.names_list = project.get_all_names()

        self.create_widgets()

    def create_widgets(self):
        """two comboboxes, one shows names and the other shows conditions"""
        self.back_button = ttk.Button(self, text="<", width=5, command=self.back_button)
        self.back_button.pack(pady=(2, 10), anchor="w")

        self.inst_1 = ttk.Label(self, text="choose the name")
        self.inst_1.pack()

        self.selected_name = tk.StringVar()
        self.choose_name = ttk.Combobox(
            self,
            textvariable=self.selected_name,
            state="readonly",
            values=self.names_list,
        )
        self.choose_name.pack()
        self.choose_name.bind("<<ComboboxSelected>>", self.name_selected)

        self.sep_1 = ttk.Separator(self, orient="horizontal")
        self.sep_1.pack(pady=15)

        self.inst_2 = ttk.Label(self, text="choose the condition")
        self.inst_2.pack()

        self.chosen_condition = tk.StringVar()
        self.condition_options = ttk.Combobox(
            self, textvariable=self.chosen_condition, state="readonly"
        )
        self.condition_options.pack(pady=(0, 15))

        self.open_file = ttk.Button(self, text="Open", command=self.open_med_file)
        self.open_file.pack()

    def back_button(self):
        """go to previous page"""
        self.pack_forget()
        open_file = OpenFile(self.root)

    def name_selected(self, event=None):
        """when a name is chosen, gets the data related to that name and shows the conditions in the combobox"""
        if len(self.selected_name.get()) > 0:
            _, self.condition = project.get_files(self.selected_name.get())
            del _

            self.condition_options["values"] = self.condition
        else:
            self.condition_options["values"] = []

    def open_med_file(self):
        """if data is provided, open a page and show the data"""
        if len(self.chosen_condition.get()) > 0:
            self.pack_forget()
            see_med_file = SeeMedFile(
                self.root, self.selected_name.get(), self.chosen_condition.get()
            )


class SeeFile(ttk.Frame):
    """a page that shows the data related to a name in a text file with the ability to hear them"""

    def __init__(self, root, file_age, file_name, file):
        super().__init__(root)

        self.root = root
        self.root.geometry("600x705")

        self.pack()

        self.file_age = file_age
        self.file_name = file_name
        self.file = file

        self.create_widgets()

    def create_widgets(self):
        """a text file to see all the data and a button to activate the text to speach and hear the data"""
        self.back_button = tk.Button(
            self, text="<", width=5, border=2, command=self.back_button
        )
        self.back_button.pack(anchor="w", pady=3, padx=10)

        self.file_text = tk.Text(self, height=30, border=5)
        self.file_text.pack()

        self.file_text.insert(
            1.0, f"name: {self.file_name}, age: {self.file_age}\nconditions:\n"
        )

        for i, conditions in enumerate(self.file):
            self.file_text.insert(f"{i + 3}.0", f"{conditions}\n")

        self.file_text["state"] = "disabled"

        self.texts = self.file_text.get("1.0", "end")

        self.speach_button = tk.Button(
            self, text="hear the text", border=3, command=self.voice
        )
        self.speach_button.pack(side="left", pady=(7, 5))

    def back_button(self):
        self.pack_forget()
        open_file = OpenFile(self.root)

    def voice(self):
        """activate text to speach"""
        # tts is an object of the TextToSpeach() class, see the last lines for reference
        global tts
        tts.voice_activated(self.texts)


class SeeMedFile(ttk.Frame):
    """a page that shows the data related to a condition in a text file with the ability to hear them"""

    def __init__(self, root, name, condition):
        super().__init__(root)

        self.root = root
        self.root.geometry("600x705")

        self.pack()
        self.name = name
        self.condition = condition

        self.get_data()

    def get_data(self):
        """get the medication of the condition and the age of the person for showing in text"""
        self.meds = project.get_med(self.condition, self.name)

        self.age, _ = project.get_files(self.name)
        del _

        self.create_widgets()

    def create_widgets(self):
        """a text file that shows all the data"""
        self.back_button = tk.Button(
            self, text="<", width=5, border=2, command=self.back_button
        )
        self.back_button.pack(anchor="w", pady=3, padx=10)

        self.med_text = tk.Text(self, height=30, border=5)
        self.med_text.pack()

        self.med_text.insert(
            1.0,
            f"name: {self.name}, age: {self.age}, condition: {self.condition}\nmedications:\n",
        )

        for i, med in enumerate(self.meds):
            self.med_text.insert(f"{i + 3}.0", f"{med}\n")

        self.med_text["state"] = "disabled"

        self.texts = self.med_text.get("1.0", "end")

        self.speach_button = tk.Button(
            self, text="hear the text", border=3, command=self.text_to_speach
        )
        self.speach_button.pack(side="left", pady=(7, 5))

    def back_button(self):
        """go to previous page"""
        self.pack_forget()
        open_medication_file = OpenMedicationFile(self.root)

    def text_to_speach(self):
        """activate text to speach and hear the data"""
        # tts is an object of TextToSpeach() class, see last lines for reference
        global tts
        tts.voice_activated(self.texts)


class EditDelete(ttk.Frame):
    """a base page with buttons that get you to pages for editing or deleting data"""

    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("352x250")
        self.pack(fill="both", padx=10)

        self.create_widgets()

    def create_widgets(self):
        """two buttons, one for edit page, one for delete page"""
        self.back_button = tk.Button(
            self, text="<", width=5, border=2, command=self.back_button
        )
        self.back_button.pack(anchor="w", pady=3, padx=10)

        self.inst_1 = ttk.Label(
            self, text="Edit a file (update a condition, correct a typo, etc)"
        )
        self.inst_1.pack(pady=10)

        self.edit_button = ttk.Button(
            self, text="Edit files", command=self.open_edit_page
        )
        self.edit_button.pack(pady=(0, 10))

        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.pack(fill="x")

        self.inst_2 = ttk.Label(self, text="Delete a file or a condition")
        self.inst_2.pack(pady=10)

        self.delete_button = ttk.Button(
            self, text="Delete files/conditions", command=self.open_delete_page
        )
        self.delete_button.pack()

    def back_button(self):
        """go to previous page"""
        self.pack_forget()
        main_frame = MainFrame(self.root)

    def open_edit_page(self):
        """go to edit page"""
        self.pack_forget()
        edit_page = EditPage(self.root)

    def open_delete_page(self):
        """go to delete page"""
        self.pack_forget()
        del_page = DeletePage(self.root)


class EditPage(ttk.Frame):
    """a base page that opens other pages for editing different types of data"""

    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("420x500")

        self.pack(fill="both")

        self.get_data()

    def get_data(self):
        """get a list of all names in database and show them in a combobox"""
        self.names_list = project.get_all_names()

        self.create_widgets()

    def create_widgets(self):
        """
        one combobox to choose a name, four buttons that each gets you to a page foe editing different data:
        one page for editing name, one page for editing age, one page for condition and one page for medicine
        buttons are deactivated until a name is chosen
        """

        self.back_button = tk.Button(
            self, text="<", width=5, border=2, command=self.back_button
        )
        self.back_button.pack(anchor="w", pady=3, padx=10)

        self.inst_1 = ttk.Label(self, text="choose a name and proceed")
        self.inst_1.pack(pady=10)

        self.selected_name = tk.StringVar()
        self.choose_name = ttk.Combobox(
            self,
            textvariable=self.selected_name,
            state="readonly",
            values=self.names_list,
        )
        self.choose_name.pack()
        self.choose_name.bind("<<ComboboxSelected>>", self.name_selected)

        self.inst_2 = ttk.Label(
            self, text="choose a name and edit it (for misspell and...)"
        )
        self.inst_2.pack(pady=10)

        self.name_button = ttk.Button(
            self, text="edit the name", state="disabled", command=self.edit_name
        )
        self.name_button.pack(pady=10)

        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.pack(fill="x")

        self.inst_3 = ttk.Label(self, text="choose the name then edit it's age")
        self.inst_3.pack(pady=10)

        self.age_button = ttk.Button(
            self, text="edit the age", state="disabled", command=self.edit_age
        )
        self.age_button.pack(pady=(0, 10))

        self.sep_2 = ttk.Separator(self, orient="horizontal")
        self.sep_2.pack(fill="x")

        self.inst_4 = ttk.Label(
            self, text="choose the name and edit one of it's conditions"
        )
        self.inst_4.pack(pady=10)

        self.condition_button = ttk.Button(
            self, text="edit a condition", state="disabled", command=self.edit_condition
        )
        self.condition_button.pack(pady=10)

        self.sep_3 = ttk.Separator(self, orient="horizontal")
        self.sep_3.pack(fill="x")

        self.inst_5 = ttk.Label(self, text="choose a name and edit a medicine")
        self.inst_5.pack(pady=10)

        self.med_button = ttk.Button(
            self, text="edit a medicine", state="disabled", command=self.edit_med
        )
        self.med_button.pack(pady=10)

    def back_button(self):
        """go to previous page"""
        self.pack_forget()
        edit_delete_page = EditDelete(self.root)

    def name_selected(self, event=None):
        """
        activate the buttons if a name is chosen and deactivate them if selection is removed
        this function may seem like bad design, but it saves me
        from checking if a name is selected for every other function
        """
        if len(self.selected_name.get()) > 0:
            self.name_button["state"] = "normal"
            self.age_button["state"] = "normal"
            self.condition_button["state"] = "normal"
            self.med_button["state"] = "normal"

        else:
            self.name_button["state"] = "disabled"
            self.age_button["state"] = "disabled"
            self.condition_button["state"] = "disabled"
            self.med_button["state"] = "disabled"

    def edit_name(self):
        """a page to edit name"""
        self.pack_forget()
        edit_name_page = EditNamePage(self.root, self.selected_name.get())

    def edit_age(self):
        """a page to edit age"""
        self.pack_forget()
        edit_age_page = EditAgePage(self.root, self.selected_name.get())

    def edit_condition(self):
        """a page to edit condition"""
        self.pack_forget()
        edit_condition_page = EditConditionPage(self.root, self.selected_name.get())

    def edit_med(self):
        """a page to edit medication"""
        self.pack_forget()
        edit_medication_page = EditMedicationPage(self.root, self.selected_name.get())


class EditNamePage(ttk.Frame):
    """a page for editing name"""

    def __init__(self, root, old_name):
        super().__init__(root)
        self.old_name = old_name

        self.root = root
        self.root.geometry("300x250")

        self.pack(fill="both")

        self.create_widgets()

    def create_widgets(self):
        """an entry to enter the new name"""
        self.back_button = ttk.Button(self, text="<", width=5, command=self.back_button)
        self.back_button.pack(pady=(3, 13), padx=10, anchor="w")

        self.info_1 = ttk.Label(self, text="the name you are changing is: ")
        self.pack()

        # show the old name as instruction
        self.info_2 = ttk.Label(self, text=f"{self.old_name}", foreground="red")
        self.info_2.pack(pady=(0, 20))

        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.pack(fill="x")

        self.inst = ttk.Label(self, text="enter the new name:")
        self.inst.pack(pady=10)

        self.new_name = tk.StringVar()
        self.get_name = ttk.Entry(self, textvariable=self.new_name)
        self.get_name.pack()

        self.save_button = ttk.Button(self, text="Save", command=self.save_name)
        self.save_button.pack(pady=15)

    def back_button(self):
        """go to previous page"""
        self.pack_forget()
        edit_page = EditPage(self.root)

    def save_name(self):
        """check if the data is inputted right and then save them"""
        if len(self.new_name.get()) <= 0:
            showinfo(title="error", message="please input the data")
            return
        elif not self.new_name.get().isnumeric():
            project.update_name(self.old_name, self.new_name.get())
            self.destroy()
            edit_page = EditPage(self.root)
            showinfo(title="name change", message="name updated")
        else:
            showinfo(title="wrong input", message="please enter a name with words")
            return


class EditAgePage(ttk.Frame):
    """a page to edit age"""

    def __init__(self, root, name):
        super().__init__(root)
        self.name = name

        self.root = root
        self.root.geometry("300x250")
        self.pack(fill="both")

        self.get_data()

    def get_data(self):
        """get the old age from database to show as instruction"""
        self.old_age, _ = project.get_files(self.name)
        del _

        self.create_widgets()

    def create_widgets(self):
        """an entry to get new age"""
        self.back_button = ttk.Button(self, text="<", width=5, command=self.back_button)
        self.back_button.pack(pady=(3, 13), padx=10, anchor="w")

        self.info_1 = ttk.Label(self, text="the age you are changing is: ")
        self.pack()

        self.info_2 = ttk.Label(self, text=f"{self.name}", foreground="blue")
        self.info_2.pack()

        self.info_3 = ttk.Label(self, text=f"is saved with \"{self.old_age}\" as age", foreground="red")
        self.info_3.pack(pady=(0, 20))

        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.pack(fill="x")

        self.inst = ttk.Label(self, text="enter the new age:")
        self.inst.pack(pady=10)

        self.new_age = tk.StringVar()
        self.get_age = ttk.Entry(self, textvariable=self.new_age)
        self.get_age.pack()

        self.save_button = ttk.Button(self, text="Save", command=self.save_age)
        self.save_button.pack(pady=15)

    def back_button(self):
        """go to previous page"""
        self.pack_forget()
        edit_page = EditPage(self.root)

    def save_age(self):
        """check if the data inputted is right, then save"""
        if self.new_age.get().isnumeric():
            project.update_age(self.name, int(self.new_age.get()))
            self.destroy()
            showinfo(title="age changed", message="age updated")
            edit_page = EditPage(self.root)
        else:
            showinfo(title="wrong input", message="please input name with numbers")
            return


class EditConditionPage(ttk.Frame):
    """a page to edit a condition"""

    def __init__(self, root, name):
        super().__init__(root)
        self.name = name

        self.root = root
        self.root.geometry("300x315")

        self.pack(fill="both")

        self.get_data()

    def get_data(self):
        """get all the condition related to the name chosen in EditPage to show in a combobox"""
        _, self.condition = project.get_files(self.name)
        del _

        self.create_widgets()

    def create_widgets(self):
        """one combobox that shows all conditions to be chosen, one entry to edit the chosen condition"""
        self.back_button = ttk.Button(self, text="<", width=5, command=self.back_button)
        self.back_button.pack(pady=(3, 13), padx=10, anchor="w")

        self.info_1 = ttk.Label(self, text=f"{self.name}", foreground="blue")
        self.info_1.pack()

        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.pack(fill="x", pady=(20, 10))

        self.inst = ttk.Label(self, text="select the condition you want to update")
        self.inst.pack()

        self.selected_condition = tk.StringVar()
        self.chose_condition = ttk.Combobox(
            self,
            textvariable=self.selected_condition,
            state="readonly",
            values=self.condition,
        )
        self.chose_condition.pack(pady=(5, 15))

        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.pack(fill="x")

        self.inst_2 = ttk.Label(self, text="enter the new condition:")
        self.inst_2.pack(pady=(15, 5))

        self.new_condition = tk.StringVar()
        self.get_condition = ttk.Entry(self, textvariable=self.new_condition)
        self.get_condition.pack()

        self.save_button = ttk.Button(self, text="Save", command=self.save_condition)
        self.save_button.pack(pady=15)

    def back_button(self):
        """go to previous page"""
        self.pack_forget()
        edit_page = EditPage(self.root)

    def save_condition(self):
        """check if inputted data is right, then save"""
        if len(self.selected_condition.get()) > 1 and len(self.new_condition.get()) > 1:
            project.update_condition(
                self.selected_condition.get(), self.new_condition.get(), self.name
            )
            self.destroy()
            showinfo(title="condition changed", message="condition updated")
            edit_page = EditPage(self.root)
        else:
            showinfo(title="missing data", message="please input the condition")


class EditMedicationPage(ttk.Frame):
    """a page to edit a medicine"""

    def __init__(self, root, name):
        super().__init__(root)
        self.root = root
        self.root.geometry("300x340")

        self.name = name

        self.pack(fill="both")

        self.get_data()

    def get_data(self):
        """get all the condition related to the name chosen in EditPage to be shown in a combobox"""
        _, self.condition = project.get_files(self.name)
        del _

        self.create_widgets()

    def create_widgets(self):
        """
        one combobox that shows all the conditions,
        one combobox that shows all the medication used for that condition,
        second combobox gets data when the first one is selected,
        an entry to get the new medicine
        """
        self.back_button = ttk.Button(self, text="<", width=5, command=self.back_button)
        self.back_button.pack(pady=(2, 10), padx=10, anchor="w")

        self.info_1 = ttk.Label(self, text=f"{self.name}", foreground="blue")
        self.info_1.pack()

        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.pack(fill="x", pady=(20, 10))

        self.inst_1 = ttk.Label(self, text="choose the condition")
        self.inst_1.pack()

        self.chosen_condition = tk.StringVar()
        self.condition_options = ttk.Combobox(
            self,
            textvariable=self.chosen_condition,
            values=self.condition,
            state="readonly",
        )
        self.condition_options.pack(pady=(0, 15))

        self.condition_options.bind("<<ComboboxSelected>>", self.condition_selected)

        self.sep_1 = ttk.Separator(self, orient="horizontal")
        self.sep_1.pack(fill="x")

        self.inst_2 = ttk.Label(self, text="choose the medicine")
        self.inst_2.pack()

        self.old_med_var = tk.StringVar()
        self.medicine_options = ttk.Combobox(
            self, textvariable=self.old_med_var, state="readonly"
        )
        self.medicine_options.pack(pady=(0, 10))

        self.sep_2 = ttk.Separator(self, orient="horizontal")
        self.sep_2.pack(fill="x")

        self.inst_3 = ttk.Label(self, text="enter the new medicine")
        self.inst_3.pack()

        self.new_med_var = tk.StringVar()
        self.new_med = ttk.Entry(self, textvariable=self.new_med_var)
        self.new_med.pack(pady=(0, 10))

        self.save = ttk.Button(self, text="Save", command=self.save_data)
        self.save.pack()

    def back_button(self):
        """go to previous page"""
        self.pack_forget()
        edit_page = EditPage(self.root)

    def condition_selected(self, event=None):
        """
        when a condition is selected in first combobox,
        get all the medication related to that condition and show them in second combobox
        """
        if len(self.chosen_condition.get()) > 0:
            self.meds = project.get_med(self.chosen_condition.get(), self.name)

            self.medicine_options["values"] = self.meds
        else:
            self.medicine_options["values"] = []

    def save_data(self):
        """check if the data inputted is right, then save it"""
        if len(self.old_med_var.get()) > 0 and len(self.new_med_var.get()) > 0:
            project.update_med(
                self.name,
                self.condition.get(),
                self.old_med_var.get(),
                self.new_med_var.get(),
            )
            self.destroy()
            showinfo(title="medicine changed", message="medicine updated")
            edit_page = EditPage(self.root)

        else:
            showinfo(title="missing data", message="please input data")


class DeletePage(ttk.Frame):
    """a page for deleting data"""

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.geometry("360x370")

        self.pack(fill="both", padx=10)

        self.get_data()

    def get_data(self):
        """get a list of all names in database and show in a combobox"""
        self.names_list = project.get_all_names()

        self.create_widgets()

    def create_widgets(self):
        """
        three Radiobuttons that let you decide what kind of data you want to delete
        three comboboxes to get the data to be deleted
        comboboxes activate when related radiobutton is selected
        """
        self.back_button = ttk.Button(self, text="<", width=5, command=self.back_button)
        self.back_button.pack(pady=(3, 13), padx=10, anchor="w")

        self.inst_1 = ttk.Label(
            self, text="delete a file or delete a condition in a file"
        )
        self.inst_1.pack(anchor="w", pady=15)

        self.selected_option = tk.StringVar()
        self.del_option1 = ttk.Radiobutton(
            self,
            text="delete a file",
            value="file",
            variable=self.selected_option,
            command=self.option_selected,
        )
        self.del_option1.pack(anchor="w", pady=(5, 5))

        self.del_option2 = ttk.Radiobutton(
            self,
            text="delete a condition",
            value="condition",
            variable=self.selected_option,
            command=self.option_selected,
        )
        self.del_option2.pack(anchor="w")

        self.del_option3 = ttk.Radiobutton(
            self,
            text="delete a medicine",
            value="medicine",
            variable=self.selected_option,
            command=self.option_selected,
        )
        self.del_option3.pack(anchor="w", pady=(5, 0))

        self.chosen_name = tk.StringVar()
        self.name_options = ttk.Combobox(
            self,
            textvariable=self.chosen_name,
            state="readonly",
            values=self.names_list,
        )
        self.name_options.pack(pady=10)

        self.name_options.bind("<<ComboboxSelected>>", self.file_selected)

        self.sep_1 = ttk.Separator(self, orient="horizontal")
        self.sep_1.pack(fill="x")

        self.chosen_condition = tk.StringVar()
        self.condition_options = ttk.Combobox(
            self, textvariable=self.chosen_condition, state="disable"
        )
        self.condition_options.pack()

        self.condition_options.bind("<<ComboboxSelected>>", self.con_selected)

        self.sep_2 = ttk.Separator(self, orient="horizontal")
        self.sep_2.pack(fill="x", pady=10)

        self.chosen_med = tk.StringVar()
        self.medicine_options = ttk.Combobox(
            self, textvariable=self.chosen_med, state="disable"
        )
        self.medicine_options.pack()

        self.delete_button = ttk.Button(self, text="delete", command=self.delete_func)
        self.delete_button.pack(anchor="s", pady=10)

    def back_button(self):
        """go to previous page"""
        self.pack_forget()
        edit_delete_page = EditDelete(self.root)

    def option_selected(self):
        # if deleting condition or medicine radiobutton is selected:
        if (
            self.selected_option.get() == "condition"
            or self.selected_option.get() == "medicine"
        ):
            # condition combobox gets activated in both case cause medications are related to conditions
            self.condition_options["state"] = "readonly"
            # if medicine radiobutton is activated open the combobox for it
            if self.selected_option.get() == "medicine":
                self.medicine_options["state"] = "readonly"
            # this option is for user changes radiobutton selection
            else:
                self.medicine_options["state"] = "disabled"
        # this option is for when user changes the selection
        else:
            self.condition_options["state"] = "disabled"
            self.medicine_options["state"] = "disabled"

    def file_selected(self, event=None):
        """when a name is selected, get all the condition related to that name and get them in condition combobox"""
        if len(self.chosen_name.get()) > 0:
            # get data from database
            _, self.condition = project.get_files(self.chosen_name.get())
            del _

            self.condition_options["values"] = self.condition
        else:
            self.condition_options["values"] = []

    def con_selected(self, event=None):
        """
        when a condition is selected
        get all the medication related to that condition and get them into medicine combobox
        """
        if len(self.chosen_condition.get()) > 0:
            # get data from database
            self.meds = project.get_med(
                self.chosen_condition.get(), self.chosen_name.get()
            )
            self.medicine_options["values"] = self.meds

        else:
            self.medicine_options["values"] = []

    def delete_func(self):
        """
        depending on the type of deleting user has chosen with radiobuttons,
        ask if they are sue then activate the related function
        """
        if self.selected_option.get() == "file":
            self.answer = askokcancel(
                title="delete file",
                message=f'Deleting will delete all data for "{self.chosen_name.get()}"',
                icon=WARNING,
            )
            if self.answer:
                self.delete_file()

        elif self.selected_option.get() == "condition":
            self.answer = askokcancel(
                title="deleting data",
                message=f'you are deleting "{self.chosen_condition.get()}" from "{self.chosen_name.get()}" file',
                icon=WARNING,
            )
            if self.answer:
                self.delete_condition()

        elif self.selected_option.get() == "medicine":
            self.answer = askokcancel(
                title="deleting data",
                message=f'you are deleting "{self.chosen_med.get()} from {self.chosen_name} file',
                icon=WARNING,
            )
            if self.answer:
                self.delete_med()

    def delete_file(self):
        """if user has chosen to delete a file, delete the whole file"""
        self.del_info = project.full_file_delete(self.chosen_name.get())
        if self.del_info == "file deleted":
            self.destroy()
            showinfo(title="deleted file", message="your file has been deleted")
            del_page = DeletePage(self.root)

    def delete_condition(self):
        """if user has chosen to delete a condition, delete it"""
        self.del_info = project.condition_delete(
            self.chosen_name.get(), self.chosen_condition.get()
        )
        if self.del_info == "condition deleted":
            self.destroy()
            showinfo(title="deleted condition", message="your file has been updated")
            del_page = DeletePage(self.root)

    def delete_med(self):
        """if the user has chosen to delete a medicine, delete it"""
        self.del_info = project.delete_medicine(
            self.chosen_name.get(), self.chosen_condition.get(), self.chosen_med.get()
        )

        if self.del_info == "medicine deleted":
            self.destroy()
            showinfo(title="deleted medicine", message="your file has been updated")
            del_page = DeletePage(self.root)


if __name__ == "__main__":
    main()
