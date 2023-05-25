import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, askokcancel, WARNING
from ctypes import windll
import sql_funcs
import pyttsx3
# from threading import Thread

windll.shcore.SetProcessDpiAwareness(1)


class TextToSpeach():
    def __init__(self, record_text):
        super().__init__()
        self.record_text = record_text

        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)

    def activate_voice(self):
        self.engine.say(self.record_text)
        self.engine.runAndWait()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("medical record")
        self.resizable(0, 0)
        self.geometry("320x300")
        self.style = ttk.Style()
        self.style.theme_use("xpnative")

        sql_funcs.make_db()

        main_frame = MainFrame(self)


class MainFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("320x300")

        self.pack(fill="both", padx=10)

        self.create_widgets()

    def create_widgets(self):
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
        self.pack_forget()
        adding_page = AddingPage(self.root)

    def open_file_page(self):
        self.pack_forget()
        open_file = OpenFile(self.root)

    def open_e_d_page(self):
        self.pack_forget()
        edit_delete_page = EditDelete(self.root)


class AddingPage(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("270x250")
        self.pack(fill="both", padx=10)

        self.create_widgets()

    def create_widgets(self):
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
        self.pack_forget()
        main_frame = MainFrame(self.root)

    def open_con_file(self):
        self.pack_forget()
        condition_file = ConditionFile(self.root)

    def open_medicine(self):
        self.pack_forget()
        medicine_file = MedicineFile(self.root)


class ConditionFile(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("360x390")
        self.pack(fill="both", padx=10)

        self.get_data()

    def get_data(self):
        self.names_list = sql_funcs.get_all_names()

        self.create_widgets()

    def create_widgets(self):
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

        self.inst_1 = ttk.Label(self, text="please enter/choose the condition(s)")
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
        self.pack_forget()
        adding_page = AddingPage(self.root)

    def save_info(self):
        name = self.name_var.get()
        age = self.age_var.get()
        condition = self.condition_var.get()

        if len(name) <= 0 or len(age) <= 0 or len(condition) <= 0:
            showinfo(title="error", message="please input data")
            return

        if name.isnumeric():
            self.name_label["text"] = "please use wrds for name"
            self.name_label["foreground"] = "red"

        if age.isnumeric():
            age = int(age)
        else:
            self.age_label["text"] = "please use numbers for age"
            self.age_label["foreground"] = "red"
            return

        if ", " in condition:
            conditions = [condition.split(", ")]
            save_file = sql_funcs.insert_name(name, age)
            save_condition = sql_funcs.insert_condition(conditions, name)

            self.saving_info(save_file, save_condition)

        elif "," in condition:
            self.condition_label["text"] = "please use comma and a space afterwards"
            self.condition_label["foreground"] = "red"
            return

        else:
            save_file = sql_funcs.insert_name(name, age)
            save_condition = sql_funcs.insert_condition(condition, name)

            self.saving_info(save_file, save_condition)

    def saving_info(self, save_file, save_condition):
        if save_file == "new file":
            showinfo(title="saved", message="saved the data")

        elif save_file == "new condition":
            if save_condition:
                showinfo(title="added", message="added data to existing file")
            else:
                showinfo(
                    title="file exists",
                    message="this condition is already in this file",
                )
                return
        self.destroy()
        adding_page = AddingPage(self.root)


class MedicineFile(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("370x370")
        self.pack(fill="both", padx=10)

        self.get_data()

    def get_data(self):
        self.names_list = sql_funcs.get_all_names()
        self.create_widgets()

    def create_widgets(self):
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
        self.pack_forget()
        adding_page = AddingPage(self.root)

    def file_selected(self, event=None):
        if len(self.selected_name.get()) > 1:
            _, self.c = sql_funcs.get_files(self.selected_name.get())
            del _

            condition = [val for t in self.c for val in t]
            self.choose_condition["value"] = condition

    def save_med(self):
        self.med = self.med.get()
        self.selected_name = self.selected_name.get()
        self.selected_condition = self.selected_condition.get()
        if len(self.med) <= 0:
            showinfo(title="missing data", message="please enter a medicine")
            return
        if ", " in self.med:
            self.meds = self.med.split(", ")
            med_info: list = sql_funcs.insert_med(
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
            med_info: str = sql_funcs.insert_med(
                self.selected_name, self.selected_condition, self.med
            )
            if med_info == self.med:
                showinfo(title="data saved", message=f"{self.med} saved into database")
            self.pack_forget()
            medicine_file = MedicineFile(self.root)


class OpenFile(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("350x260")

        self.pack(fill="both", padx=10)

        self.create_widgets()

    def create_widgets(self):
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
        self.pack_forget()
        open_condition_file = OpenConditionFile(self.root)

    def open_medication(self):
        self.pack_forget()
        open_medication_file = OpenMedicationFile(self.root)


class OpenConditionFile(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("350x250")

        self.pack(fill="both", padx=10)

        self.get_data()

    def get_data(self):
        self.names_list = sql_funcs.get_all_names()

        self.create_widgets()

    def create_widgets(self):
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
        self.pack_forget()
        open_file = OpenFile(self.root)

    def opening_file(self):
        if len(self.selected_name.get()) > 0:
            db_age, db_file = sql_funcs.get_files(self.selected_name.get())

            self.pack_forget()
            see_file = SeeFile(self.root, db_age, self.selected_name.get(), db_file)
        else:
            showinfo(title="missing data", message="please select a name")
            return


class OpenMedicationFile(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("300x300")

        self.pack(fill="both", padx=10)

        self.get_data()

    def get_data(self):
        self.names_list = sql_funcs.get_all_names()

        self.create_widgets()

    def create_widgets(self):
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
        self.pack_forget()
        open_file = OpenFile(self.root)

    def name_selected(self, event=None):
        if len(self.selected_name.get()) > 0:
            _, self.c = sql_funcs.get_files(self.selected_name.get())
            del _
            self.condition = [val for t in self.c for val in t]

            self.condition_options["values"] = self.condition

    def open_med_file(self):
        if len(self.chosen_condition.get()) > 0:
            self.pack_forget()
            see_med_file = SeeMedFile(
                self.root, self.selected_name.get(), self.chosen_condition.get()
            )


class SeeFile(ttk.Frame):
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
            self.file_text.insert(f"{i+3}.0", f"{conditions[0]}\n")

        self.file_text["state"] = "disabled"

        self.texts = self.file_text.get("1.0", "end")

        self.tts = TextToSpeach(
            self.texts,
        )
        # self.tts.run()

        self.speach_button = tk.Button(
            self, text="hear the text", border=3, command=self.text_to_speach
        )
        self.speach_button.pack(side="left", pady=(7, 5))

    def back_button(self):
        self.pack_forget()
        open_file = OpenFile(self.root)

    def text_to_speach(self):
        self.tts.activate_voice()


class SeeMedFile(ttk.Frame):
    def __init__(self, root, name, condition):
        super().__init__(root)

        self.root = root
        self.root.geometry("600x705")

        self.pack()
        self.name = name
        self.condition = condition

        self.get_data()

    def get_data(self):
        self.age, _ = sql_funcs.get_files(self.name)
        del _

        self.create_widgets()

    def create_widgets(self):
        self.meds = sql_funcs.get_med(self.condition, self.name)

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
            self.med_text.insert(f"{i+3}.0", f"{med[0]}\n")

        self.med_text["state"] = "disabled"

        self.texts = self.med_text.get("1.0", "end")
        self.tts = TextToSpeach(
            self.texts,
        )
        self.tts.run()

        self.speach_button = tk.Button(
            self, text="hear the text", border=3, command=self.text_to_speach
        )
        self.speach_button.pack(side="left", pady=(7, 5))

    def back_button(self):
        self.pack_forget()
        open_medication_file = OpenMedicationFile(self.root)

    def text_to_speach(self):
        self.tts.activate_voice()


class EditDelete(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("352x250")
        self.pack(fill="both", padx=10)

        self.create_widgets()

    def create_widgets(self):
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
        self.pack_forget()
        main_frame = MainFrame(self.root)

    def open_edit_page(self):
        self.pack_forget()
        edit_page = EditPage(self.root)

    def open_delete_page(self):
        self.pack_forget()
        del_page = DeletePage(self.root)


class EditPage(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("420x500")

        self.pack(fill="both")

        self.get_data()

    def get_data(self):
        self.names_list = sql_funcs.get_all_names()

        self.create_widgets()

    def create_widgets(self):
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
        self.pack_forget()
        edit_delete_page = EditDelete(self.root)

    def name_selected(self, event=None):
        """this function may seem like bad design, but it saves me
        from checking if a name is selected for every other function"""
        if len(self.selected_name.get()) > 0:
            self.name_button["state"] = "normal"
            self.age_button["state"] = "normal"
            self.condition_button["state"] = "normal"
            self.med_button["state"] = "normal"

            self.selected_name = self.selected_name.get()
        else:
            self.name_button["state"] = "disabled"
            self.age_button["state"] = "disabled"
            self.condition_button["state"] = "disabled"
            self.med_button["state"] = "disabled"

    def edit_name(self):
        self.pack_forget()
        edit_name_page = EditNamePage(self.root, self.selected_name)

    def edit_age(self):
        self.pack_forget()
        edit_age_page = EditAgePage(self.root, self.selected_name)

    def edit_condition(self):
        self.pack_forget()
        edit_condition_page = EditConditionPage(self.root, self.selected_name)

    def edit_med(self):
        self.pack_forget()
        edit_medication_page = EditMedicationPage(self.root, self.selected_name)


class EditNamePage(ttk.Frame):
    def __init__(self, root, old_name):
        super().__init__(root)
        self.old_name = old_name

        self.root = root
        self.root.geometry("300x250")

        self.pack(fill="both")

        self.create_widgets()

    def create_widgets(self):
        self.back_button = ttk.Button(self, text="<", width=5, command=self.back_button)
        self.back_button.pack(pady=(3, 13), padx=10, anchor="w")

        self.info_1 = ttk.Label(self, text="the name you are changing is: ")
        self.pack()

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
        self.pack_forget()
        edit_page = EditPage(self.root)

    def save_name(self):
        if len(self.new_name.get()) <= 0:
            showinfo(title="error", message="please input the data")
            return
        elif not self.new_name.get().isnumeric():
            sql_funcs.update_name(self.old_name, self.new_name.get())
            self.destroy()
            edit_page = EditPage(self.root)
            showinfo(title="name change", message="name updated")
        else:
            showinfo(title="wrong input", message="please enter a name with words")
            return


class EditAgePage(ttk.Frame):
    def __init__(self, root, name):
        super().__init__(root)
        self.name = name

        self.root = root
        self.root.geometry("300x250")
        self.pack(fill="both")

        self.get_data()

    def get_data(self):
        self.old_age, _ = sql_funcs.get_files(self.name)
        del _

        self.create_widgets()

    def create_widgets(self):
        self.back_button = ttk.Button(self, text="<", width=5, command=self.back_button)
        self.back_button.pack(pady=(3, 13), padx=10, anchor="w")

        self.info_1 = ttk.Label(self, text="the age you are changing is: ")
        self.pack()

        self.info_2 = ttk.Label(self, text=f"{self.old_age}", foreground="red")
        self.info_2.pack(pady=(0, 20))

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
        self.pack_forget()
        edit_page = EditPage(self.root)

    def save_age(self):
        if self.new_age.get().isnumeric():
            sql_funcs.update_age(self.name, int(self.new_age.get()))
            self.destroy()
            showinfo(title="age changed", message="age updated")
            edit_page = EditPage(self.root)
        else:
            showinfo(title="wrong input", message="please input name with numbers")
            return


class EditConditionPage(ttk.Frame):
    def __init__(self, root, name):
        super().__init__(root)
        self.name = name

        self.root = root
        self.root.geometry("300x250")

        self.pack(fill="both")

        self.get_data()

    def get_data(self):
        _, self.c = sql_funcs.get_files(self.name)
        del _
        self.condition = [val for t in self.c for val in t]

        self.create_widgets()

    def create_widgets(self):
        self.back_button = ttk.Button(self, text="<", width=5, command=self.back_button)
        self.back_button.pack(pady=(3, 13), padx=10, anchor="w")

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
        self.pack_forget()
        edit_page = EditPage(self.root)

    def save_condition(self):
        if len(self.selected_condition.get()) > 1 and len(self.new_condition.get()) > 1:
            sql_funcs.update_condition(
                self.selected_condition.get(), self.new_condition.get(), self.name
            )
            self.destroy()
            showinfo(title="condition changed", message="condition updated")
            edit_page = EditPage(self.root)
        else:
            showinfo(title="missing data", message="please input the condition")


class EditMedicationPage(ttk.Frame):
    def __init__(self, root, name):
        super().__init__(root)
        self.root = root
        self.root.geometry("300x300")

        self.name = name

        self.pack(fill="both")

        self.get_data()

    def get_data(self):
        _, self.c = sql_funcs.get_files(self.name)
        del _
        self.condition = [val for t in self.c for val in t]

        self.create_widgets()

    def create_widgets(self):
        self.back_button = ttk.Button(self, text="<", width=5, command=self.back_button)
        self.back_button.pack(pady=(2, 10), padx=10, anchor="w")

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
        self.pack_forget()
        edit_page = EditPage(self.root)

    def condition_selected(self, event=None):
        if len(self.chosen_condition.get()) > 0:
            self.condition = self.chosen_condition.get()
            self.m = sql_funcs.get_med(self.chosen_condition.get(), self.name)
            meds = [val for i in self.m for val in i]
            self.medicine_options["values"] = meds
        else:
            self.medicine_options["values"] = []

    def save_data(self):
        if len(self.old_med_var.get()) > 0 and len(self.new_med_var.get()) > 0:
            sql_funcs.update_med(
                self.name,
                self.condition,
                self.old_med_var.get(),
                self.new_med_var.get(),
            )
            self.destroy()
            showinfo(title="medicine changed", message="medicine updated")
            edit_page = EditPage(self.root)


class DeletePage(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.geometry("360x370")

        self.pack(fill="both", padx=10)

        self.get_data()

    def get_data(self):
        self.names_list = sql_funcs.get_all_names()

        self.create_widgets()

    def create_widgets(self):
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
        self.pack_forget()
        edit_delete_page = EditDelete(self.root)

    def option_selected(self):
        if (
            self.selected_option.get() == "condition"
            or self.selected_option.get() == "medicine"
        ):
            self.condition_options["state"] = "readonly"
            if self.selected_option.get() == "medicine":
                self.medicine_options["state"] = "readonly"
            else:
                self.medicine_options["state"] = "disabled"

        else:
            self.condition_options["state"] = "disabled"
            self.medicine_options["state"] = "disabled"

    def file_selected(self, event=None):
        if len(self.chosen_name.get()) > 0:
            _, self.c = sql_funcs.get_files(self.chosen_name.get())
            del _

            condition = [val for t in self.c for val in t]
            self.condition_options["values"] = condition

    def con_selected(self, event=None):
        if len(self.chosen_condition.get()) > 0:
            self.m = sql_funcs.get_med(
                self.chosen_condition.get(), self.chosen_name.get()
            )
            meds = [val for i in self.m for val in i]
            self.medicine_options["values"] = meds

    def delete_func(self):
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
        self.del_info = sql_funcs.full_file_delete(self.chosen_name.get())
        if self.del_info == "file deleted":
            self.destroy()
            showinfo(title="deleted file", message="your file has been deleted")
            del_page = DeletePage(self.root)

    def delete_condition(self):
        self.del_info = sql_funcs.condition_delete(
            self.chosen_name.get(), self.chosen_condition.get()
        )
        if self.del_info == "condition deleted":
            self.destroy()
            showinfo(title="deleted condition", message="your file has been updated")
            del_page = DeletePage(self.root)

    def delete_med(self):
        self.del_info = sql_funcs.medicine_delete(
            self.chosen_name.get(), self.chosen_condition.get(), self.chosen_med.get()
        )

        if self.del_info == "medicine deleted":
            self.destroy()
            showinfo(title="deleted medicine", message="your file has been updated")
            del_page = DeletePage(self.root)


if __name__ == "__main__":
    app = App()
    app.mainloop()
