import os
import librosa
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import tkinter as tk
from tkinter import messagebox

# Setup
USER_DIR = "users"
if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)

# Record voice
def record_voice(filename, duration=5, fs=16000):
    messagebox.showinfo("Recording", "Recording... Please say: 'My voice is my password'.")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, fs, audio)

# Extract MFCC features
def extract_features(filename):
    y, sr = librosa.load(filename, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    # Normalize to handle volume variations
    mfcc = (mfcc - np.mean(mfcc, axis=1, keepdims=True)) / np.std(mfcc, axis=1, keepdims=True)
    return mfcc.T  # Don't average; DTW needs the full sequence

# DTW comparison
def match_using_dtw(file1, file2):
    mfcc1 = extract_features(file1)
    mfcc2 = extract_features(file2)
    distance, _ = fastdtw(mfcc1, mfcc2, dist=euclidean)
    print(f"[DEBUG] DTW Distance: {distance}")
    return distance

# Anti-spoofing check
def is_spoofed(filename):
    y, sr = librosa.load(filename, sr=None)
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    energy = np.mean(librosa.feature.rms(y=y))
    if zcr < 0.01 or energy < 0.001:
        return True
    return False

# Register user
def register():
    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Error", "Enter a username.")
        return
    filepath = os.path.join(USER_DIR, f"{username}.wav")
    record_voice(filepath)
    messagebox.showinfo("Registered", f"User '{username}' registered successfully!")

# Authenticate user
def authenticate():
    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Error", "Enter a username.")
        return

    stored_file = os.path.join(USER_DIR, f"{username}.wav")
    if not os.path.exists(stored_file):
        messagebox.showerror("Error", "User not registered.")
        return

    temp_file = "temp_test.wav"
    record_voice(temp_file)

    if is_spoofed(temp_file):
        os.remove(temp_file)
        messagebox.showerror("Spoofing Detected", "Fake or unclear voice input.")
        return

    # Compare using DTW
    distance = match_using_dtw(temp_file, stored_file)
    os.remove(temp_file)

    threshold = 800  # Adjusted threshold for better tolerance
    if distance <= threshold:
        messagebox.showinfo("Access Granted", f"Welcome, {username}!")
    else:
        messagebox.showerror("Access Denied", "Voice not recognized.")

# GUI Actions
def show_action_buttons():
    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Error", "Please enter a username.")
        return
    register_button.pack(pady=5)
    authenticate_button.pack(pady=5)

# GUI Setup
root = tk.Tk()
root.title("Voice Authentication")
root.geometry("300x250")

tk.Label(root, text="Enter Username").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

submit_button = tk.Button(root, text="Submit", command=show_action_buttons)
submit_button.pack(pady=10)

register_button = tk.Button(root, text="Register", command=register)
authenticate_button = tk.Button(root, text="Authenticate", command=authenticate)

root.mainloop()
