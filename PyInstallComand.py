import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess
import sys

# ─── Локалізація / Localiation ───────────────────────────────────────────────────────────────
LANG = {
    "en": {
        "title": "PyInstaller Command Generator",
        "tab_main": "Main",
        "tab_advanced": "Advanced",
        "tab_output": "Generated Command",
        "script_file": "Script File (.py)",
        "browse": "Browse",
        "app_name": "App Name (--name)",
        "icon_file": "Icon File (.ico)",
        "one_file": "Single file (--onefile)",
        "windowed": "No console window (--windowed)",
        "clean": "Clean build (--clean)",
        "upx": "Compress with UPX (--upx-dir)",
        "debug": "Debug mode (--debug all)",
        "add_data": "Add Data Files (--add-data)",
        "add_data_btn": "Add File/Folder",
        "add_data_list": "Added data:",
        "remove_selected": "Remove Selected",
        "hidden_imports": "Hidden Imports (comma separated)",
        "extra_hooks": "Extra Hook Dirs",
        "extra_hooks_btn": "Browse Folder",
        "dist_path": "Output (--distpath)",
        "dist_path_btn": "Browse Folder",
        "work_path": "Work Dir (--workpath)",
        "work_path_btn": "Browse Folder",
        "generate": "⚡ Generate Command",
        "copy": "Copy to Clipboard",
        "run_pyinstaller": "▶ Run via PyInstaller",
        "run_python": "▶ Run via Python",
        "clear": "Clear All",
        "lang_btn": "🇺🇦 Українська",
        "no_script": "Please select a script file (.py)!",
        "copied": "Command copied to clipboard!",
        "running": "Running...",
        "success": "Done! Check the dist/ folder.",
        "error": "Error",
        "placeholder_name": "MyApp",
        "placeholder_hidden": "e.g. sklearn, PIL",
        "data_sep": "Files separator: SOURCE;DEST (Windows) or SOURCE:DEST (Linux/Mac)",
        "add_data_dialog": "Select file or folder to add",
        "dest_dialog": "Enter destination folder name (in the app bundle):",
        "dest_default": ".",
    },
    "uk": {
        "title": "Генератор команд PyInstaller",
        "tab_main": "Основне",
        "tab_advanced": "Додатково",
        "tab_output": "Згенерована команда",
        "script_file": "Файл скрипту (.py)",
        "browse": "Вибрати",
        "app_name": "Назва програми (--name)",
        "icon_file": "Іконка (.ico)",
        "one_file": "Один файл (--onefile)",
        "windowed": "Без консолі (--windowed)",
        "clean": "Очистити перед збіркою (--clean)",
        "upx": "Стиснути UPX (--upx-dir)",
        "debug": "Режим налагодження (--debug all)",
        "add_data": "Додати файли/папки (--add-data)",
        "add_data_btn": "Додати файл/папку",
        "add_data_list": "Додані дані:",
        "remove_selected": "Видалити вибране",
        "hidden_imports": "Приховані імпорти (через кому)",
        "extra_hooks": "Додаткові хук-директорії",
        "extra_hooks_btn": "Вибрати папку",
        "dist_path": "Папка виводу (--distpath)",
        "dist_path_btn": "Вибрати папку",
        "work_path": "Робоча папка (--workpath)",
        "work_path_btn": "Вибрати папку",
        "generate": "⚡ Згенерувати команду",
        "copy": "Копіювати в буфер",
        "run_pyinstaller": "▶ Запустити через PyInstaller",
        "run_python": "▶ Запустити через Python",
        "clear": "Очистити все",
        "lang_btn": "🇬🇧 English",
        "no_script": "Будь ласка, виберіть файл скрипту (.py)!",
        "copied": "Команду скопійовано в буфер обміну!",
        "running": "Виконується...",
        "success": "Готово! Перевірте папку dist/.",
        "error": "Помилка",
        "placeholder_name": "МояПрограма",
        "placeholder_hidden": "напр. sklearn, PIL",
        "data_sep": "Роздільник файлів: ДЖЕРЕЛО;ЦІЛЬ (Windows) або ДЖЕРЕЛО:ЦІЛЬ (Linux/Mac)",
        "add_data_dialog": "Виберіть файл або папку для додавання",
        "dest_dialog": "Введіть назву папки призначення (у пакеті програми):",
        "dest_default": ".",
    },
}

