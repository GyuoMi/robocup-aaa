#!/usr/bin/env bash
#settings
distrobox_distro="ubuntu-24-04"
session_name="robocup"

####################################################
#YOU NEED TO CHANGE THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!#
####################################################
#it needs to be the top directory of everything
path_to_robocup="~/Documents/Work/Wits/AAA/robocup-aaa/"

window_1="client"
window_2="server"
window_3="renderer"
window_4="work"

# Check if the session exist, deletes it if it does
if tmux has-session -t $session_name 2>/dev/null; then
	tmux kill-session -t $session_name
fi

tmux new-session -d -s "$session_name" -c $path_to_robocup

tmux new-window -d -t "$session_name" -n "$window_1"
tmux send-keys -t "$session_name:$window_1" "distrobox enter $distrobox_distro" Enter
sleep 1
tmux send-keys -t "$session_name:$window_1" "rcssserver3d" Enter

tmux new-window -d -t "$session_name" -n "$window_2"
tmux send-keys -t "$session_name:$window_2" "distrobox enter $distrobox_distro" Enter
sleep 1
tmux send-keys -t "$session_name:$window_2" "cd WitsFC-Codebase" Enter
tmux send-keys -t "$session_name:$window_2" "./start.sh" Enter

tmux new-window -d -t "$session_name" -n "$window_3"
tmux send-keys -t "$session_name:$window_3" "distrobox enter $distrobox_distro" Enter
sleep 1
tmux send-keys -t "$session_name:$window_3" "./bin/roboviz.sh" Enter

#create an extra window for anything else
#tmux new-window -d -t "$session_name" -n "$window_4"

tmux attach -t "$session_name" 
