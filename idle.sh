#!/bin/bash

counter=0
RED='\033[0;31m'
ORANGE='\033[0;33m'
NC='\033[0m'
GREEN='\033[0;32m'
CUT='\033[0K'
CURRENT_SCREEN='fight'

focus_idle_skilling () {
    AW=$(xdotool search --name "^Idle Skilling$")
    if [ '$AW' ]; then
            xdotool windowactivate "${AW}"
        else
            exit
    fi
}

switch_modes () {
    # takes start and destination as args, then click to destination
    echo 'hello'
    focus_idle_skilling

    if [ $1 == 'midas' ] && [ $2 == 'extract' ]; then
            xdotool mousemove 2051 898
            xdotool click 1
            sleep 1
            tunnel_extract_farm && return
        elif [ $1 == 'extract' ] && [ $2 == 'midas' ]; then
            xdotool mousemove 1780 891
            xdotool click 1
            sleep 1
            midas_clicks && return
    fi
}

tunnel_extract_farm () {
    star1=24
    star2=240
    star3=2080
    speed=$((24100/60/60))
    tcounter=0
    stars=0
    extract_secs=$(($star3/$speed))

    xdotool mousemove 1719 992  # get spelunker A
    xdotool click 1
    sleep 0.1
    xdotool mousemove 2493 1267 # assuming ready to extract
    xdotool click 1
    sleep 0.1
    xdotool mousemove 1898 1336 # get bag
    xdotool click 1
    sleep 0.1
    xdotool click 1

    while [ $tcounter -le 10 ]
    do
        echo -en "\r   ${ORANGE}Tunnel Extract  ${RED}Jumping...${NC}${CUT}"
        focus_idle_skilling
        sleep 2.4
        # assuming jump in progress, can cause loss of learning or dig progress.
        # extract/jump location
        xdotool mousemove 2493 1267
        xdotool click 1 # jump
        sleep 30
        xdotool click 1 # extract
        # open the bag
        xdotool mousemove 1898 1336
        xdotool click 1
    done
}

midas_clicks () {
    midas_secs=51
    while [ $counter -le 10 ]
    do
        echo -en "\r   ${ORANGE}Midas ${RED}Running...${NC}${CUT}"
    
    focus_idle_skilling

        xdotool key 3
        xdotool mousemove 2084 1180
        xdotool click --repeat 700 --delay 9 1

        secs=$((midas_secs))
        while [ $secs -gt 0 ]
        do
            echo -ne "\r   ${ORANGE}Midas ${GREEN}Paused...${NC} $secs ${CUT}"
            read -n 1 -t 1 -p "Enter Option to do something else: "$'\r' opto
            if [ "$opto" == 'r' ]; then
                    break
                elif [ "$opto" == 'q' ]; then
                    echo ''
                    exit
                elif [ "$opto" == 'e' ]; then
                    switch_modes 'midas' 'extract'
                    return
            fi
            : $((secs--))
        done
    done
}
 
echo -e "${ORANGE}Brandonds hilarious Midas Clicker!!!${NC}"

midas_clicks
