#!/usr/bin/env fish
# generated from catkin/cmake/template/local_setup.fish.in

# since this file is sourced either use the provided _CATKIN_SETUP_DIR
# or fall back to the destination set at configure time

if test -z $_CATKIN_SETUP_DIR
    set _CATKIN_SETUP_DIR /media/Disk_D/CUFE_CMP_2024/Fourth_year_26/first_semster/CMP4021_CR/project/multi-robot-exploration/multi-robot-exploration_ws/devel/.private/limo_bringup
end

set CATKIN_SETUP_UTIL_ARGS "--extend --local"
source "$_CATKIN_SETUP_DIR/setup.fish"

set -e CATKIN_SETUP_UTIL_ARGS
