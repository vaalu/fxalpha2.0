#!/bin/sh
cd ~/build/source/scripts/nix
nohup ./start-alphaonegraphql.sh > /home/ubuntu/build/logs/alphaone-graphql.log &
echo "Inintialized Alpha One Graphql Server"
nohup ./start-alphaoneui.sh > /home/ubuntu/build/logs/alphaone-ui.log &
echo "Inintialized Alpha One UI Server"
nohup ./start-alphaonepy.sh > /home/ubuntu/build/logs/alphaone-py.log &
echo "Initialized Alpha Prime Websocket Server"
