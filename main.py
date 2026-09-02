import customtkinter as ctk
import time

class Popup(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        WIDTH = 400
        HEIGHT = 150
        self.update()
        windowWidth = 2496
        windowHeight = 1664
        winX = windowWidth - 2*WIDTH + 25
        winY = windowHeight - 2*HEIGHT - 100
        self.geometry(f"{WIDTH}x{HEIGHT}+{winX}+{winY}")

        self.grid_columnconfigure(0, weight=1)

        self.createWidgets()

    def createWidgets(self):
        self.settingFrame()
        self.contentFrame()

    def settingFrame(self):
        frame = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            frame, 
            text="Settings", 
            command=None).grid(row=0, column=0, sticky="nse", padx=(10, 10), pady=(10, 10))

        frame.grid(row=0, column=0, sticky="nsew")

    def contentFrame(self):
        self.contentFrame = ctk.CTkFrame(self)
        self.contentFrame.grid_columnconfigure(0, weight=1)
        self.contentFrame.grid_rowconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            self.contentFrame, 
            text="Drink water Meercat").grid(row=0, column=0, sticky="nsew", padx=(5, 5), pady=(20, 5))

        buttonFrame = ctk.CTkFrame(self.contentFrame)
        buttonFrame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            buttonFrame,
            text="I Drank Already",
            fg_color="green",
            command=None
        ).grid(row=0, column=0, sticky="nsew")
        ctk.CTkButton(
            buttonFrame,
            text=f"Snooze ({self.getSnoozeTime()})",
            fg_color="red"
        ).grid(row=0, column=1, sticky="nsew")

        buttonFrame.grid(row=1, column=0, sticky="nsew", padx=(5, 5), pady=(5, 5))

        self.contentFrame.grid(row=1, column=0, sticky="nsew")

    def getSnoozeTime(self):
        pass

    def snooze(self):
        pass

    def drankWater(self):
        pass

if __name__ == "__main__":
    while True:
        window = Popup("black")
        window.mainloop()

        time.sleep