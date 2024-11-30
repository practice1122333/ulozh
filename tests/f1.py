import tkinter as tk

def send_command(command):
    console_output.insert(tk.END, f"Відправлено: {command}\n")
    console_output.insert(tk.END, f"Команда '{command}' виконано успішно\n")
    console_output.see(tk.END)

# Створення головного вікна
root = tk.Tk()
root.title("Управління кіберінцидентами")

# Створення кнопок команд
button1 = tk.Button(root, text="Відновлення системи", command=lambda: send_command("Відновлення системи"))
button1.pack(pady=5)

button2 = tk.Button(root, text="Перевірка безпеки", command=lambda: send_command("Перевірка безпеки"))
button2.pack(pady=5)

button3 = tk.Button(root, text="Інше завдання", command=lambda: send_command("Інше завдання"))
button3.pack(pady=5)

# Поле для виводу результатів
console_output = tk.Text(root, height=10, width=50, state='normal')
console_output.pack(pady=10)

# Запуск основного циклу
root.mainloop()