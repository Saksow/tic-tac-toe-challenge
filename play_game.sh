#!/bin/bash

if ! command -v http; then
  echo 'You need HTTPie to run this script!'
  exit 1
fi

if [ -z "$DEMO_GAME_ID" ]; then
  echo 'You need to set the env variable DEMO_GAME_ID!'
  exit 1
fi

URL=:5000/api/games

# Print commands and their arguments as they are executed.
set -x

http GET $URL/"$DEMO_GAME_ID"
http POST $URL/"$DEMO_GAME_ID"/moves player_number:=1 tile_number:=5
http POST $URL/"$DEMO_GAME_ID"/moves player_number:=2 tile_number:=9
http POST $URL/"$DEMO_GAME_ID"/moves player_number:=1 tile_number:=3
http POST $URL/"$DEMO_GAME_ID"/moves player_number:=2 tile_number:=2
http POST $URL/"$DEMO_GAME_ID"/moves player_number:=1 tile_number:=7
# Player number 1 won the game
