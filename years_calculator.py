"""Years Calculator: how many years (and months, days) since a date.
Use it as an age calculator, or to compare any two dates.
Only needs Python (tkinter is built in).   Run:  python years_calculator.py
"""
import calendar
import tkinter as tk
from datetime import date, datetime

# ---------- Black & Pink Theme ----------
BG = "#121212"
CARD = "#1C1C1C"
TEXT = "#FFFFFF"
SUBTEXT = "#A6A6A6"
FIELD = "#292929"
SPECIAL = "#383838"
SPECIAL_HOVER = "#505050"
ACCENT = "#FF4F9A"
ACCENT_HOVER = "#FF79B2"
DARK_TEXT = "#121212"
ERROR = "#FF5252"
FONT = "Segoe UI"

DATE_FORMATS = ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%Y")   # day first, like 15/03/2000


# ---------------------------- the maths (no GUI) ----------------------------
def parse_date(text: str) -> date:
    text = text.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    raise ValueError("Could not read that date. Use DD/MM/YYYY, for example 15/03/2000.")


def add_months(d: date, n: int) -> date:
    year, month0 = divmod(d.month - 1 + n, 12)
    year += d.year
    month = month0 + 1
    return date(year, month, min(d.day, calendar.monthrange(year, month)[1]))


def date_diff(start: date, end: date):
    """Return (years, months, days, total_months) between two dates, start <= end."""
    total_months = (end.year - start.year) * 12 + end.month - start.month
    if end.day < start.day:
        total_months -= 1
    anchor = add_months(start, total_months)
    days = (end - anchor).days
    years, months = divmod(total_months, 12)
    return years, months, days, total_months


def plural(n: int, word: str) -> str:
    return f"{n} {word}" + ("" if n == 1 else "s")


def next_anniversary(start: date, after: date) -> date:
    for year in (after.year, after.year + 1):
        day = min(start.day, calendar.monthrange(year, start.month)[1])   # Feb 29 -> Feb 28
        candidate = date(year, start.month, day)
        if candidate >= after:
            return candidate


def build_report(from_text: str, to_text: str) -> dict:
    """Turn the two typed dates into the text shown on screen. Raises ValueError with a friendly message."""
    if not from_text.strip():
        raise ValueError("Enter the From date.")
    start = parse_date(from_text)
    end = parse_date(to_text) if to_text.strip() else date.today()
    if start > end:
        raise ValueError("The From date must be earlier than the To date.")
    years, months, days, total_months = date_diff(start, end)
    total_days = (end - start).days
    anniversary = next_anniversary(start, end)
    if anniversary == end:
        anniv_text = "Today is the anniversary!"
    else:
        anniv_text = f"Next anniversary: {anniversary:%A, %d %B %Y} (in {plural((anniversary - end).days, 'day')})"
    return {
        "headline": plural(years, "year"),
        "detail": f"{plural(months, 'month')} and {plural(days, 'day')}",
        "stats": "\n".join([
            f"Total months: {total_months:,}",
            f"Total weeks: {total_days // 7:,}",
            f"Total days: {total_days:,}",
            f"The From date was a {start:%A}",
            anniv_text,
        ]),
    }


