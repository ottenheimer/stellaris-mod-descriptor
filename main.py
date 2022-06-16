from pathlib import Path
from Mod import Mod
from tkinter import *


def initialize_descriptors(mod_path):
    descriptors_to_create = []
    path = Path(mod_path)
    if path.exists():
        for file in path.glob("*"):
            if file.is_dir():
                mod_name = file.name
                file_to_create = mod_path + "\\" + mod_name + ".mod"
                if Path(file_to_create).is_file():
                    print(f"already created {mod_name}.mod")
                    continue
                else:
                    for mod_file in Path(file).glob("*.mod"):
                        # print(mod_file)
                        mod = Mod(mod_name, file_to_create)
                        mod.descriptor_content = mod_file.read_text()

                        descriptors_to_create.append(mod)
    return descriptors_to_create


def create_descriptor_text(mod_path, descriptors_to_create):
    for mod in descriptors_to_create:
        create_mod = Path(mod.path_to_create)
        content = mod.descriptor_content
        path = mod_path + "\\" + mod.mod_folder_name
        path = "\"" + path.replace("\\", "/") + "\""
        content = content + f"\npath={path}"

        file_to_create = mod_path + "\\" + mod.mod_folder_name + ".mod"
        descriptor = open(mod_path + "\\" + mod.mod_folder_name + "\\descriptor.mod")
        descriptor_lines = descriptor.readlines()

        replaced_path = False
        for line_number in range(0, len(descriptor_lines)):
            if descriptor_lines[line_number].startswith("path="):
                descriptor_lines[line_number] = f"\npath={path}\n"
                replaced_path = True
                print(f"Edited {file_to_create}")
                file = open(file_to_create, "w+")
                file.writelines(descriptor_lines)
                file.close()

        if not replaced_path:
            descriptor_lines.append(f"\npath={path}")
            file = open(file_to_create, "w+")
            print(f"Created {file_to_create}")
            file.writelines(descriptor_lines)
            file.close()


'''UI'''
window = Tk()
window.title("Stellaris Mod Descriptor Creator")
window.geometry('500x300')
font = ('Arial', 14)

path_label = Label(window, text="Path: ", fg='black', font=font)
path_label.grid(row=0, column=0, padx=5, pady=10)
path_text = StringVar()
path_text.set("testdirectory")

path_entry = Entry(window, textvariable=path_text, fg='black', font=font)
path_entry.grid(row=0, column=1)


def start_process():
    path = path_text.get()
    desc_list = initialize_descriptors(path)
    create_descriptor_text(path, desc_list)


button = Button(window, command=start_process, text="Process", fg="black", font=font)
button.grid(row=1, column=1)


window.mainloop()

