# GOS 2026 Bunny Bots Scouting App

## Initial setup

NOTE: On windows, depending on how python is installed, you may need to do `py` instead of `python3`

1. Create a virtual environment for the repository
`py -m venv .venv`

2. Activate your virtual environment
Windows: `.venv/Scripts/Activate.ps1`
OSX/Linux: `source .venv/bin/activate`

3. Install python dependencies
```
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -r requirements-live.txt
```

## Running Jupyter Notebooks
jupyter lab

## Running Shiny App
shiny run app.py

Note: You can add ` --reload` to that to have any changes in PyCharm auto update the website. It doesn't work great on Windows though.

## Hosted Website
https://girlsofsteelrobotics.github.io/2026BunnyBotsScouting/
