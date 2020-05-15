#!/bin/sh
while inotifywait -e modify,create,close_write,move,delete ./_layouts/; do
  make
done
