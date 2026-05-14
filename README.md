# Air-drum simulator
Real-time virtual drum kit. Built with using MediaPipe hand-tracking & computer vision.
The program tracks hand movement with a webcam and plays drum sounds when your finger hits different drum zones on the screen.

## Installation

Clone the repository:

```bash
git clone <https://github.com/hiromaruyama/air-drum.git>
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
|__ main.py
|__ requirements.txt
|__ pictures/
|__ soundEffect/
|__ README.md
```
