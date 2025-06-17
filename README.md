# 🖱️ Virtual Mouse using Hand Gesture Recognition

A Python-based Virtual Mouse system that allows you to control your computer’s mouse cursor using hand gestures captured via a webcam — no physical mouse required!

## ✨ Features

- Move cursor with your index finger
- Left and right click gestures
- Scroll using hand movement
- Drag & drop functionality
- Works in real-time with webcam input

## 📹 Demo

![Virtual Mouse Demo](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*-wc57H4KMXJXZpeze0eVSQ.gif) <!-- Replace with actual gif/video link or remove -->

## 🛠️ Tech Stack

- Python 🐍
- OpenCV 🎥
- MediaPipe (optional, for hand detection) ✋
- PyAutoGUI for mouse control

## 🚀 How It Works

1. Uses webcam to capture real-time video feed.
2. Detects hand landmarks using OpenCV or MediaPipe.
3. Tracks specific finger positions and maps them to screen coordinates.
4. Executes mouse actions (clicks, scrolls, drag) using gesture logic and `pyautogui`.

## 📦 Installation

```bash
git clone https://github.com/yourusername/virtual-mouse.git
cd virtual-mouse
pip install -r requirements.txt
````

### Requirements

* Python 3.7+
* OpenCV
* PyAutoGUI
* MediaPipe *(if used)*

Install manually:

```bash
pip install opencv-python pyautogui mediapipe
```

## ▶️ Usage

```bash
python virtual_mouse.py
```

* Ensure your webcam is connected.
* Make sure your hand is visible and well-lit.
* Use finger gestures to control the cursor.

## ✋ Gesture Controls

| Gesture             | Action      |
| ------------------- | ----------- |
| Index finger up     | Move cursor |
| Index + middle up   | Left click  |
| Thumb + index touch | Drag        |
| Pinch (2 fingers)   | Scroll      |

*(You can modify these as per your implementation.)*

## 🧠 Future Improvements

* Multi-hand support
* Gesture customization UI
* Voice-triggered gestures
* Cross-platform calibration tool

## 📁 File Structure

```
virtual-mouse/
├── main.py
├── README.md
├── requirements.txt
```

## 🙋‍♂️ Author

**Gourab Chakraborty**
🎓 B.Tech CSE @ ICFAI University Tripura
📺 [YouTube: Gourab's Pixel Path](https://www.youtube.com/@GourabsPixelPath)
🔗 [LinkedIn](https://linkedin.com/in/yourprofile) • [GitHub](https://github.com/Gourabbabu)

## 📄 License

This project is open-source under the [MIT License](LICENSE).

---

> If you like this project, consider giving it a ⭐ on GitHub!

