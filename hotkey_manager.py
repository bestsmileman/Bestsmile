import tkinter as tk
from tkinter import ttk
import json
import os
from tksheet import Sheet

DATA_FILE = "manual_hotkeys.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data_json = json.load(f)
        except:
            data_json = []
else:
    data_json = []

root = tk.Tk()
root.title("Hotkey Manager v7 - Full Spec Preview")
root.geometry("1024x600")

lang_var = tk.StringVar(value="ko")
lang_dropdown = ttk.Combobox(root, textvariable=lang_var, values=["ko", "en"], width=5)
lang_dropdown.place(x=970, y=5)

top_padding = tk.Frame(root, height=84)
top_padding.pack()

label = tk.Label(root, text="데이터 셀을 클릭하여 수정, 입력 및 삭제", font=("맑은 고딕", 12))
label.pack()

frame = tk.Frame(root)
frame.pack(expand=True, fill="both", padx=10)

headers = ["app", "hotkey", "간이", "중복", "우선", "type"]
num_rows = 20
table_data = [[
    entry.get("app", ""),
    entry.get("hotkey", ""),
    entry.get("simple", ""),
    entry.get("duplicate", ""),
    entry.get("priority", ""),
    entry.get("type", "")
] for entry in data_json]

while len(table_data) < num_rows:
    table_data.append(["" for _ in headers])

sheet = Sheet(frame,
              data=table_data,
              headers=headers,
              show_row_index=True,
              show_header=True)

sheet.enable_bindings((
    "single_select",
    "row_select",
    "column_select",
    "arrowkeys",
    "right_click_popup_menu",
    "rc_select",
    "rc_insert_row",
    "rc_delete_row",
    "rc_insert_column",
    "rc_delete_column",
    "edit_cell"))

sheet.grid(row=0, column=0, sticky="nswe")
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

sheet.set_all_column_widths(160)
sheet.set_row_heights([24]*num_rows)

def save_data():
    updated = sheet.get_sheet_data(return_copy=True)
    json_data = []
    for row in updated:
        if any(cell.strip() for cell in row):
            json_data.append({
                "app": row[0],
                "hotkey": row[1],
                "simple": row[2],
                "duplicate": row[3],
                "priority": row[4],
                "type": row[5],
            })
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

bottom_frame = tk.Frame(root, height=48)
bottom_frame.pack(fill="x")

save_button = tk.Button(bottom_frame, text="HTML로 보기/인쇄", command=save_data)
save_button.pack(pady=10)

root.mainloop()
