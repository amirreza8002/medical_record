import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, askokcancel, WARNING
from ctypes import windll
import sql_funcs
import pyttsx3

windll.shcore.SetProcessDpiAwareness(1)


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
        welcome.pack()

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
        self.root.geometry("350x400")
        self.pack(fill="both", padx=10)

        self.create_widgets()

    def create_widgets(self):
        names_list = sql_funcs.get_all_names()

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
            self, textvariable=self.name_var, values=names_list
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
        main_frame = MainFrame(self.root)

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


class OpenFile(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.root.geometry("350x250")

        self.pack(fill="both", padx=10)

        self.create_widgets()

    def create_widgets(self):
        names_list = sql_funcs.get_all_names()

        self.back_button = ttk.Button(self, text="<", command=self.back_button)
        self.back_button.pack(pady=(2, 10), anchor="w")

        self.inst = ttk.Label(self, text="select the person's name")
        self.inst.pack(pady=(0, 10))

        self.selected_name = tk.StringVar()
        self.choose_name = ttk.Combobox(
            self, textvariable=self.selected_name, state="readonly", values=names_list
        )
        self.choose_name.pack()

        self.see_button = ttk.Button(self, text="open file", command=self.opening_file)
        self.see_button.pack(pady=(15, 0))

    def back_button(self):
        self.pack_forget()
        main_frame = MainFrame(self.root)

    def opening_file(self):
        if len(self.selected_name.get()) > 0:
            db_age, db_file = sql_funcs.get_files(self.selected_name.get())

            self.pack_forget()
            see_file = SeeFile(self.root, db_age, self.selected_name.get(), db_file)
        else:
            showinfo(title="missing data", message="please select a name")
            return


class SeeFile(ttk.Frame):
    def __init__(self, root, file_age, file_name, file):
        super().__init__(root)

        self.root = root
        self.root.geometry("600x600")

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

        self.record_text = tk.Text(self, height=25, border=5)
        self.record_text.pack()

        self.record_text.insert(
            1.0, f"name: {self.file_name}, age: {self.file_age}\nconditions:\n"
        )

        for i, conditions in enumerate(self.file):
            self.record_text.insert(f"{i+3}.0", f"{conditions[0]}\n")

        self.record_text["state"] = "disabled"

        self.speach_button = tk.Button(
            self, text="hear the text", border=3, command=self.text_to_speach
        )
        self.speach_button.pack(side="left", pady=(7, 5))

    def back_button(self):
        self.pack_forget()
        open_file = OpenFile(self.root)

    def text_to_speach(self):
        pass


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
        self.root.geometry("400x400")

        self.pack(fill="both")

        self.create_widgets()

    def create_widgets(self):
        names_list = sql_funcs.get_all_names()

        self.back_button = tk.Button(
            self, text="<", width=5, border=2, command=self.back_button
        )
        self.back_button.pack(anchor="w", pady=3, padx=10)

        self.inst_1 = ttk.Label(self, text="choose a name and proceed")
        self.inst_1.pack(pady=10)

        self.selected_name = tk.StringVar()
        self.choose_name = ttk.Combobox(
            self, textvariable=self.selected_name, state="readonly", values=names_list
        )
        self.choose_name.pack()

        self.inst_2 = ttk.Label(
            self, text="choose a name and edit it (for misspell and...)"
        )
        self.inst_2.pack(pady=10)

        self.name_button = ttk.Button(
            self, text="edit the name", command=self.edit_name
        )
        self.name_button.pack(pady=10)

        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.pack(fill="x")

        self.inst_3 = ttk.Label(self, text="choose the name then edit it's age")
        self.inst_3.pack(pady=10)

        self.age_button = ttk.Button(self, text="edit the age", command=self.edit_age)
        self.age_button.pack(pady=(0, 10))

        self.sep_2 = ttk.Separator(self, orient="horizontal")
        self.sep_2.pack(fill="x")

        self.inst_4 = ttk.Label(
            self, text="choose the name and edit one it's conditions"
        )
        self.inst_4.pack(pady=10)

        self.condition_button = ttk.Button(
            self, text="edit a condition", command=self.edit_condition
        )
        self.condition_button.pack(pady=10)

    def back_button(self):
        self.pack_forget()
        edit_delete_page = EditDelete(self.root)

    def edit_name(self):
        if len(self.selected_name.get()) > 0:
            self.pack_forget()
            edit_name_page = EditNamePage(self.root, self.selected_name.get())
        else:
            showinfo(title="missing data", message="please select a name")
            return

    def edit_age(self):
        if len(self.selected_name.get()) > 0:
            self.pack_forget()
            edit_age_page = EditAgePage(self.root, self.selected_name.get())

        else:
            showinfo(title="missing data", message="please select a name")
            return

    def edit_condition(self):
        if len(self.selected_name.get()) > 0:
            self.pack_forget()
            edit_condition_page = EditConditionPage(self.root, self.selected_name.get())

        else:
            showinfo(title="missing data", message="please select a name")
            return


class EditNamePage(ttk.Frame):
    def __init__(self, root, old_name):
        super().__init__(root)
        self.old_name = old_name

        self.root = root
        self.root.geometry("300x250")

        self.pack(fill="both")

        self.create_widgets()

    def create_widgets(self):
        self.back_button = ttk.Button(self, text="<", command=self.back_button)
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

        self.create_widgets()

    def create_widgets(self):
        self.old_age, _ = sql_funcs.get_files(self.name)
        del _

        self.back_button = ttk.Button(self, text="<", command=self.back_button)
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

        self.create_widgets()

    def create_widgets(self):
        _, self.conditions = sql_funcs.get_files(self.name)
        del _

        self.back_button = ttk.Button(self, text="<", command=self.back_button)
        self.back_button.pack(pady=(3, 13), padx=10, anchor="w")

        self.inst = ttk.Label(self, text="select the condition you want to update")
        self.inst.pack()

        self.selected_condition = tk.StringVar()
        self.chose_condition = ttk.Combobox(
            self,
            textvariable=self.selected_condition,
            state="readonly",
            values=self.conditions,
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


class DeletePage(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.geometry("360x300")

        self.pack(fill="both", padx=10)

        self.create_widgets()

    def create_widgets(self):
        names_list = sql_funcs.get_all_names()

        self.back_button = ttk.Button(self, text="<", command=self.back_button)
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

        self.chosen_name = tk.StringVar()
        self.name_options = ttk.Combobox(
            self, textvariable=self.chosen_name, state="readonly", values=names_list
        )
        self.name_options.pack(pady=10)

        self.name_options.bind("<<ComboboxSelected>>", self.file_selected)

        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.pack(fill="x")

        self.chosen_condition = tk.StringVar()
        self.condition_options = ttk.Combobox(
            self, textvariable=self.chosen_condition, state="disable"
        )
        self.condition_options.pack(pady=(0, 10))

        self.delete_button = ttk.Button(self, text="delete", command=self.delete_fuc)
        self.delete_button.pack(anchor="s", pady=10)

    def back_button(self):
        self.pack_forget()
        edit_delete_page = EditDelete(self.root)

    def option_selected(self):
        if self.selected_option.get() == "condition":
            self.condition_options["state"] = "readonly"

        else:
            self.condition_options["state"] = "disabled"

    def file_selected(self, event=None):
        if len(self.chosen_name.get()) > 1:
            _, self.c = sql_funcs.get_files(self.chosen_name.get())
            del _

            condition = [val for t in self.c for val in t]
            self.condition_options["values"] = condition

    def delete_fuc(self):
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


if __name__ == "__main__":
    app = App()
    app.mainloop()
