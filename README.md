# Hand Gesture Recognition Web Application 🤚

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-red.svg)](https://opencv.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.8+-orange.svg)](https://mediapipe.dev)

A modern web application that uses computer vision to recognize hand gestures in real-time. Built with Flask, OpenCV, and MediaPipe.

## ✨ Features

- **Real-time hand detection** using MediaPipe's high-performance hand tracking
- **8+ gesture recognition** with high accuracy
- **Beautiful web interface** with live camera feed
- **Gesture smoothing** to prevent false triggers
- **Multi-hand support** (up to 2 hands)
- **Screenshot capture** functionality
- **Responsive design** works on all devices

## 🎯 Supported Gestures

| Gesture | Name | Action |
|---------|------|--------|
| 👍 | Thumbs Up | Volume Up |
| 👎 | Thumbs Down | Volume Down |
| ✌️ | Peace | Play/Pause |
| 👊 | Fist | Mute |
| ✋ | Open Palm | Stop |
| 👌 | Okay | Confirm |
| 🤙 | Call Me | Answer Call |
| 🤘 | Rock On | Party Mode |

## 🛠️ Technology Stack

### Backend
- **Python** - Core programming language
- **Flask** - Web framework
- **OpenCV** - Image processing
- **MediaPipe** - Hand landmark detection
- **NumPy** - Mathematical operations

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling and animations
- **JavaScript** - Interactive features
- **Font Awesome** - Icons

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam
- Modern web browser (Chrome, Firefox, Edge)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hand-gesture-webapp.git
   cd hand-gesture-webapp