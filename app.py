import tkinter as tk

root = tk.Tk()

root.title("Vivid Version Manager")
root.minsize(500, 500)
root.maxsize(750, 750)

label = tk.Label(root, text="Installed Versions")
label.pack()

listbox = tk.Listbox(root)
listbox.insert(1, "2.8265.999")
listbox.insert(2, "aaaa")
listbox.pack()

launchbutton = tk.Button(root, text="Launch")
launchbutton.pack()

root.mainloop()