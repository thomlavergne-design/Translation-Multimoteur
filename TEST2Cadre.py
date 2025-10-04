
import tkinter as tk

class DualFrameGridExample:
    def __init__(self, root):
        self.root = root
        self.root.title("Dual Frame with Entries and Buttons using Grid")

        # Configure the grid layout for the root window
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Create the first frame
        self.frame1 = tk.LabelFrame(root, text="Frame 1", padx=10, pady=10)
        self.frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.entry1 = tk.Entry(self.frame1, width=30)
        self.entry1.grid(row=0, column=0, pady=5)

        self.button1 = tk.Button(self.frame1, text="Submit Frame 1", command=lambda: self.on_submit(self.entry1))
        self.button1.grid(row=1, column=0, pady=5)

        # Create the second frame
        self.frame2 = tk.LabelFrame(root, text="Frame 2", padx=10, pady=10)
        self.frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.entry2 = tk.Entry(self.frame2, width=30)
        self.entry2.grid(row=0, column=0, pady=5)

        self.button2 = tk.Button(self.frame2, text="Submit Frame 2", command=lambda: self.on_submit(self.entry2))
        self.button2.grid(row=1, column=0, pady=5)

        # Configure grid layout for frames
        self.frame1.columnconfigure(0, weight=1)
        self.frame2.columnconfigure(0, weight=1)

    def on_submit(self, entry):
        # Retrieve and print the text from the entry widget
        entered_text = entry.get()
        print(f"Submitted text: {entered_text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DualFrameGridExample(root)
    root.mainloop()
