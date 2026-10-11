import json
import os
import socket
import subprocess
import sys
import threading
from pathlib import Path
from queue import Empty, Queue
from tkinter import END, BOTH, LEFT, RIGHT, SINGLE, VERTICAL, X, Y, filedialog, messagebox, ttk
import tkinter as tk


APP_TITLE = "PDF Merge Tool"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 39271
BUFFER_SIZE = 65536


class MissingBackendError(RuntimeError):
    pass


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def vendor_dir() -> Path:
    return app_dir() / "vendor"


def vendor_search_dirs() -> list[Path]:
    candidates: list[Path] = []
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates.append(Path(meipass) / "vendor")
    candidates.append(vendor_dir())

    unique: list[Path] = []
    seen: set[str] = set()
    for path in candidates:
        key = str(path).lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(path)
    return unique


def show_missing_backend_message() -> None:
    messagebox.showerror(
        "Missing dependency",
        "The PDF merge backend is unavailable.\n\n"
        "Install 'pypdf' into the app's vendor folder, or rebuild the EXE after bundling pypdf.",
    )


def normalize_files(paths: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for raw_path in paths:
        if not raw_path:
            continue
        path = Path(raw_path).expanduser().resolve()
        if not path.exists() or path.suffix.lower() != ".pdf":
            continue
        key = str(path).lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(str(path))
    return normalized


def install_pypdf() -> bool:
    target = vendor_dir()
    target.mkdir(parents=True, exist_ok=True)

    command_candidates: list[list[str]] = []
    if not getattr(sys, "frozen", False):
        command_candidates.append([sys.executable, "-m", "pip"])
    command_candidates.extend([
        ["py", "-m", "pip"],
        ["python", "-m", "pip"],
    ])

    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    attempts: list[str] = []
    seen: set[tuple[str, ...]] = set()
    for base_command in command_candidates:
        key = tuple(base_command)
        if key in seen:
            continue
        seen.add(key)
        command = [
            *base_command,
            "install",
            "--disable-pip-version-check",
            "--no-warn-script-location",
            "--target",
            str(target),
            "pypdf",
        ]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                creationflags=creationflags,
            )
        except OSError as exc:
            attempts.append(f"{' '.join(command)}\n{exc}")
            continue

        if result.returncode == 0:
            return True

        details = (result.stderr or result.stdout or "").strip() or "Unknown error"
        attempts.append(f"{' '.join(command)}\n{details}")

    if getattr(sys, "frozen", False):
        details = "No usable Python/pip launcher was found."
        if attempts:
            details = "\n\n".join(attempts)
    else:
        details = "\n\n".join(attempts) if attempts else "Unknown error"

    messagebox.showerror(
        "Install failed",
        "Could not install pypdf automatically.\n\n"
        "Please check your Python/pip installation and network connection, then try again.\n\n"
        f"Details:\n{details}",
    )
    return False


