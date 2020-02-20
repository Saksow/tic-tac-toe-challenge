# That tic-tac-toe REST API
A simple but comprehensive REST API for tic-tac-toe.

## Context
This is a solution to a coding assignment sent by [Anaconda](
https://www.anaconda.com/anaconda-careers/). The problem statement can be 
viewed [here](./README.md).

## Technologies and tools
This application is based on the following:
* [Flask](https://pypi.org/project/Flask): a lightweight web application framework for Python.
* [Connexion](https://pypi.org/project/connexion): an OpenAPI first framework on top of Flask.
* [Flask-Injector](https://pypi.org/project/Flask-Injector): adding dependency injection for Flask.
* [Redis](https://redis.io): a key-value data store.
* [Poetry](https://python-poetry.org/): a tool to manage Python dependencies.

## Run the app
Make sure you have `docker-compose` installed, then just run:
```shell script
docker-compose up  # You can pass the option `-d` for detached mode
```
This will start 2 services:
* **flask**: Flask app, by default running on 0.0.0.0:5000. See `Dockerfile` for full config.
* **redis**: Redis storage backend with enabled persistence.

## View the app
You can visit http://0.0.0.0:5000/api/ui/ to see the OpenAPI UI and try the
API in a browser. There is a description for every operation and further down in `Schemas` you can
find an explanation for the fields accepted/returned by the API.

## Try the app
There are 2 demo shell scripts that can let your try the app:
```shell script
./new_game.sh
export DEMO_GAME_ID="<COPY_GAME_ID"
./play_game.sh
```

## Test the app
To run the automated tests you need to install the dev dependencies.

### Using Poetry
Poetry is a relatively new tool to package Python projects and manage their
dependencies. It's probably not worth it for such a small app but it was cool
to try. You can skip to next section if you want to use a virtual env.

If you are still reading, [install](https://python-poetry.org/docs/#installation)
Poetry, then run:
```shell script
poetry run pytest -q --flake8 --isort --cov=.
```

### Using a virtual env
For convenience, a `requirements.txt` file has been generated using Poetry.
Run these commands:
```shell script
python3.6 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q --flake8 --isort --cov=.
```

*These tests ran successfully on `Ubuntu 18.04.3 LTS`.*

## Improvements
What could we do if we had twice the time?
* Tests: currently only having unit tests, we should add a fixture representing a test client then
make API calls. This fixture can have a mocked Storage or FakeStrictRedis injected into the app.
* UI/CLI: add a wrapper that lets users interact with the API to list available games, start a new
game and play rounds.
* Undo: something cool we could add is an "undo" endpoint which can simply remove the latest move
and allow a player to make another move.

## Technical choice in API
I took the freedom to deviate from this requirement: 
>POST /api/games/\<id>: Update the Game with the given ID, replacing its data with the newly POSTed data.

First, I think if we want to update an existing game to a new state we should use
`PUT` instead. `POST` is known to be non-idempotent as it usually creates new
resources, therefore repeating the same `POST` request should not keep our
server in the exact same state, which is not respected by this requirement.  
Second, `PUT` usually requires sending all the resource data which makes it
idempotent, unfortunately for our case this is a waste because we know that
the only thing that a player can add while playing a game is one single move.  
So for these reasons, I made the choice to change this to:
```http request
POST /api/games/<id>/moves
```
This design allows us to easily build a snapshot of the board by combining
all moves but additionally it offers a historical view on it, which we could
use for example to show a replay of finished games or add an undo
functionality.
