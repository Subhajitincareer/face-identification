import os
import time
import threading
from datetime import datetime
import subprocess

import speech_recognition as sr
from PIL import ImageGrab, Image
import cv2
import numpy as np
import mss

import tkinter as tk
import win32clipboard
from io import BytesIO

TRIGGER_PHRASES = {
    "take screenshot",
    "screenshot",
    "take picture",
    "স্ক্রিনশট নাও",
    "স্ক্রিনশট নিন",
}

START_RECORDING_PHRASES = {
    "start recording",
    "ভিডিও শুরু করো",
    "রেকর্ডিং শুরু করো",
}

STOP_RECORDING_PHRASES = {
    "stop recording",
    "ভিডিও বন্ধ করো",
    "রেকর্ডিং বন্ধ করো",
}

# The user mentioned "window shutdown hoy na", so let's add a basic trigger for shutdown if they meant that.
SHUTDOWN_PHRASES = {
    "window shutdown",
    "কম্পিউটার বন্ধ করো",
    "shutdown computer"
}

SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
VIDEO_DIR = os.path.join(os.getcwd(), "videos")

is_recording = False
recording_thread = None

def copy_image_to_clipboard(filepath):
    try:
        image = Image.open(filepath)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
    except Exception as e:
        print(f"Clipboard copy error: {e}")

def copy_file_to_clipboard(filepath):
    try:
        import struct
        DROPFILES_SIZE = 20
        stg = struct.pack('IIIIi', DROPFILES_SIZE, 0, 0, 0, 1)
        paths = filepath.replace('/', '\\').encode('utf-16le') + b'\0\0' + b'\0\0'
        data = stg + paths
        
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_HDROP, data)
        win32clipboard.CloseClipboard()
    except Exception as e:
        print(f"Clipboard copy error: {e}")

def show_popup(filepath):
    def _run_ui():
        root = tk.Tk()
        root.title("Capture Saved")
        root.attributes('-topmost', True)
        
        window_width = 350
        window_height = 100
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{window_width}x{window_height}+{screen_width - window_width - 20}+{screen_height - window_height - 60}")
        
        def on_copy():
            if filepath.endswith('.png'):
                copy_image_to_clipboard(filepath)
            else:
                copy_file_to_clipboard(filepath)
            print("Copied to clipboard.")
            root.destroy()
            
        def on_delete():
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"Deleted: {filepath}")
            root.destroy()
            
        def on_open():
            subprocess.Popen(f'explorer /select,"{filepath}"')
            root.destroy()
            
        def on_close():
            root.destroy()

        filename = os.path.basename(filepath)
        tk.Label(root, text=f"Saved: {filename}", font=("Arial", 10, "bold")).pack(pady=10)
        
        btn_frame = tk.Frame(root)
        btn_frame.pack()
        
        tk.Button(btn_frame, text="Copy File", command=on_copy).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete", command=on_delete, fg="red").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Open Folder", command=on_open).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Close", command=on_close).pack(side=tk.LEFT, padx=5)
        
        root.mainloop()

    ui_thread = threading.Thread(target=_run_ui)
    ui_thread.start()

def take_screenshot() -> str:
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(SCREENSHOT_DIR, f"screenshot_{timestamp}.png")
    image = ImageGrab.grab()
    image.save(filepath)
    return filepath

def record_screen():
    global is_recording
    os.makedirs(VIDEO_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Standard mp4 format
    filepath = os.path.join(VIDEO_DIR, f"video_{timestamp}.mp4")
    
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        width, height = monitor["width"], monitor["height"]
        
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(filepath, fourcc, 10.0, (width, height))
        
        while is_recording:
            # mss is extremely fast and light on CPU
            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            out.write(frame)
            time.sleep(0.08) # ~12 FPS, frees CPU for voice recognition
            
        out.release()
    print(f"\n[Video saved: {filepath}]\n")
    show_popup(filepath)

def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())

def listen_loop() -> None:
    global is_recording, recording_thread
    
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    print("=" * 60)
    print("Voice Screenshot & Screen Recording Tool")
    print("Commands:")
    print(" - 'take screenshot'")
    print(" - 'start recording'")
    print(" - 'stop recording'")
    print(" - 'window shutdown'")
    print("Press Ctrl+C to stop.")
    print("=" * 60)

    try:
        with sr.Microphone() as source:
            print("Calibrating microphone...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Microphone ready.\n")
    except Exception as exc:
        print(f"Microphone initialization failed: {exc}")
        return

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                # Allow background threads CPU time while listening
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            print("Recognizing...")
            text = recognizer.recognize_google(audio, language="en-US")
            print(f"Heard: {text}")
            normalized = normalize_text(text)

            if any(phrase in normalized for phrase in TRIGGER_PHRASES):
                filepath = take_screenshot()
                print(f"Screenshot saved: {filepath}\n")
                show_popup(filepath)
                
            elif any(phrase in normalized for phrase in START_RECORDING_PHRASES):
                if not is_recording:
                    is_recording = True
                    recording_thread = threading.Thread(target=record_screen, daemon=True)
                    recording_thread.start()
                    print("Started recording...\n")
                else:
                    print("Already recording.\n")
                    
            elif any(phrase in normalized for phrase in STOP_RECORDING_PHRASES):
                if is_recording:
                    print("Stopping recording...")
                    is_recording = False
                    # Don't join(), let it finish asynchronously so mic doesn't hang
                else:
                    print("Not currently recording.\n")

            elif any(phrase in normalized for phrase in SHUTDOWN_PHRASES):
                print("Shutdown command detected!")
                os.system("shutdown /s /t 10")
                break

            else:
                print("No valid command detected.\n")

        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            print("Could not understand the speech.\n")
        except sr.RequestError as exc:
            print(f"Speech recognition service error: {exc}\n")
            time.sleep(2)
        except KeyboardInterrupt:
            print("\nStopped.")
            if is_recording:
                is_recording = False
            break
        except Exception as exc:
            print(f"Unexpected error: {exc}\n")
            time.sleep(1)

if __name__ == "__main__":
    listen_loop()