def ensure_pypdf():
    local_vendor = vendor_dir()
    for search_dir in vendor_search_dirs():
        if str(search_dir) not in sys.path:
            sys.path.insert(0, str(search_dir))

    # #region debug-point A:ensure-pypdf-entry
    import json, urllib.request, os; _p='.dbg/startup-missing-dep.env'; _u,_s='http://127.0.0.1:7777/event','startup-missing-dep'; exec("try:\n with open(_p, encoding='utf-8') as f: c=f.read(); _u=next((l.split('=',1)[1] for l in c.split('\\n') if l.startswith('DEBUG_SERVER_URL=')),_u); _s=next((l.split('=',1)[1] for l in c.split('\\n') if l.startswith('DEBUG_SESSION_ID=')),_s)\n urllib.request.urlopen(urllib.request.Request(_u, data=json.dumps({\"sessionId\":_s,\"runId\":\"pre-fix\",\"hypothesisId\":\"A\",\"location\":\"pdf_merge_tool.pyw:71\",\"msg\":\"[DEBUG] entering ensure_pypdf\",\"data\":{\"vendor_dir\":str(local_vendor),\"vendor_exists\":os.path.isdir(local_vendor),\"sys_path_has_vendor\":str(local_vendor) in sys.path}}, ensure_ascii=False).encode(), headers={\"Content-Type\":\"application/json\"}), timeout=0.2).read()\nexcept: pass")
    # #endregion

    try:
        from pypdf import PdfReader, PdfWriter

        # #region debug-point B:pypdf-import-success
        import json, urllib.request; _p='.dbg/startup-missing-dep.env'; _u,_s='http://127.0.0.1:7777/event','startup-missing-dep'; exec("try:\n with open(_p, encoding='utf-8') as f: c=f.read(); _u=next((l.split('=',1)[1] for l in c.split('\\n') if l.startswith('DEBUG_SERVER_URL=')),_u); _s=next((l.split('=',1)[1] for l in c.split('\\n') if l.startswith('DEBUG_SESSION_ID=')),_s)\n urllib.request.urlopen(urllib.request.Request(_u, data=json.dumps({\"sessionId\":_s,\"runId\":\"pre-fix\",\"hypothesisId\":\"B\",\"location\":\"pdf_merge_tool.pyw:77\",\"msg\":\"[DEBUG] pypdf import succeeded\",\"data\":{}}, ensure_ascii=False).encode(), headers={\"Content-Type\":\"application/json\"}), timeout=0.2).read()\nexcept: pass")
        # #endregion

        return PdfReader, PdfWriter
    except ImportError:
        # #region debug-point C:pypdf-import-failed
        import json, urllib.request; _p='.dbg/startup-missing-dep.env'; _u,_s='http://127.0.0.1:7777/event','startup-missing-dep'; exec("try:\n with open(_p, encoding='utf-8') as f: c=f.read(); _u=next((l.split('=',1)[1] for l in c.split('\\n') if l.startswith('DEBUG_SERVER_URL=')),_u); _s=next((l.split('=',1)[1] for l in c.split('\\n') if l.startswith('DEBUG_SESSION_ID=')),_s)\n urllib.request.urlopen(urllib.request.Request(_u, data=json.dumps({\"sessionId\":_s,\"runId\":\"pre-fix\",\"hypothesisId\":\"C\",\"location\":\"pdf_merge_tool.pyw:80\",\"msg\":\"[DEBUG] pypdf import failed before UI ready\",\"data\":{\"cwd\":os.getcwd(),\"argv\":sys.argv}}, ensure_ascii=False).encode(), headers={\"Content-Type\":\"application/json\"}), timeout=0.2).read()\nexcept: pass")
        # #endregion
        install_now = messagebox.askyesno(
            "Missing dependency",
            "The tool needs the 'pypdf' package to merge files.\n\n"
            "Install it automatically now?",
        )
        if not install_now:
            if getattr(sys, "frozen", False):
                show_missing_backend_message()
            raise MissingBackendError("pypdf installation was cancelled")
        if not install_pypdf():
            if getattr(sys, "frozen", False):
                show_missing_backend_message()
            raise MissingBackendError("pypdf installation failed")
        from pypdf import PdfReader, PdfWriter

        return PdfReader, PdfWriter


def send_payload_to_running_instance(files: list[str]) -> bool:
    payload = json.dumps({"files": files}).encode("utf-8")
    try:
        with socket.create_connection((SERVER_HOST, SERVER_PORT), timeout=0.4) as client:
            client.sendall(payload)
            return True
    except OSError:
        return False


class ExternalFileServer(threading.Thread):
    def __init__(self, queue: Queue):
        super().__init__(daemon=True)
        self.queue = queue
        self._stop_event = threading.Event()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, SERVER_PORT))
        self.server.listen()
        self.server.settimeout(0.5)

    def run(self) -> None:
        while not self._stop_event.is_set():
            try:
                connection, _ = self.server.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            with connection:
                chunks: list[bytes] = []
                while True:
                    data = connection.recv(BUFFER_SIZE)
                    if not data:
                        break
                    chunks.append(data)
                if not chunks:
                    self.queue.put([])
                    continue
                try:
                    payload = json.loads(b"".join(chunks).decode("utf-8"))
                    files = normalize_files(payload.get("files", []))
                    self.queue.put(files)
                except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
                    continue

    def stop(self) -> None:
        self._stop_event.set()
        try:
            self.server.close()
        except OSError:
            pass


