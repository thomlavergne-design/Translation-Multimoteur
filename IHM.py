import tkinter as tk
from tkinter import ttk

class SerialPortSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Port Configuration")

        # Port COM
        self.com_port_label = ttk.Label(root, text="Port COM:")
        self.com_port_label.grid(column=0, row=0, padx=10, pady=10)

        self.com_port_var = tk.StringVar()
        self.com_port_dropdown = ttk.Combobox(root, textvariable=self.com_port_var)
        self.com_port_dropdown['values'] = ['COM1', 'COM2', 'COM3', 'COM4']
        self.com_port_dropdown.grid(column=1, row=0, padx=10, pady=10)
        self.com_port_dropdown.current(0)

        # Baudrate
        self.baudrate_label = ttk.Label(root, text="Baudrate:")
        self.baudrate_label.grid(column=0, row=1, padx=10, pady=10)

        self.baudrate_var = tk.StringVar()
        self.baudrate_dropdown = ttk.Combobox(root, textvariable=self.baudrate_var)
        self.baudrate_dropdown['values'] = ['9600', '19200', '38400', '57600', '115200']
        self.baudrate_dropdown.grid(column=1, row=1, padx=10, pady=10)
        self.baudrate_dropdown.current(0)

        # Vitesse
        self.speed_label = ttk.Label(root, text="Vitesse:")
        self.speed_label.grid(column=0, row=2, padx=10, pady=10)

        self.speed_scale = ttk.Scale(root, from_=0, to=100, orient='horizontal')
        self.speed_scale.grid(column=1, row=2, padx=10, pady=10)

        # Bouton de soumission
        self.submit_button = ttk.Button(root, text="Appliquer", command=self.submit)
        self.submit_button.grid(column=0, row=3, columnspan=2, pady=10)

    def submit(self):
        com_port = self.com_port_var.get()
        baudrate = self.baudrate_var.get()
        speed = self.speed_scale.get()
        print(f"Port COM: {com_port}, Baudrate: {baudrate}, Vitesse: {speed}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialPortSelector(root)
    root.mainloop()