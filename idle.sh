#!/bin/bash

counter=0
RED='\033[0;31m'
ORANGE='\033[0;33m'
NC='\033[0m'
GREEN='\033[0;32m'
CUT='\033[0K'
CURRENT_SCREEN='fight'
midas_secs=51

focus_idle_skilling () {
    AW=$(xdotool search --name "Idle Skilling")
    if [ '$AW' ]; then
            xdotool windowactivate "${AW}"
        else
            exit
    fi
}

midas_clicks () {
    while [ $counter -le 10 ]
    do
        echo -en "\r   ${RED}Running...${NC}${CUT}"
        focus_idle_skilling

        xdotool key 3
        xdotool mousemove 2084 1180
        xdotool click --repeat 700 --delay 9 1

        secs=$((midas_secs))
        while [ $secs -gt 0 ]
        do
            echo -ne "\r   ${GREEN}Paused...${NC} $secs ${CUT}"
            read -n 1 -t 1 -p "Enter Option to do something else: "$'\r' opto
            if [ "$opto" == 'r' ]; then
                break
            fi
            : $((secs--))
        done
    done
}

echo -e "${ORANGE}Brandonds hilarious Midas Clicker!!!${NC}"

midas_clicks
