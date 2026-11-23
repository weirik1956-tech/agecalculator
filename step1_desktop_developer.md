### years_calculator.py
```python
import tkinter as tk
from tkinter import messagebox

class YearsCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Years Calculator")
        self.window.geometry("300x200")

        # Create input fields
        self.year_label = tk.Label(self.window, text="Enter year:")
        self.year_label.pack()
        self.year_entry = tk.Entry(self.window)
        self.year_entry.pack()

        # Create buttons
        self.calculate_button = tk.Button(self.window, text="Calculate", command=self.calculate_years)
        self.calculate_button.pack()
        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset_years)
        self.reset_button.pack()

    def calculate_years(self):
        try:
            year = int(self.year_entry.get())
            if year <= 0:
                messagebox.showerror("Error", "Year must be a positive integer")
                return
            result = self.calculate_year(year)
            messagebox.showinfo("Result", f"{year} years is equal to {result} months")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a positive integer")

    def calculate_year(self, year):
        # Simple formula: 12 months in a year / 12 months in a year
        return (12 * year) / 12

    def reset_years(self):
        self.year_entry.delete(0, tk.END)
        messagebox.showinfo("Reset", "Years calculator reset")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = YearsCalculator()
    calculator.run()
```
### FILE: years_calculator.py
```
### FILE: years_calculator.py
```
### FILE: output.txt
```
### FILE: years_calculator.py
```