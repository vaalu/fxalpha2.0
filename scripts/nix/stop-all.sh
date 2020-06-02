#!/bin/sh
# killall node
# echo "Node Services stopped"
# curl http://localhost:5000/shutdown
pkill -9 python
pkill -9 python3
echo
echo "Python server stopped"