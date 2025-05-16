import tkinter as tk
from tkinter import ttk, messagebox
import sys
import requests
import tempfile
import os

def download_icon_tempfile(url):
    response = requests.get(url)
    if response.status_code == 200:
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ico")
        tmp_file.write(response.content)
        tmp_file.close()
        return tmp_file.name
    else:
        return None
icon_url = "https://raw.githubusercontent.com/fuadismayil585/valyuta-cevirici/main/icon.ico"
icon_path = download_icon_tempfile(icon_url)
API_KEY = "67051e043e0baa9483903bd1"
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"
def get_exchange_rates(base_currency):
    try:
        response = requests.get(API_URL + base_currency)
        if response.status_code == 200:
            return response.json().get("conversion_rates", {})
        else:
            messagebox.showerror("Server Xətası", "Məlumat alına bilmədi.")
            return {}
    except Exception as e:
        messagebox.showerror("Xəta", f"Bağlantı xətası: {e}")
        return {}
def convert_currency():
    try:
        amount = float(entry_amount.get())
        from_currency = combo_from.get()
        to_currency = combo_to.get()
        rates = get_exchange_rates(from_currency)
        if to_currency in rates:
            result = amount * rates[to_currency]
            label_result.config(text=f"Nəticə: {result:.2f} {to_currency}")
        else:
            label_result.config(text="Valyuta tapılmadı!")
    except ValueError:
        messagebox.showwarning("Xəta", "Zəhmət olmasa düzgün rəqəm daxil edin.")
    except Exception as e:
        messagebox.showerror("Xəta", f"Xəta baş verdi: {e}")
def main():
    global entry_amount, combo_from, combo_to, label_result
    root = tk.Tk()
    if icon_path and os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    else:
        print("İkon yüklənmədi!")
    root.title("Valyuta Çevirici")
    root.geometry("500x300")
    root.resizable(False, False)
    tk.Label(root, text="Məbləği daxil edin:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_amount = tk.Entry(root, font=("Arial", 12))
    entry_amount.grid(row=0, column=1, padx=10, pady=10)
    tk.Label(root, text="Dəyişdirilən valyuta:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    combo_from = ttk.Combobox(root, values=currency_list(), font=("Arial", 12), state="readonly")
    combo_from.grid(row=1, column=1, padx=10, pady=10)
    combo_from.set("AZN")
    tk.Label(root, text="Alınan valyuta:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
    combo_to = ttk.Combobox(root, values=currency_list(), font=("Arial", 12), state="readonly")
    combo_to.grid(row=2, column=1, padx=10, pady=10)
    combo_to.set("USD")
    btn_convert = tk.Button(root, text="Çevir", command=convert_currency, font=("Arial", 12), bg="#4CAF50", fg="white")
    btn_convert.grid(row=3, column=0, columnspan=2, pady=20)
    label_result = tk.Label(root, text="Nəticə: ", font=("Arial", 14))
    label_result.grid(row=4, column=0, columnspan=2)
    label_credit = tk.Label(root, text="by Fuad İsmayıl", font=("Arial", 8), fg="gray")
    label_credit.grid(row=5, column=1, sticky="e", padx=10, pady=(0,10))
    root.mainloop()
def currency_list():
    return ["USD", "EUR", "GBP", "AZN", "RUB", "TRY", "CNY", "JPY"]
if __name__ == "__main__":
    main()
if icon_path and os.path.exists(icon_path):
    os.remove(icon_path)
