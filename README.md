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

## Challenges/Difficulties
* One challenge I encountered during this process was the duplication of sound triggering when using multiple-hand detection. When one hand was inside the box and the other hand was outside the box, it kept creating duplicated sounds. It was not supposed to make duplicated sounds as when one hand is inside the box and hands are not outside the box yet, that would be consider as one sound.
Because this algorithm defaults to switching between left and right hands by default, it causes duplicate sound when using multiple hand detection. I have additionally created the cooldown to stop the duplicate sound, but that was only a temporary solution.

#Solution
* To solve this, I created current_hits of each instrument and hit_state of each instrument.
Current_hit would count how many hands are currently inside the box for each instrument.
Hit_state stores how many previous frame's hit were counted for each instrument.

If current_hits>hit_state, it would execute the sound. And having hit_state[name] = current_hits[name] in the end, reinitialize hit_state so it prevents from making duplicated sound.

Remember, after the next frame, the current_hit would be initialized back to 0, and leaving hands should not sound. Hit_state then becomes 0.  Then, repeats this process.

## Project Structure

```text
air-drum/
|__ main.py
|__ requirements.txt
|__ pictures/
|__ soundEffect/
|__ README.md
```
