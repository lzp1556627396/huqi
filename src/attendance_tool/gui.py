from __future__ import annotations

import threading
import traceback
from pathlib import Path

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .excel_processor import process_workbook


class AttendanceApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("考勤自动分析工具")
        self.geometry("760x420")
        self.resizable(True, True)

        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.sheet_var = tk.StringVar(value="概况统计与打卡明细")

        self._build_widgets()

    def _build_widgets(self) -> None:
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="输入 Excel：").grid(row=0, column=0, sticky=tk.W, pady=6)
        input_entry = ttk.Entry(frame, textvariable=self.input_var)
        input_entry.grid(row=0, column=1, sticky=tk.EW, padx=8)
        ttk.Button(frame, text="选择", command=self._choose_input).grid(row=0, column=2, sticky=tk.W)

        ttk.Label(frame, text="输出文件：").grid(row=1, column=0, sticky=tk.W, pady=6)
        output_entry = ttk.Entry(frame, textvariable=self.output_var)
        output_entry.grid(row=1, column=1, sticky=tk.EW, padx=8)
        ttk.Button(frame, text="选择", command=self._choose_output).grid(row=1, column=2, sticky=tk.W)

        ttk.Label(frame, text="工作表名：").grid(row=2, column=0, sticky=tk.W, pady=6)
        sheet_entry = ttk.Entry(frame, textvariable=self.sheet_var)
        sheet_entry.grid(row=2, column=1, sticky=tk.EW, padx=8)

        self.process_button = ttk.Button(frame, text="开始处理", command=self._start_processing)
        self.process_button.grid(row=3, column=0, columnspan=3, sticky=tk.EW, pady=12)

        ttk.Label(frame, text="处理日志：").grid(row=4, column=0, sticky=tk.W)
        self.log_text = tk.Text(frame, height=12, wrap=tk.WORD)
        self.log_text.grid(row=5, column=0, columnspan=3, sticky=tk.NSEW, pady=(6, 0))

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=5, column=3, sticky=tk.NS, pady=(6, 0))
        self.log_text.configure(yscrollcommand=scrollbar.set)

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(5, weight=1)

    def _choose_input(self) -> None:
        path = filedialog.askopenfilename(
            title="选择考勤 Excel",
            filetypes=[("Excel 文件", "*.xlsx *.xlsm *.xltx *.xltm"), ("全部文件", "*.*")],
        )
        if not path:
            return
        self.input_var.set(path)

        input_path = Path(path)
        default_output = input_path.with_name(f"{input_path.stem}_处理结果{input_path.suffix}")
        self.output_var.set(str(default_output))
        self._log(f"已选择输入文件：{input_path}")

    def _choose_output(self) -> None:
        path = filedialog.asksaveasfilename(
            title="选择输出文件",
            defaultextension=".xlsx",
            filetypes=[("Excel 文件", "*.xlsx")],
        )
        if not path:
            return
        self.output_var.set(path)
        self._log(f"已设置输出文件：{path}")

    def _start_processing(self) -> None:
        input_path = self.input_var.get().strip()
        output_path = self.output_var.get().strip()
        sheet_name = self.sheet_var.get().strip() or "概况统计与打卡明细"

        if not input_path:
            messagebox.showwarning("提示", "请先选择输入 Excel 文件。")
            return

        self._set_busy(True)
        self._log("开始处理，请稍候...")

        worker = threading.Thread(
            target=self._process_in_background,
            args=(input_path, output_path, sheet_name),
            daemon=True,
        )
        worker.start()

    def _process_in_background(self, input_path: str, output_path: str, sheet_name: str) -> None:
        try:
            output = process_workbook(
                input_file=input_path,
                output_file=output_path or None,
                sheet_name=sheet_name,
            )
        except Exception as exc:
            error_text = f"{exc}\n{traceback.format_exc()}"
            self.after(0, self._on_failure, error_text)
            return

        self.after(0, self._on_success, str(output))

    def _on_success(self, output_path: str) -> None:
        self._set_busy(False)
        self._log(f"处理完成，输出文件：{output_path}")
        messagebox.showinfo("完成", f"处理完成！\n输出文件：\n{output_path}")

    def _on_failure(self, error_text: str) -> None:
        self._set_busy(False)
        self._log("处理失败：")
        self._log(error_text)
        messagebox.showerror("错误", "处理失败，请查看日志。")

    def _set_busy(self, busy: bool) -> None:
        state = tk.DISABLED if busy else tk.NORMAL
        self.process_button.configure(state=state)

    def _log(self, message: str) -> None:
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

