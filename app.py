import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import json
import shutil
from pathlib import Path
from datetime import datetime 
import uuid

root = tk.Tk()

root.title("Vivid Version Manager")
root.minsize(1000, 750)
root.maxsize(1000, 750)

frame2 = tk.Frame(root)

frame = tk.Frame(root)

frame3 = tk.Frame(root)

frame2.pack(side="bottom", fill="x")

frame.pack(side="left", fill="both", expand=True)

frame3.pack(side="right", fill="both", expand=True)

version_title = tk.Label(frame3, text="No version selected", font=("Arial", 16))
version_title.pack(anchor="nw", padx=20, pady=20)

version_number = tk.Label(frame3, text="")
version_number.pack(anchor="nw", padx=20)

version_path = tk.Label(frame3, text="")
version_path.pack(anchor="nw", padx=20)

label = tk.Label(frame, text="Installed Versions")
label.pack(fill="x")

verlist = ttk.Treeview(
    frame, 
    columns=("version",), 
    show="tree headings"
    )
verlist.heading("#0", text="Title")
verlist.heading("version", text="Version")

with open("verlist.json", "r") as file:
    data = json.load(file)

with open("data/settings.json", "r") as file:
    settings = json.load(file)

active_version_id = settings["active_version_id"]

print(f"Active save profile: {active_version_id}")
print(10*"-")

print(data)
print(10*"-")

version_entries = {}

for version in data["versions"]:
    item_id = verlist.insert(
        "",
        tk.END,
        text=version["title"],
        values=(version["version"],)
    )

    version_entries[item_id] = version

verlist.bind("<<TreeviewSelect>>", lambda event: selection())

verlist.pack(fill="both", expand=True)


def selection():
    selected_items = verlist.selection()

    if not selected_items:
        print("No version selected.")
        return

    selected_item = selected_items[0]

    title = verlist.item(selected_item, "text")
    version = verlist.item(selected_item, "values")[0]

    version_title.config(text=title)
    version_number.config(text=f"Version: {version}")
    version_path.config(text=f"Location: {version_entries[selected_item]['executable']}")

    print(f"Selected; {title} ({version})")

def add_version():
    add_window = tk.Toplevel(root)
    add_window.title("Add Version")
    add_window.geometry("400x300")
    add_window.resizable(False, False)
    title_label = tk.Label(add_window, text="Version Title:")
    title_label.pack()

    title_entry = tk.Entry(add_window)
    title_entry.pack()

    version_label = tk.Label(add_window, text="Version Number:")
    version_label.pack()

    version_entry = tk.Entry(add_window)
    version_entry.pack()

    id_label = tk.Label(add_window, text="Version ID:")
    id_label.pack()

    id_entry = tk.Entry(add_window)
    id_entry.pack()

    executable_label = tk.Label(add_window, text="Executable:")
    executable_label.pack()

    executable_entry = tk.Entry(add_window, width=40)
    executable_entry.pack()

    def browse_executable():
        path = filedialog.askopenfilename(
            title="Select VIVIDSTASIS.exe",
            filetypes=[("Executable", "*.exe")]
        )

        if path:
            executable_entry.delete(0, tk.END)
            executable_entry.insert(0, path)


    browse_button = tk.Button(
        add_window,
        text="Browse...",
        command=browse_executable
    )
    browse_button.pack()

    def save_version():
        title = title_entry.get().strip()
        version = version_entry.get().strip()
        version_id = id_entry.get().strip()
        executable = executable_entry.get().strip()

        if not title or not version or not version_id or not executable:
            messagebox.showerror(
            "Invalid Version",
            "Please fill in all fields."
            )
            return

        for existing_version in data["versions"]:
            if existing_version["id"] == version_id:
                messagebox.showerror(
                    "Duplicate Version ID",
                    "This version ID is already in use."
                )
                return

        for existing_version in data["versions"]:
            if os.path.normcase(os.path.abspath(existing_version["executable"])) == os.path.normcase(os.path.abspath(executable)):
                messagebox.showerror(
                    "Duplicate Installation",
                    "This executable is already registered."
                )
                return

        if not os.path.isfile(executable):
            messagebox.showerror(
                "Invalid Executable",
                "The selected executable does not exist."
                )
            return

        if os.path.basename(executable).lower() != "vividstasis.exe":
            messagebox.showerror(
                "Invalid Executable",
                "Please select VIVIDSTASIS.exe."
                )
            return

        new_version = {
            "id": version_id,
            "title": title,
            "version": version,
            "executable": executable
            }
        data["versions"].append(new_version)
        with open("verlist.json", "w") as file:
            json.dump(data, file, indent=4)

        item_id = verlist.insert(
            "",
            tk.END,
            text=title,
            values=(version,)
        )

        version_entries[item_id] = new_version

        add_window.destroy()

    add_button = tk.Button(
        add_window,
        text="Add Version",
        command=save_version
    )
    add_button.pack()

with open("verlist.json") as f:
    contents = f.read()
    versioncount = contents.count("title")

def game_is_running():
    result = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq VIVIDSTASIS.exe", "/FO", "CSV", "/NH"],
        capture_output=True,
        text=True
    )

    return "VIVIDSTASIS.exe" in result.stdout

