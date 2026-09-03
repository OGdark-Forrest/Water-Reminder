from ultralytics import YOLO
import cv2
import customtkinter as ctk
import time
from win11toast import toast

model = YOLO("yolov8m.pt")

DRINKWARE = {"cup", "bottle", "wine glass"}

def startVerification():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Nothing to see")
            break

        results = model(frame, conf=0.2, iou=0.45, verbose=False)[0]

        drinkware_present = False

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = results.names[cls_id]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if label in DRINKWARE:
                drinkware_present = True
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        status = "DRINKWARE DETECTED" if drinkware_present else "no drinkware"
        if status == "DRINKWARE DETECTED":
            cap.release()
            cv2.destroyAllWindows()
            return "verified"
        color = (0, 255, 0) if drinkware_present else (0, 0, 255)
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow("Drinkware Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return "cancelled"

    cap.release()
    cv2.destroyAllWindows()

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
        winY = windowHeight - 2*self.HEIGHT - 150
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{winX}+{winY}")

        self.grid_columnconfigure(0, weight=1)

        self.overrideredirect(True)

        self.snoozeTime = 5
        self.isSetting = False
        self.snoozeCount = 0

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
        self.contentFrame = ctk.CTkFrame(self, fg_color="black")
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
        snoozeButton = ctk.CTkButton(
            buttonFrame,
            text=f"Snooze ({self.getSnoozeTime()} mins)",
            fg_color="red",
            command=self.snooze
        )
        snoozeButton.grid(row=0, column=1)
        if self.snoozeCount > 2:
            snoozeButton.configure(state="disabled")

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
        self.snoozeCount += 1
        self.destroy()
        time.sleep(self.getSnoozeTime() * 60)

    def drankWater(self):
        result = startVerification()
        if result == "verified":
            toast("Verified Succesfully")
            self.snoozeCount = 0
            self.destroy()
            time.sleep(20 * 60)
            return
        toast("Verification cancelled")

    def createSettingFrame(self):
        self.settingFrame = ctk.CTkFrame(self, fg_color="black")
        self.settingFrame.grid_columnconfigure(0, weight=1)
        self.settingFrame.grid_rowconfigure(0, weight=1)

        SliderFrame(
            self.settingFrame, 
            "Set your snooze time: (in minutes)", 
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