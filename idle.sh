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

get_pid () {
    CURRENT_PID=$(xdotool getactivewindow getwindowpid)
}

check_game_running () {
    CPU_STAT=$(ps -eo %cpu,pid --sort -%cpu | grep $CURRENT_PID | awk '{ print $1 }' )
    if [ $CPU_STAT == 0 ]; then
            echo -en "\r    Game Froze. Recovery initiated.${CUT}"
            pkill TERM $CURRENT_PID
            steam steam://rungameid/1048370
            sleep 10
            focus_idle_skilling
            get_pid
            xdotool getactivewindow windowmove 2000 2000
            xdotool mousemove 2314 1333
            xdotool click 1
            sleep 1.5
            return
    fi
}

switch_modes () {
    # takes start and destination as args, then click to destination
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
    # most of these star numbers are estimates
    star0=24
    star1=190
    star2=2080
    star3=20000
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
    midas_secs=37
    while [ $counter -le 10 ]
    do
        check_game_running

        echo -en "\r   ${ORANGE}Midas ${RED}Running...${NC}${CUT}"
    
        focus_idle_skilling

        xdotool key 3
        xdotool mousemove 2084 1180
        xdotool click --repeat 675 --delay 9 1
        # Toggle skills page to fight skills
        xdotool mousemove 1843 1302; xdotool click 1

        secs=$((midas_secs))
        while [ $secs -gt 0 ]
        do
            if [ $((secs%5)) -eq 0 ]; then
                    xdotool key 1+2+3+4+5
            fi
            echo -ne "\r   ${ORANGE}Midas ${GREEN}Paused...${NC} $secs ${CUT}"
            read -n 1 -t 1 -p "Enter Option to do something else: "$'\r' opto
            if [ "$opto" == 'r' ]; then
                    # return skills to support skills
                    xdotool mousemove 1843 1302; xdotool click 1
                    break
                elif [ "$opto" == 'q' ]; then
                    echo ''
                    exit
                elif [ "$opto" == 'e' ]; then
                    # return skills to support skills
                    xdotool mousemove 1843 1302; xdotool click 1
                    switch_modes 'midas' 'extract'
                    return
            fi
            : $((secs--))
        done
        # return skills to support skills
        xdotool mousemove 1843 1302; xdotool click 1
    done
}

echo -e "${ORANGE}Brandonds hilarious Midas Clicker!!!${NC}"

main () {
    focus_idle_skilling
    get_pid
    midas_clicks
}

main
