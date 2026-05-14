# Air-drum simulator
Real-time virtual drum kit. built with MediaPipe hand-tracking and computer vision.
The program tracks hand movement with a webcam and plays drum sounds when your finger hits different drum zones on the screen.

## Installation

Clone the repository:

```bash
git clone <your-repo-url>
cd air-drum
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python3 main.py
```

## How to play

* Move your hand in front of the webcam
* Hit virtual drum zones to play sounds
* Press `q` to quit

## Project Structure

```text
air-drum/
├── main.py
├── requirements.txt
├── pictures/
├── soundEffect/
└── README.md
```
