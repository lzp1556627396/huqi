from __future__ import annotations

from .gui import AttendanceApp


def main() -> None:
    app = AttendanceApp()
    app.mainloop()


if __name__ == "__main__":
    main()

