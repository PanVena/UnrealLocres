import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import subprocess
import os

UNREALLOCRES_EXE = "UnrealLocres.exe"

def browse_file(entry, filetypes):
    path = filedialog.askopenfilename(filetypes=filetypes)
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def browse_save(entry):
    path = filedialog.asksaveasfilename(defaultextension=".locres")
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result.stdout + '\n' + result.stderr)
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

def run_export():
    input_path = export_input_entry.get()
    fmt = export_format_var.get()
    out_path = export_output_entry.get()
    if not input_path:
        return messagebox.showerror("Помилка", "Виберіть .locres файл.")
    cmd = [UNREALLOCRES_EXE, "export", input_path]
    if fmt:
        cmd += ["-f", fmt]
    if out_path:
        cmd += ["-o", out_path]
    run_command(cmd)

def run_import():
    locres_path = import_input_entry.get()
    trans_path = import_trans_entry.get()
    fmt = import_format_var.get()
    out_path = import_output_entry.get()
    if not locres_path or not trans_path:
        return messagebox.showerror("Помилка", "Вкажіть обидва файли: .locres і переклад.")
    cmd = [UNREALLOCRES_EXE, "import", locres_path, trans_path]
    if fmt:
        cmd += ["-f", fmt]
    if out_path:
        cmd += ["-o", out_path]
    run_command(cmd)

def run_merge():
    target = merge_target_entry.get()
    source = merge_source_entry.get()
    out_path = merge_output_entry.get()
    if not target or not source:
        return messagebox.showerror("Помилка", "Виберіть обидва locres-файли.")
    cmd = [UNREALLOCRES_EXE, "merge", target, source]
    if out_path:
        cmd += ["-o", out_path]
    run_command(cmd)

# --- GUI ---
root = tk.Tk()
root.title("UnrealLocres GUI")

tab_parent = tk.ttk.Notebook(root)

# === Export tab ===
export_tab = tk.Frame(tab_parent)
tab_parent.add(export_tab, text="Export")

tk.Label(export_tab, text="Locres файл:").grid(row=0, column=0, sticky='w')
export_input_entry = tk.Entry(export_tab, width=50)
export_input_entry.grid(row=0, column=1)
tk.Button(export_tab, text="Обрати", command=lambda: browse_file(export_input_entry, [("Locres", "*.locres")])).grid(row=0, column=2)

tk.Label(export_tab, text="Формат:").grid(row=1, column=0, sticky='w')
export_format_var = tk.StringVar(value="csv")
tk.OptionMenu(export_tab, export_format_var, "csv", "pot").grid(row=1, column=1, sticky='w')

tk.Label(export_tab, text="Output файл (опц.):").grid(row=2, column=0, sticky='w')
export_output_entry = tk.Entry(export_tab, width=50)
export_output_entry.grid(row=2, column=1)
tk.Button(export_tab, text="Обрати", command=lambda: browse_save(export_output_entry)).grid(row=2, column=2)

tk.Button(export_tab, text="Експортувати", command=run_export, bg="lightblue").grid(row=3, column=1, pady=5)

# === Import tab ===
import_tab = tk.Frame(tab_parent)
tab_parent.add(import_tab, text="Import")

tk.Label(import_tab, text="Оригінал .locres:").grid(row=0, column=0, sticky='w')
import_input_entry = tk.Entry(import_tab, width=50)
import_input_entry.grid(row=0, column=1)
tk.Button(import_tab, text="Обрати", command=lambda: browse_file(import_input_entry, [("Locres", "*.locres")])).grid(row=0, column=2)

tk.Label(import_tab, text="Файл перекладу:").grid(row=1, column=0, sticky='w')
import_trans_entry = tk.Entry(import_tab, width=50)
import_trans_entry.grid(row=1, column=1)
tk.Button(import_tab, text="Обрати", command=lambda: browse_file(import_trans_entry, [("CSV/POT", "*.csv *.pot")])).grid(row=1, column=2)

tk.Label(import_tab, text="Формат:").grid(row=2, column=0, sticky='w')
import_format_var = tk.StringVar(value="csv")
tk.OptionMenu(import_tab, import_format_var, "csv", "pot").grid(row=2, column=1, sticky='w')

tk.Label(import_tab, text="Output файл (опц.):").grid(row=3, column=0, sticky='w')
import_output_entry = tk.Entry(import_tab, width=50)
import_output_entry.grid(row=3, column=1)
tk.Button(import_tab, text="Обрати", command=lambda: browse_save(import_output_entry)).grid(row=3, column=2)

tk.Button(import_tab, text="Імпортувати", command=run_import, bg="lightgreen").grid(row=4, column=1, pady=5)

# === Merge tab ===
merge_tab = tk.Frame(tab_parent)
tab_parent.add(merge_tab, text="Merge")

tk.Label(merge_tab, text="Target файл:").grid(row=0, column=0, sticky='w')
merge_target_entry = tk.Entry(merge_tab, width=50)
merge_target_entry.grid(row=0, column=1)
tk.Button(merge_tab, text="Обрати", command=lambda: browse_file(merge_target_entry, [("Locres", "*.locres")])).grid(row=0, column=2)

tk.Label(merge_tab, text="Source файл:").grid(row=1, column=0, sticky='w')
merge_source_entry = tk.Entry(merge_tab, width=50)
merge_source_entry.grid(row=1, column=1)
tk.Button(merge_tab, text="Обрати", command=lambda: browse_file(merge_source_entry, [("Locres", "*.locres")])).grid(row=1, column=2)

tk.Label(merge_tab, text="Output файл (опц.):").grid(row=2, column=0, sticky='w')
merge_output_entry = tk.Entry(merge_tab, width=50)
merge_output_entry.grid(row=2, column=1)
tk.Button(merge_tab, text="Обрати", command=lambda: browse_save(merge_output_entry)).grid(row=2, column=2)

tk.Button(merge_tab, text="Змерджити", command=run_merge, bg="orange").grid(row=3, column=1, pady=5)

# === Output log ===
tab_parent.pack(expand=1, fill='both')

output_text = tk.Text(root, height=10, width=100)
output_text.pack(padx=5, pady=5)

root.mainloop()
