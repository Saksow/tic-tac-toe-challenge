#!/bin/bash

if ! command -v http; then
  echo 'You need HTTPie to run this script!'
  exit 1
fi

URL=:5000/api/games

# Print commands and their arguments as they are executed.
set -x

http GET $URL # Empty list of games
http POST $URL players:='[{"name": "Mario"}, {"name": "Luigi"}]'
# You should now copy the game "id" and set it to DEMO_GAME_ID
# export DEMO_GAME_ID=<COPIED_ID>