# ---------------------------------- the window ----------------------------------
class YearsApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Years Calculator")
        root.geometry("420x640")
        root.minsize(380, 600)
        root.configure(bg=BG)
        self.set_icon()
        self.from_var = tk.StringVar()
        self.to_var = tk.StringVar(value=date.today().strftime("%d/%m/%Y"))

        tk.Label(root, text="Years Calculator", bg=BG, fg=TEXT,
                 font=(FONT, 22, "bold")).pack(pady=(18, 2))
        tk.Label(root, text="How long since a date? Dates are DD/MM/YYYY.", bg=BG,
                 fg=SUBTEXT, font=(FONT, 10)).pack(pady=(0, 14))

        form = tk.Frame(root, bg=BG)
        form.pack(fill="x", padx=24)
        self.from_entry = self.add_field(form, "From date  (e.g. 15/03/2000)", self.from_var)
        row = tk.Frame(form, bg=BG)
        tk.Label(form, text="To date  (today by default)", bg=BG, fg=SUBTEXT,
                 font=(FONT, 11), anchor="w").pack(fill="x", pady=(12, 4))
        row.pack(fill="x")
        entry = self.make_entry(row, self.to_var)
        entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.make_button(row, "Today", "special", self.set_today, 12).pack(side="left", padx=(8, 0), ipady=6, ipadx=6)

        buttons = tk.Frame(root, bg=BG)
        buttons.pack(fill="x", padx=24, pady=16)
        self.make_button(buttons, "Calculate", "accent", self.calculate, 16).pack(
            side="left", fill="x", expand=True, ipady=8)
        self.make_button(buttons, "Clear", "special", self.clear, 16).pack(
            side="left", padx=(8, 0), ipady=8, ipadx=14)

        self.error = tk.Label(root, text="", bg=BG, fg=ERROR, font=(FONT, 11), wraplength=360)
        self.error.pack()

        card = tk.Frame(root, bg=CARD)
        card.pack(fill="both", expand=True, padx=24, pady=(6, 24))
        self.headline = tk.Label(card, text="", bg=CARD, fg=ACCENT, font=(FONT, 44, "bold"))
        self.headline.pack(pady=(18, 0))
        self.detail = tk.Label(card, text="Your result appears here", bg=CARD, fg=TEXT, font=(FONT, 15))
        self.detail.pack(pady=(0, 14))
        self.stats = tk.Label(card, text="", bg=CARD, fg=SUBTEXT, font=(FONT, 11),
                              justify="left", anchor="w", wraplength=340)
        self.stats.pack(fill="x", padx=20)

        root.bind("<Return>", lambda e: self.calculate())
        root.bind("<Escape>", lambda e: self.clear())
        self.from_entry.focus_set()

    # ----- small helpers -----
    def set_icon(self):
        icon = tk.PhotoImage(width=32, height=32)
        icon.put(ACCENT, to=(0, 0, 32, 32))
        icon.put(DARK_TEXT, to=(6, 6, 26, 10))      # top bar
        icon.put(DARK_TEXT, to=(6, 14, 26, 26))     # calendar body
        self.root.iconphoto(True, icon)
        self._icon = icon

    def make_entry(self, parent, var):
        return tk.Entry(parent, textvariable=var, font=(FONT, 18), bg=FIELD, fg=TEXT,
                        insertbackground=TEXT, relief="flat", justify="center",
                        highlightthickness=2, highlightbackground=FIELD, highlightcolor=ACCENT)

    def add_field(self, parent, label, var):
        tk.Label(parent, text=label, bg=BG, fg=SUBTEXT, font=(FONT, 11), anchor="w").pack(fill="x", pady=(0, 4))
        entry = self.make_entry(parent, var)
        entry.pack(fill="x", ipady=8)
        return entry

    def make_button(self, parent, text, kind, command, size):
        bg, hover, fg = (ACCENT, ACCENT_HOVER, DARK_TEXT) if kind == "accent" else (SPECIAL, SPECIAL_HOVER, TEXT)
        b = tk.Button(parent, text=text, command=command, font=(FONT, size, "bold"), bg=bg, fg=fg,
                      activebackground=hover, activeforeground=fg, relief="flat", bd=0, cursor="hand2")
        b.bind("<Enter>", lambda e: b.config(bg=hover))
        b.bind("<Leave>", lambda e: b.config(bg=bg))
        return b

    # ----- actions -----
    def show(self, headline="", detail="", stats="", error=""):
        self.error.config(text=error)
        self.headline.config(text=headline)
        self.detail.config(text=detail or ("" if error else "Your result appears here"))
        self.stats.config(text=stats)

    def calculate(self):
        try:
            r = build_report(self.from_var.get(), self.to_var.get())
        except ValueError as e:
            self.show(error=str(e))
            return
        self.show(r["headline"], r["detail"], r["stats"])

    def set_today(self):
        self.to_var.set(date.today().strftime("%d/%m/%Y"))

    def clear(self):
        self.from_var.set("")
        self.set_today()
        self.show()
        self.from_entry.focus_set()


def main():
    root = tk.Tk()
    YearsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()