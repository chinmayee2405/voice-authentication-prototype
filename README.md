# voice-authentication-prototype
A voice authentication prototype with GUI, DTW-based voice matching, and anti-spoofing detection using Python.
# Voice Authentication Prototype 🎙️🔐

A Python-based voice authentication system using **Dynamic Time Warping (DTW)**, **MFCC features**, and a simple **Tkinter GUI**.  
Includes a basic **anti-spoofing check** using Zero Crossing Rate (ZCR) and Energy detection.

## Features
- User registration with recorded voice sample  
- Authentication using DTW similarity of MFCC features  
- Basic anti-spoofing (detects low-energy or artificial input)  
- GUI built with Tkinter  

## Requirements
Install dependencies:
```bash
pip install -r requirements.txt
