import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import QuantBotApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantBotApp(root)
    root.mainloop()