class PdfMergeApp:
    def __init__(self, initial_files: list[str], queue: Queue, server: ExternalFileServer):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title(APP_TITLE)
        self.root.geometry("760x500")
        self.root.minsize(700, 450)

        # #region debug-point D:app-init-before-dependency
        import json, urllib.request; _p='.dbg/startup-missing-dep.env'; _u,_s='http://127.0.0.1:7777/event','startup-missing-dep'; exec("try:\n with open(_p, encoding='utf-8') as f: c=f.read(); _u=next((l.split('=',1)[1] for l in c.split('\\n') if l.startswith('DEBUG_SERVER_URL=')),_u); _s=next((l.split('=',1)[1] for l in c.split('\\n') if l.startswith('DEBUG_SESSION_ID=')),_s)\n urllib.request.urlopen(urllib.request.Request(_u, data=json.dumps({\"sessionId\":_s,\"runId\":\"pre-fix\",\"hypothesisId\":\"D\",\"location\":\"pdf_merge_tool.pyw:157\",\"msg\":\"[DEBUG] app init reached before ensure_pypdf\",\"data\":{\"initial_file_count\":len(initial_files)}}, ensure_ascii=False).encode(), headers={\"Content-Type\":\"application/json\"}), timeout=0.2).read()\nexcept: pass")
        # #endregion

        self.PdfReader = None
        self.PdfWriter = None

        self.paths: list[str] = []
        self.queue = queue
        self.server = server

        self.output_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")

        self._build_ui()
        self._add_files(initial_files)
        self._suggest_output_path()
        self.root.after(200, self._drain_external_queue)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.deiconify()

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=BOTH, expand=True)

        toolbar = ttk.Frame(main)
        toolbar.pack(fill=X)

        ttk.Button(toolbar, text="Add PDFs", command=self._choose_files).pack(side=LEFT, padx=(0, 8))
        ttk.Button(toolbar, text="Remove Selected", command=self._remove_selected).pack(side=LEFT, padx=(0, 8))
        ttk.Button(toolbar, text="Move Up", command=lambda: self._move_selected(-1)).pack(side=LEFT, padx=(0, 8))
        ttk.Button(toolbar, text="Move Down", command=lambda: self._move_selected(1)).pack(side=LEFT, padx=(0, 8))
        ttk.Button(toolbar, text="Clear", command=self._clear_all).pack(side=LEFT)

        list_frame = ttk.Frame(main)
        list_frame.pack(fill=BOTH, expand=True, pady=12)

        self.listbox = tk.Listbox(list_frame, selectmode=SINGLE, activestyle="dotbox")
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.configure(yscrollcommand=scrollbar.set)

        output_frame = ttk.LabelFrame(main, text="Output")
        output_frame.pack(fill=X)

        ttk.Entry(output_frame, textvariable=self.output_var).pack(side=LEFT, fill=X, expand=True, padx=(10, 8), pady=10)
        ttk.Button(output_frame, text="Browse", command=self._choose_output).pack(side=RIGHT, padx=(0, 10), pady=10)

        action_frame = ttk.Frame(main)
        action_frame.pack(fill=X, pady=(12, 0))

        ttk.Button(action_frame, text="Merge PDFs", command=self._merge_files).pack(side=LEFT)
        ttk.Label(action_frame, textvariable=self.status_var).pack(side=RIGHT)

    def _choose_files(self) -> None:
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")],
        )
        self._add_files(list(files))
        self._suggest_output_path()

    def _choose_output(self) -> None:
        initial_file = self.output_var.get().strip() or "merged.pdf"
        path = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            initialfile=Path(initial_file).name,
            initialdir=str(Path(initial_file).parent) if os.path.isabs(initial_file) else None,
            filetypes=[("PDF files", "*.pdf")],
        )
        if path:
            self.output_var.set(path)

    def _add_files(self, files: list[str]) -> None:
        added_count = 0
        existing = {path.lower() for path in self.paths}
        for path in normalize_files(files):
            key = path.lower()
            if key in existing:
                continue
            existing.add(key)
            self.paths.append(path)
            self.listbox.insert(END, path)
            added_count += 1
        if added_count:
            self.status_var.set(f"Added {added_count} file(s)")

    def _remove_selected(self) -> None:
        selection = self.listbox.curselection()
        if not selection:
            return
        index = selection[0]
        self.listbox.delete(index)
        del self.paths[index]
        self._suggest_output_path()
        self.status_var.set("Removed selected file")

    def _move_selected(self, direction: int) -> None:
        selection = self.listbox.curselection()
        if not selection:
            return
        old_index = selection[0]
        new_index = old_index + direction
        if new_index < 0 or new_index >= len(self.paths):
            return
        self.paths[old_index], self.paths[new_index] = self.paths[new_index], self.paths[old_index]
        self._refresh_listbox()
        self.listbox.selection_set(new_index)
        self.listbox.activate(new_index)
        self.status_var.set("Updated file order")

    def _clear_all(self) -> None:
        self.paths.clear()
        self.listbox.delete(0, END)
        self.output_var.set("")
        self.status_var.set("Cleared all files")

    def _refresh_listbox(self) -> None:
        self.listbox.delete(0, END)
        for path in self.paths:
            self.listbox.insert(END, path)

    def _suggest_output_path(self) -> None:
        if self.output_var.get().strip() or not self.paths:
            return
        first = Path(self.paths[0])
        suggested = first.with_name(f"{first.stem}_merged.pdf")
        self.output_var.set(str(suggested))

    def _focus_window(self) -> None:
        self.root.deiconify()
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after(300, lambda: self.root.attributes("-topmost", False))
        self.root.focus_force()

    def _drain_external_queue(self) -> None:
        received = False
        try:
            while True:
                files = self.queue.get_nowait()
                if files:
                    self._add_files(files)
                    self._suggest_output_path()
                received = True
        except Empty:
            pass

        if received:
            self._focus_window()

        self.root.after(200, self._drain_external_queue)

    def _merge_files(self) -> None:
        if len(self.paths) < 2:
            messagebox.showwarning("Not enough files", "Please add at least two PDF files.")
            return

        if self.PdfReader is None or self.PdfWriter is None:
            try:
                self.PdfReader, self.PdfWriter = ensure_pypdf()
            except MissingBackendError:
                self.status_var.set("Backend unavailable")
                return

        output_path = self.output_var.get().strip()
        if not output_path:
            self._choose_output()
            output_path = self.output_var.get().strip()
            if not output_path:
                return

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        self.status_var.set("Merging...")
        self.root.update_idletasks()

        writer = self.PdfWriter()
        try:
            for path in self.paths:
                reader = self.PdfReader(path)
                for page in reader.pages:
                    writer.add_page(page)

            with output.open("wb") as handle:
                writer.write(handle)
        except Exception as exc:  # noqa: BLE001
            self.status_var.set("Merge failed")
            messagebox.showerror("Merge failed", f"Could not merge PDFs.\n\n{exc}")
            return

        self.status_var.set(f"Saved: {output}")
        open_file = messagebox.askyesno(
            "Merge complete",
            f"Merged PDF saved to:\n{output}\n\nOpen the file now?",
        )
        if open_file:
            os.startfile(str(output))

    def _on_close(self) -> None:
        self.server.stop()
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    cli_files = normalize_files(sys.argv[1:])
    if send_payload_to_running_instance(cli_files):
        return
    queue: Queue = Queue()
    try:
        server = ExternalFileServer(queue)
    except OSError:
        for _ in range(10):
            if send_payload_to_running_instance(cli_files):
                return
            threading.Event().wait(0.15)
        raise

    server.start()
    try:
        app = PdfMergeApp(cli_files, queue, server)
    except Exception:
        server.stop()
        raise
    app.run()


if __name__ == "__main__":
    main()