def backup_active_save():
    if game_is_running():
        print("Cannot back up saves while vivid/stasis is running!")
        return False

    save_directory = Path(os.environ["LOCALAPPDATA"]) / "VIVIDSTASIS"

    backup_directory = Path("data") / "backups"

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")

    backup_path = backup_directory / f"active-save-{timestamp}"

    if not save_directory.is_dir():
        print("Save directory does not exist!")
        return False

    try:
        backup_directory.mkdir(parents=True, exist_ok=True)
        shutil.copytree(save_directory, backup_path)
    except OSError as error:
        print(f"Could not create save backup: {error}")
        return False

    profile_directory = Path("data") / "saves" / active_version_id

    profile_staging = profile_directory.parent / f"{active_version_id}-staging-{uuid.uuid4().hex}"
    profile_rollback = profile_directory.parent / f"{active_version_id}-rollback-{uuid.uuid4().hex}"

    try:
        profile_directory.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(save_directory, profile_staging)

        if profile_directory.exists():
            profile_directory.rename(profile_rollback)

        try:
            profile_staging.rename(profile_directory)
        except Exception:
            if profile_rollback.exists():
                profile_rollback.rename(profile_directory)
            raise

        if profile_rollback.exists():
            try:
                shutil.rmtree(profile_rollback)
            except OSError as error:
                print(f"Warning: Could not remove old profile: {error}")

    except Exception as error:
        print(f"Profile backup failed: {error}")
        return False

    finally:
        if profile_staging.exists():
            try:
                shutil.rmtree(profile_staging)
            except Exception as error:
                print(f"Warning: Could not remove staging directory: {error}") 

    print(f"Version profile updated: {active_version_id}")

    print(f"Save backup created: {backup_path}")

    return True

def save_settings():
    settings["active_version_id"] = active_version_id

    with open("data/settings.json", "w") as file:
        json.dump(settings, file, indent=4)

def restore_save_profile(version_id):
    global active_version_id

    if game_is_running():
        print("Cannot restore saves while vivid/stasis is running!")
        return False

    profile_directory = Path("data") / "saves" / version_id
    save_directory = Path(os.environ["LOCALAPPDATA"]) / "VIVIDSTASIS"

    if not profile_directory.is_dir():
        print(f"No save profile exists for {version_id}. Creating a new one...")
        profile_directory.mkdir(parents=True, exist_ok=True)

    if not save_directory.is_dir():
        print("Active save directory does not exist!")
        return False

    staging_directory = save_directory.parent / f"VIVIDSTASIS-staging-{uuid.uuid4().hex}"
    rollback_directory = save_directory.parent / f"VIVIDSTASIS-rollback-{uuid.uuid4().hex}"

    try:
        shutil.copytree(profile_directory, staging_directory)
        print(f"Profile staged: {version_id}")

        save_directory.rename(rollback_directory)

        try:
            staging_directory.rename(save_directory)
        except Exception:
            rollback_directory.rename(save_directory)
            raise

        previous_version_id = active_version_id
        active_version_id = version_id

        try:
            save_settings()
        except Exception:
            active_version_id = previous_version_id

            save_directory.rename(staging_directory)
            rollback_directory.rename(save_directory)

            raise

        try:
            shutil.rmtree(rollback_directory)
        except OSError as error:
            print(f"Warning: Could not remove rollback directory: {error}")

        print(f"Restored save profile: {version_id}")

        return True

    except Exception as error:
        print(f"Save restoration failed: {error}")
        return False

    finally:
        if staging_directory.exists():
            try:
                shutil.rmtree(staging_directory)
            except Exception as error:
                print(f"Warning: Could not remove staging directory: {error}")

def launch():
    if game_is_running():
        print("Vivid/stasis is already running! Close it first.")
        return
    
    selected_items = verlist.selection()

    if not selected_items:
        print("Please select a version first.")
        return

    selected_item = selected_items[0]

    version = version_entries[selected_item]

    executable = version["executable"]
    version_id = version["id"]

    if not os.path.isfile(executable):
        print("Executable not found!")
        return

    if version_id != active_version_id:
        if not backup_active_save():
            print("Could not back up the active save. Launch cancelled.")
            return
        if not restore_save_profile(version_id):
            print("Could not restore the selected save profile. Launch Cancelled.")
            return

    print(f"Launching {version['title']}")
    print(f"Save profile: {version_id}")

    game_directory = os.path.dirname(executable)

    subprocess.Popen([executable], cwd=game_directory)


launch_button = tk.Button(
    frame2, 
    text="Launch", 
    command=launch
    )

launch_button.pack(side="left", expand=True, pady=10)

backup_button = tk.Button(
    frame2,
    text="Backup Active Save",
    command=backup_active_save
)

backup_button.pack(side="left", expand=True, pady=10)

add_version_button = tk.Button(
    frame2,
    text="Add Version",
    command=add_version
)

add_version_button.pack(side="left", expand=True, pady=10)

label = tk.Label(frame, text=f"Versions Installed: {versioncount}")
label.pack(fill="x")

root.mainloop()