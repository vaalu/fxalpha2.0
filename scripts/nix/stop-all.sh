#!/bin/sh
killall node
echo "Node Services stopped"

curl http://localhost:5000/shutdown
echo
echo "Python server stopped"