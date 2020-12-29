# HoTS Py Bot

This is a pixel scanner (on steroids) bot for Heroes of The Storm, a MOBA by Blizzard
This projects makes extensive use of the OpenCV2 library for python, it uses threads and processes to parallelize the screen analysis making data acquisition really fast and on par with human performace.

The goal for this bot is to play and win games VS AI with the help of machine learning algorithms (in the future), in the current state the bot can determine:
* Game State
  * Lobby
  * Roster
  * Loading Screen (and map side)
  * Thanks screen
  * In game screen
  * mvp screen
  * after-game screen (leave screen)
Once in game it can track:
* Own hero HP
* Teams levels
* Map:
  * own structures
  * enemy structures
  * camps / objectives
  * Player position (dodgy)

All this is possible tanks to the use of the opencv2 library.
It uses 2 types of matching, color matching and tempalte matching to determine the game state and track structures players and hp. 

The short-term goal is to make it gather enough data to feed to the ML algorithm.


## How to run the bot

### Requirements

1. [tesseract-ocr](https://github.com/tesseract-ocr/tesseract)
2. [redis](https://redis.io/) server

### Setup
1. clone the repo: `git clone https://github.com/mozempk/HoTSPyBot.git`
2. cd into the repo folder: `cd /path/to/repo/HoTSPyBot`
3. create a python3 virtual environment: `python -m venv /path/to/repo/HoTSPyBot/.venv`
4. activate the virtual environment, you will need to run the proper `activate` script for your OS. plese refer to [this guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment)
5. install tesseract-ocr, refer to [this guide](https://github.com/tesseract-ocr/tesseract)
6. install python dependencies: `pip install -r requirements.txt`
7. generate the template files: 

```shell
  cd /path/to/repo/HoTSPyBot/Utils
  python ./templateFileBuilder.py
```
8. create a `.env` file in the root of the repo
9. inside it place the redis connection string, eg: `REDIS=redis://default:password@host:port`
10. run the main script: `python main.py`

You can checkout app state updating in real-time at http://localhost:3000


Data that remains to be acquired:
1. enemy and allied heroes position in the hero's FoV
2. track enemy and friendly minions in the hero FoV
3. ~~Teams' level (OCR)~~
4. Own cooldowns (OCR)
5. determine What own spells do (it needs to be as generic as possible) ?

