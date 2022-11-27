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
    CPU_STAT=$(ps -eo %cpu,pid --sort -%cpu | grep "\b${CURRENT_PID}\b" | awk '{ print $1 }' )
    if [ $CPU_STAT == 0 ]; then
            echo -en "\r    Game Froze. Recovery initiated.${CUT}"
            kill $CURRENT_PID
            steam  steam://rungameid/1048370
            sleep 10
            focus_idle_skilling
            get_pid
            xdotool getactivewindow windowmove 2000 2000
            xdotool mousemove 2314 1333
            xdotool click 1
            sleep 1.5
            read -p "Temporary safety feature... Press any key to continue"
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
            # works for any screen on top page 1
            xdotool mousemove 1780 891
            xdotool click 1
            sleep 1
            # bottom skill goes back to page one every time you leave
            toggle_bottom_skill
            toggle_bottom_skill
            toggle_top_skill
            midas_clicks && return
    fi
}


tunnel_extract_farm () {
    # set star to level of bag to farm
    star=3
    starwee=$(($star-1))
    valuedang=52
    speed=$((1980000))
    tcounter=0

    # valuedang is the value that reaches the next star. Multiplied by 10^(number of stars) - looking for value formula
    # speed is the speed per hour in the game after all multipliers and levels, then I convert to per second.
    extract_secs=$((($valuedang*(10**$starwee))/($speed/60/60)))

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
        sleep 2.4 # wait for animation
        # assuming jump in progress, can cause loss of learning or dig progress.
        # extract/jump location
        xdotool mousemove 2493 1267
        xdotool click 1 # jump
        sleep $(($extract_secs+1))
        xdotool click 1 # extract
        # open the bag
        xdotool mousemove 1898 1336
        xdotool click 1
    done
}


toggle_top_skill () {
    xdotool mousemove 1843 1302
    xdotool click 1
}


toggle_bottom_skill () {
    xdotool mousemove 1812 1366             # location of other skills, assumes on correct page
    xdotool click 1
    sleep 0.1
}


toggle_mark () {
    toggle_bottom_skill
    xdotool key 1
    sleep 0.1

    if [ ! -z $1 ]; then                 # strafe while you're at it
            xdotool mousemove 1999 1311  # strafe has no key
            xdotool click 1
            sleep 0.1
    fi

    toggle_top_skill
}


gain_strafe () {
    strafe_count=0
    echo hello
    while [ $strafe_count -lt 30 ]
    do
        # go to portal screen
        xdotool mousemove 1994 892
        xdotool click 1
        sleep 1
        # go to lava guy
        xdotool mousemove 1667 1057
        xdotool click 1
        sleep .5
        # go to craft
        xdotool mousemove 1915 891
        xdotool click 1
        sleep 1
        : $((strafe_count++))
    done
    switch_modes 'extract' 'midas'
    return
}


midas_clicks () {
    midas_secs=34
    strafe=1
    mark=1

    while [ $counter -le 10 ]
    do
        check_game_running

        echo -en "\r   ${ORANGE}Midas ${RED}Running...${NC}${CUT}"

        focus_idle_skilling

        if [ $mark == 1 ]; then         # turn mark on
            toggle_mark
        fi

        xdotool key 3                                   # activate Midas
        xdotool mousemove 2084 1180                     # move mouse to empy area
        xdotool click --repeat 650 --delay 9 1          # click a lot
        sleep 0.1
        # Toggle skills page to fight skills
        toggle_top_skill

        if [ $mark == 1 ]; then
            toggle_mark '1'
        fi

        secs=$((midas_secs))
        while [ $secs -gt 0 ]
        do
            if [ $((secs%2)) -eq 0 ]; then
                    xdotool key 1+2+3+4+5; xdotool mousemove 2518 1241; xdotool click 1 &
            fi
            echo -ne "\r   ${ORANGE}Midas ${GREEN}Paused...${NC} $secs ${CUT}"
            read -n 1 -t 1 -p "Enter Option to do something else: "$'\r' opto
            if [ "$opto" == 'r' ]; then
                    echo -ne "\r${CUT}\n"
                    break
                elif [ "$opto" == 'q' ]; then
                    toggle_top_skill
                    exit
                elif [ "$opto" == 'e' ]; then
                    # return skills to support skills
                    toggle_top_skill
                    switch_modes 'midas' 'extract'
                    return
                elif [ "$opto" == 's' ]; then
                    # f-strafe
                    gain_strafe
            fi
            : $((secs--))
        done
        # return skills to support skills
        toggle_top_skill
    done
}


main () {
    echo -e "${ORANGE}Brandonds hilarious Midas Clicker!!!${NC}"
    focus_idle_skilling
    get_pid
    midas_clicks
}

main