# ─── App ────────────────────────────────────────────────────────────────────────
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_lang = "uk"
        self.data_entries = []  # list of (source, dest) strings

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(self.t("title"))
        self.geometry("860x720")
        self.minsize(780, 640)
        self.resizable(True, True)

        self._build_ui()

    def t(self, key):
        return LANG[self.current_lang].get(key, key)

    # ── UI ──────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Top bar
        top = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color=("#1a1a2e", "#0f0f23"))
        top.pack(fill="x")
        top.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            top, text=self.t("title"),
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#4fc3f7"
        )
        self.title_label.pack(side="left", padx=20, pady=10)

        self.lang_btn = ctk.CTkButton(
            top, text=self.t("lang_btn"), width=130,
            fg_color="#1565c0", hover_color="#0d47a1",
            command=self._toggle_lang
        )
        self.lang_btn.pack(side="right", padx=15, pady=8)

        # Tabs
        self.tabs = ctk.CTkTabview(self, corner_radius=10)
        self.tabs.pack(fill="both", expand=True, padx=15, pady=(8, 5))

        self.tab_main = self.tabs.add(self.t("tab_main"))
        self.tab_adv = self.tabs.add(self.t("tab_advanced"))
        self.tab_out = self.tabs.add(self.t("tab_output"))

        self._build_main_tab()
        self._build_advanced_tab()
        self._build_output_tab()

        # Bottom buttons
        self._build_bottom_bar()

    def _build_main_tab(self):
        f = self.tab_main
        f.grid_columnconfigure(1, weight=1)

        row = 0
        # Script file
        self.lbl_script = ctk.CTkLabel(f, text=self.t("script_file"), anchor="w")
        self.lbl_script.grid(row=row, column=0, sticky="w", padx=15, pady=(18, 4))
        sf = ctk.CTkFrame(f, fg_color="transparent")
        sf.grid(row=row, column=1, sticky="ew", padx=(0, 15), pady=(18, 4))
        sf.grid_columnconfigure(0, weight=1)
        self.script_var = ctk.StringVar()
        self.script_entry = ctk.CTkEntry(sf, textvariable=self.script_var, placeholder_text="main.py")
        self.script_entry.grid(row=0, column=0, sticky="ew")
        self.btn_browse_script = ctk.CTkButton(sf, text=self.t("browse"), width=80, command=self._browse_script)
        self.btn_browse_script.grid(row=0, column=1, padx=(6, 0))

        row += 1
        # App name
        self.lbl_name = ctk.CTkLabel(f, text=self.t("app_name"), anchor="w")
        self.lbl_name.grid(row=row, column=0, sticky="w", padx=15, pady=4)
        self.name_var = ctk.StringVar()
        self.name_entry = ctk.CTkEntry(f, textvariable=self.name_var, placeholder_text=self.t("placeholder_name"))
        self.name_entry.grid(row=row, column=1, sticky="ew", padx=(0, 15), pady=4)

        row += 1
        # Icon
        self.lbl_icon = ctk.CTkLabel(f, text=self.t("icon_file"), anchor="w")
        self.lbl_icon.grid(row=row, column=0, sticky="w", padx=15, pady=4)
        icf = ctk.CTkFrame(f, fg_color="transparent")
        icf.grid(row=row, column=1, sticky="ew", padx=(0, 15), pady=4)
        icf.grid_columnconfigure(0, weight=1)
        self.icon_var = ctk.StringVar()
        self.icon_entry = ctk.CTkEntry(icf, textvariable=self.icon_var, placeholder_text="app.ico")
        self.icon_entry.grid(row=0, column=0, sticky="ew")
        self.btn_browse_icon = ctk.CTkButton(icf, text=self.t("browse"), width=80, command=self._browse_icon)
        self.btn_browse_icon.grid(row=0, column=1, padx=(6, 0))

        row += 1
        # Separator
        ctk.CTkLabel(f, text="", height=4).grid(row=row, column=0, columnspan=2)

        row += 1
        # Checkboxes frame
        chk_frame = ctk.CTkFrame(f, fg_color=("#e8eaf6", "#1a1a3e"), corner_radius=10)
        chk_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=15, pady=6)
        chk_frame.grid_columnconfigure((0, 1), weight=1)

        self.var_onefile = ctk.BooleanVar(value=True)
        self.var_windowed = ctk.BooleanVar()
        self.var_clean = ctk.BooleanVar()
        self.var_upx = ctk.BooleanVar()
        self.var_debug = ctk.BooleanVar()

        self.chk_onefile = ctk.CTkCheckBox(chk_frame, text=self.t("one_file"), variable=self.var_onefile)
        self.chk_onefile.grid(row=0, column=0, sticky="w", padx=20, pady=8)
        self.chk_windowed = ctk.CTkCheckBox(chk_frame, text=self.t("windowed"), variable=self.var_windowed)
        self.chk_windowed.grid(row=0, column=1, sticky="w", padx=20, pady=8)
        self.chk_clean = ctk.CTkCheckBox(chk_frame, text=self.t("clean"), variable=self.var_clean)
        self.chk_clean.grid(row=1, column=0, sticky="w", padx=20, pady=8)
        self.chk_upx = ctk.CTkCheckBox(chk_frame, text=self.t("upx"), variable=self.var_upx)
        self.chk_upx.grid(row=1, column=1, sticky="w", padx=20, pady=8)
        self.chk_debug = ctk.CTkCheckBox(chk_frame, text=self.t("debug"), variable=self.var_debug)
        self.chk_debug.grid(row=2, column=0, sticky="w", padx=20, pady=8)

    def _build_advanced_tab(self):
        f = self.tab_adv
        f.grid_columnconfigure(1, weight=1)

        row = 0
        # Add data
        self.lbl_adddata = ctk.CTkLabel(f, text=self.t("add_data"), anchor="w",
                                         font=ctk.CTkFont(weight="bold"))
        self.lbl_adddata.grid(row=row, column=0, columnspan=2, sticky="w", padx=15, pady=(16, 4))

        row += 1
        self.btn_add_data = ctk.CTkButton(f, text=self.t("add_data_btn"), command=self._add_data_file)
        self.btn_add_data.grid(row=row, column=0, sticky="w", padx=15, pady=4)
        self.btn_remove_data = ctk.CTkButton(f, text=self.t("remove_selected"),
                                              fg_color="#b71c1c", hover_color="#7f0000",
                                              command=self._remove_data_entry)
        self.btn_remove_data.grid(row=row, column=1, sticky="w", padx=6, pady=4)

        row += 1
        self.data_listbox = ctk.CTkTextbox(f, height=90, state="disabled",
                                            fg_color=("#f5f5f5", "#12122a"))
        self.data_listbox.grid(row=row, column=0, columnspan=2, sticky="ew", padx=15, pady=4)

        row += 1
        ctk.CTkLabel(f, text="", height=6).grid(row=row, column=0)

        row += 1
        # Hidden imports
        self.lbl_hidden = ctk.CTkLabel(f, text=self.t("hidden_imports"), anchor="w")
        self.lbl_hidden.grid(row=row, column=0, sticky="w", padx=15, pady=4)
        self.hidden_var = ctk.StringVar()
        self.hidden_entry = ctk.CTkEntry(f, textvariable=self.hidden_var,
                                          placeholder_text=self.t("placeholder_hidden"))
        self.hidden_entry.grid(row=row, column=1, sticky="ew", padx=(0, 15), pady=4)

        row += 1
        # Extra hooks
        self.lbl_hooks = ctk.CTkLabel(f, text=self.t("extra_hooks"), anchor="w")
        self.lbl_hooks.grid(row=row, column=0, sticky="w", padx=15, pady=4)
        hf = ctk.CTkFrame(f, fg_color="transparent")
        hf.grid(row=row, column=1, sticky="ew", padx=(0, 15), pady=4)
        hf.grid_columnconfigure(0, weight=1)
        self.hooks_var = ctk.StringVar()
        self.hooks_entry = ctk.CTkEntry(hf, textvariable=self.hooks_var)
        self.hooks_entry.grid(row=0, column=0, sticky="ew")
        self.btn_hooks = ctk.CTkButton(hf, text=self.t("extra_hooks_btn"), width=100,
                                        command=lambda: self._browse_folder(self.hooks_var))
        self.btn_hooks.grid(row=0, column=1, padx=(6, 0))

        row += 1
        ctk.CTkLabel(f, text="", height=6).grid(row=row, column=0)

        row += 1
        # Dist path
        self.lbl_dist = ctk.CTkLabel(f, text=self.t("dist_path"), anchor="w")
        self.lbl_dist.grid(row=row, column=0, sticky="w", padx=15, pady=4)
        df = ctk.CTkFrame(f, fg_color="transparent")
        df.grid(row=row, column=1, sticky="ew", padx=(0, 15), pady=4)
        df.grid_columnconfigure(0, weight=1)
        self.dist_var = ctk.StringVar()
        self.dist_entry = ctk.CTkEntry(df, textvariable=self.dist_var, placeholder_text="dist")
        self.dist_entry.grid(row=0, column=0, sticky="ew")
        self.btn_dist = ctk.CTkButton(df, text=self.t("dist_path_btn"), width=100,
                                       command=lambda: self._browse_folder(self.dist_var))
        self.btn_dist.grid(row=0, column=1, padx=(6, 0))

        row += 1
        # Work path
        self.lbl_work = ctk.CTkLabel(f, text=self.t("work_path"), anchor="w")
        self.lbl_work.grid(row=row, column=0, sticky="w", padx=15, pady=4)
        wf = ctk.CTkFrame(f, fg_color="transparent")
        wf.grid(row=row, column=1, sticky="ew", padx=(0, 15), pady=4)
        wf.grid_columnconfigure(0, weight=1)
        self.work_var = ctk.StringVar()
        self.work_entry = ctk.CTkEntry(wf, textvariable=self.work_var, placeholder_text="build")
        self.work_entry.grid(row=0, column=0, sticky="ew")
        self.btn_work = ctk.CTkButton(wf, text=self.t("work_path_btn"), width=100,
                                       command=lambda: self._browse_folder(self.work_var))
        self.btn_work.grid(row=0, column=1, padx=(6, 0))

    def _build_output_tab(self):
        f = self.tab_out
        f.grid_columnconfigure(0, weight=1)
        f.grid_rowconfigure(0, weight=1)

        self.output_text = ctk.CTkTextbox(f, font=ctk.CTkFont(family="Courier", size=13),
                                           fg_color=("#f0f0f0", "#0d0d1a"),
                                           text_color=("#1a1a1a", "#4fc3f7"),
                                           corner_radius=8)
        self.output_text.grid(row=0, column=0, sticky="nsew", padx=15, pady=(15, 8))

        btn_row = ctk.CTkFrame(f, fg_color="transparent")
        btn_row.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))
        btn_row.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_copy = ctk.CTkButton(btn_row, text=self.t("copy"),
                                       fg_color="#1565c0", hover_color="#0d47a1",
                                       command=self._copy_command)
        self.btn_copy.grid(row=0, column=0, sticky="ew", padx=4)

        self.btn_run_pi = ctk.CTkButton(btn_row, text=self.t("run_pyinstaller"),
                                         fg_color="#1b5e20", hover_color="#0a3d0a",
                                         command=lambda: self._run_command("pyinstaller"))
        self.btn_run_pi.grid(row=0, column=1, sticky="ew", padx=4)

        self.btn_run_py = ctk.CTkButton(btn_row, text=self.t("run_python"),
                                         fg_color="#4a148c", hover_color="#2d0058",
                                         command=lambda: self._run_command("python"))
        self.btn_run_py.grid(row=0, column=2, sticky="ew", padx=4)

    def _build_bottom_bar(self):
        bar = ctk.CTkFrame(self, height=55, corner_radius=0, fg_color=("#e8eaf6", "#0f0f23"))
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        bar.grid_columnconfigure(0, weight=1)

        self.btn_generate = ctk.CTkButton(
            bar, text=self.t("generate"),
            font=ctk.CTkFont(size=15, weight="bold"),
            height=38, fg_color="#1565c0", hover_color="#0d47a1",
            command=self._generate
        )
        self.btn_generate.pack(side="left", padx=15, pady=8)

        self.btn_clear = ctk.CTkButton(
            bar, text=self.t("clear"), height=38, width=110,
            fg_color="#37474f", hover_color="#263238",
            command=self._clear_all
        )
        self.btn_clear.pack(side="right", padx=15, pady=8)

        self.status_label = ctk.CTkLabel(bar, text="", text_color="#4fc3f7",
                                          font=ctk.CTkFont(size=12))
        self.status_label.pack(side="left", padx=10, pady=8)

    # ── Actions ─────────────────────────────────────────────────────────────────
    def _toggle_lang(self):
        self.current_lang = "en" if self.current_lang == "uk" else "uk"
        self._refresh_ui()

    def _refresh_ui(self):
        self.title(self.t("title"))
        self.title_label.configure(text=self.t("title"))
        self.lang_btn.configure(text=self.t("lang_btn"))

        # Tabs – rename
        self.tabs.rename(list(self.tabs._name_list)[0], self.t("tab_main"))
        self.tabs.rename(list(self.tabs._name_list)[1], self.t("tab_advanced"))
        self.tabs.rename(list(self.tabs._name_list)[2], self.t("tab_output"))

        # Main tab labels
        self.lbl_script.configure(text=self.t("script_file"))
        self.btn_browse_script.configure(text=self.t("browse"))
        self.lbl_name.configure(text=self.t("app_name"))
        self.lbl_icon.configure(text=self.t("icon_file"))
        self.btn_browse_icon.configure(text=self.t("browse"))
        self.chk_onefile.configure(text=self.t("one_file"))
        self.chk_windowed.configure(text=self.t("windowed"))
        self.chk_clean.configure(text=self.t("clean"))
        self.chk_upx.configure(text=self.t("upx"))
        self.chk_debug.configure(text=self.t("debug"))

        # Advanced tab labels
        self.lbl_adddata.configure(text=self.t("add_data"))
        self.btn_add_data.configure(text=self.t("add_data_btn"))
        self.btn_remove_data.configure(text=self.t("remove_selected"))
        self.lbl_hidden.configure(text=self.t("hidden_imports"))
        self.lbl_hooks.configure(text=self.t("extra_hooks"))
        self.btn_hooks.configure(text=self.t("extra_hooks_btn"))
        self.lbl_dist.configure(text=self.t("dist_path"))
        self.btn_dist.configure(text=self.t("dist_path_btn"))
        self.lbl_work.configure(text=self.t("work_path"))
        self.btn_work.configure(text=self.t("work_path_btn"))

        # Output tab
        self.btn_copy.configure(text=self.t("copy"))
        self.btn_run_pi.configure(text=self.t("run_pyinstaller"))
        self.btn_run_py.configure(text=self.t("run_python"))

        # Bottom bar
        self.btn_generate.configure(text=self.t("generate"))
        self.btn_clear.configure(text=self.t("clear"))

    def _browse_script(self):
        path = filedialog.askopenfilename(filetypes=[("Python files", "*.py"), ("All", "*.*")])
        if path:
            self.script_var.set(path)
            if not self.name_var.get():
                self.name_var.set(os.path.splitext(os.path.basename(path))[0])

    def _browse_icon(self):
        path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico"), ("All", "*.*")])
        if path:
            self.icon_var.set(path)

    def _browse_folder(self, var):
        path = filedialog.askdirectory()
        if path:
            var.set(path)

    def _add_data_file(self):
        path = filedialog.askopenfilename(title=self.t("add_data_dialog"))
        if not path:
            path = filedialog.askdirectory(title=self.t("add_data_dialog"))
        if not path:
            return
        dest = ctk.CTkInputDialog(
            text=self.t("dest_dialog"),
            title="Destination"
        ).get_input()
        if dest is None:
            dest = self.t("dest_default")
        sep = ";" if sys.platform == "win32" else ":"
        entry = f"{path}{sep}{dest}"
        self.data_entries.append(entry)
        self._refresh_data_list()

    def _remove_data_entry(self):
        if self.data_entries:
            self.data_entries.pop()
            self._refresh_data_list()

    def _refresh_data_list(self):
        self.data_listbox.configure(state="normal")
        self.data_listbox.delete("0.0", "end")
        for e in self.data_entries:
            self.data_listbox.insert("end", e + "\n")
        self.data_listbox.configure(state="disabled")

    def _build_command(self, runner="pyinstaller"):
        script = self.script_var.get().strip()
        if not script:
            return None, self.t("no_script")

        parts = []
        if runner == "python":
            parts.append(f'python -m PyInstaller')
        else:
            parts.append("pyinstaller")

        if self.var_onefile.get():
            parts.append("--onefile")
        if self.var_windowed.get():
            parts.append("--windowed")
        if self.var_clean.get():
            parts.append("--clean")
        if self.var_debug.get():
            parts.append("--debug all")

        name = self.name_var.get().strip()
        if name:
            parts.append(f'--name "{name}"')

        icon = self.icon_var.get().strip()
        if icon:
            parts.append(f'--icon "{icon}"')

        for entry in self.data_entries:
            parts.append(f'--add-data "{entry}"')

        hidden = self.hidden_var.get().strip()
        if hidden:
            for imp in [x.strip() for x in hidden.split(",") if x.strip()]:
                parts.append(f"--hidden-import {imp}")

        hooks = self.hooks_var.get().strip()
        if hooks:
            parts.append(f'--additional-hooks-dir "{hooks}"')

        dist = self.dist_var.get().strip()
        if dist:
            parts.append(f'--distpath "{dist}"')

        work = self.work_var.get().strip()
        if work:
            parts.append(f'--workpath "{work}"')

        if self.var_upx.get():
            parts.append("--upx-dir upx")

        parts.append(f'"{script}"')
        cmd = " \\\n    ".join(parts)
        return cmd, None

    def _generate(self):
        cmd, err = self._build_command()
        if err:
            messagebox.showwarning(self.t("error"), err)
            return
        self.output_text.configure(state="normal")
        self.output_text.delete("0.0", "end")
        self.output_text.insert("end", cmd)
        self.output_text.configure(state="disabled")
        self.tabs.set(self.t("tab_output"))
        self.status_label.configure(text="✅ OK")

    def _copy_command(self):
        cmd_text = self.output_text.get("0.0", "end").strip()
        if cmd_text:
            self.clipboard_clear()
            self.clipboard_append(cmd_text)
            self.status_label.configure(text=self.t("copied"))

    def _run_command(self, runner):
        cmd, err = self._build_command(runner)
        if err:
            messagebox.showwarning(self.t("error"), err)
            return
        # Flatten for execution
        flat_cmd = cmd.replace(" \\\n    ", " ")
        self.status_label.configure(text=self.t("running"))
        self.update()
        try:
            result = subprocess.run(flat_cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("✅", self.t("success"))
                self.status_label.configure(text="✅ Done")
            else:
                messagebox.showerror(self.t("error"), result.stderr[-1200:] if result.stderr else "Unknown error")
                self.status_label.configure(text="❌ Error")
        except Exception as exc:
            messagebox.showerror(self.t("error"), str(exc))
            self.status_label.configure(text="❌ Error")

    def _clear_all(self):
        self.script_var.set("")
        self.name_var.set("")
        self.icon_var.set("")
        self.hidden_var.set("")
        self.hooks_var.set("")
        self.dist_var.set("")
        self.work_var.set("")
        self.var_onefile.set(True)
        self.var_windowed.set(False)
        self.var_clean.set(False)
        self.var_upx.set(False)
        self.var_debug.set(False)
        self.data_entries.clear()
        self._refresh_data_list()
        self.output_text.configure(state="normal")
        self.output_text.delete("0.0", "end")
        self.output_text.configure(state="disabled")
        self.status_label.configure(text="")


if __name__ == "__main__":
    app = App()

    app.mainloop()
