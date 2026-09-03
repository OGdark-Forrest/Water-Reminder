import customtkinter as ctk
import time

class Label(ctk.CTkLabel):
    def __init__(self, master, text, font=None):
        super().__init__(master, text=text, font=font)

    def gridWidget(self, row, column):
        self.grid(row=row, column=column, sticky="nsew", padx=(5, 5), pady=(5, 5))

class SliderFrame(ctk.CTkFrame):
    def __init__(self, master, labelText, labelTuple: tuple, sliderInfo: tuple[int, int, int], updateCommand, setCommand):
        super().__init__(master)
        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        Label(self, text=labelText).gridWidget(0, 0)

        labelContainer = ctk.CTkFrame(self)
        labelContainer.grid_columnconfigure(tuple(range(len(labelTuple))), weight=1)

        for i in range(len(labelTuple)):
            Label(labelContainer, text=labelTuple[i]).gridWidget(0, i)

        labelContainer.grid(row=1, column=0, sticky="nsew", padx=(5, 5), pady=(5, 5))

        slider = ctk.CTkSlider(self, number_of_steps=sliderInfo[0], from_=sliderInfo[1], to=sliderInfo[2], command=updateCommand)
        slider.set(setCommand())
        slider.grid(row=2, column=0, sticky="nsew", padx=(5,5), pady=(5,5))

    def gridWidget(self, row, column):
        self.grid(row=row, column=column, sticky="nsew", padx=(10, 10), pady=(10, 10))

class Popup(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.WIDTH = 400
        self.HEIGHT = 150
        self.update()
        windowWidth = 2496
        windowHeight = 1664
        winX = windowWidth - 2*self.WIDTH + 35
        winY = windowHeight - 2*self.HEIGHT - 175
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{winX}+{winY}")

        self.grid_columnconfigure(0, weight=1)

        self.snoozeTime = 5
        self.isSetting = False

        self.createWidgets()

    def createWidgets(self):
        self.createSettingButtonFrame()
        self.createContentFrame()

    def createSettingButtonFrame(self):
        frame = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            frame, 
            text="Settings", 
            command=self.displaySettings).grid(row=0, column=0, sticky="nse", padx=(10, 10), pady=(10, 10))

        frame.grid(row=0, column=0, sticky="nsew")

    def createContentFrame(self):
        self.contentFrame = ctk.CTkFrame(self)
        self.contentFrame.grid_columnconfigure(0, weight=1)
        self.contentFrame.grid_rowconfigure((0, 1), weight=1)

        Label(
            self.contentFrame, 
            text="Drink water Meercat").gridWidget(row=0, column=0)

        buttonFrame = ctk.CTkFrame(self.contentFrame)
        buttonFrame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            buttonFrame,
            text="I Drank Already",
            fg_color="green",
            command=self.drankWater
        ).grid(row=0, column=0, sticky="nsew")
        ctk.CTkButton(
            buttonFrame,
            text=f"Snooze ({self.getSnoozeTime()} mins)",
            fg_color="red",
            command=self.snooze
        ).grid(row=0, column=1)

        buttonFrame.grid(row=1, column=0, sticky="nsew", padx=(5, 5), pady=(5, 5))

        self.contentFrame.grid(row=1, column=0, sticky="nsew")

    def displaySettings(self):
        if self.isSetting:
            self.geometry(f"{self.WIDTH}x150")
            self.settingFrame.destroy()
            self.createContentFrame()
            self.isSetting = False
        else:
            self.geometry(f"{self.WIDTH}x200")
            self.contentFrame.destroy()
            self.createSettingFrame()
            self.isSetting = True

    def getSnoozeTime(self):
        return self.snoozeTime

    def snooze(self):
        self.destroy()
        time.sleep(self.getSnoozeTime() * 60)

    def drankWater(self):
        self.destroy()
        time.sleep(20 * 60)

    def createSettingFrame(self):
        self.settingFrame = ctk.CTkFrame(self)
        self.settingFrame.grid_columnconfigure(0, weight=1)
        self.settingFrame.grid_rowconfigure(0, weight=1)

        SliderFrame(
            self.settingFrame, 
            "Set your snooze time:", 
            (2, 4, 6, 8, 10), 
            (10, 1, 11), 
            self.updateSnoozeTime, 
            self.setSnooze).gridWidget(row=0, column=0)

        self.settingFrame.grid(row=1, column=0, sticky="nsew")

    def updateSnoozeTime(self, value):
        self.snoozeTime = value

    def setSnooze(self):
        return self.snoozeTime

if __name__ == "__main__":
    while True:
        window = Popup("black")
        window.mainloop()