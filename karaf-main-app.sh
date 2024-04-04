#!/bin/bash

ONOS_IP=172.16.1.52
ONOS_CONTAINER="onos-application"
remove_known_hosts_entry() {
    ssh-keygen -f "$HOME/.ssh/known_hosts" -R "[$ONOS_IP]:8101" &>/dev/null
}


activate_onos_apps() {
    read -p "Do you want to run app activate org.onosproject.fwd?yes-1, no-2 :" response
    local apps
    if [[ $response -eq "1" ]]; then
    	apps="app activate org.onosproject.fwd;app activate org.onosproject.openflow;app activate org.onosproject.cli"
    elif [[ $response -eq "2" ]]; then
    	apps="app activate org.onosproject.openflow;app activate org.onosproject.cli"
    fi
    echo -e "\nActivating onos apps in progress..."
    ssh-add "$HOME/.ssh/id_rsa"
    ssh -p 8101 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null karaf@$ONOS_IP $apps 
}

check_docker_running(){
	local docker_run=$1
	if docker ps -q --filter $ONOS_CONTAINER 2>/dev/null; then
		echo -e "\nContainer $ONOS_CONTAINER is already running."
	else
		echo -e "Container ID: $docker_run"
		sleep 1
		echo -e "\nContainer $ONOS_CONTAINER has been started."
	fi

}


read -p "Press 1 if you want to run docker container!" runner
if [[ $runner -eq "1" ]]; then
	#echo -e "\nThe process of running onos app in docker container is in progress.."
	sudo service openvswitch-switch stop
	sleep 1
	cmd=($(docker run -itd --rm --network business -p 8181:8181 -p 6653:6653 --ip $ONOS_IP --name onos-application onosproject/onos 2>&1))
    	check_docker_running "$cmd" > /dev/null
else
	echo -e "\nContinue..."
fi

echo -e "--------------------------------------------\nIf you run command python <filename.py>, press 1\nIf you run command mn --custom <filename.py> --topo mytopo, then press 2\nIf you want to run tree topology, then press 3
If you want to run linear topology, press 4\nIf you do not want to run a mininet script, then press anything else\n--------------------------------------------"
read -p "Pass the number: " option
if [[ $option -eq "1" ]] || [[ $option -eq "2" ]]; then
	read -p "Pass the name of python file:" filename
fi

remove_known_hosts_entry

echo -e "\nSSH Session initiation is underway!\n"
sudo mn -c
sudo mn -c
sleep 3
activate_onos_apps
#ssh -p 8101 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null karaf@172.20.0.51
sleep 2

if ! sudo service openvswitch-switch status &>/dev/null; then
    sudo service openvswitch-switch start
fi

if [[ $option -eq "1" ]] && [[ ${#filename} >0 ]]; then
	sudo python ~/Desktop/onosFolder/$filename
elif [[ $option -eq "2" ]] && [[ ${#filename} >0 ]]; then
        sudo mn --custom ~/Desktop/onosFolder/$filename --controller remote,ip=$ONOS_IP --mac --switch ovs,protocols=OpenFlow14 --topo mytopo 

elif [[ $option -eq "3" ]]; then
	local depth=2
	local fanout=8
	echo -e "You checked tree topology. Default values: depth=2,fanout=8.\nYou can change it, by passing new values...\n"
	read -p "Value of depth:" depth1
	read -p "Value of fanout:" fanout1
	if [[ -z $depth1 ]] && [[ -z $fanout1 ]]; then depth=depth1;fanout=fanout1
	fi
	 
	sudo mn --topo=tree,depth=2,fanout=8 --controller remote,ip=$ONOS_IP --mac --switch ovs,protocols=OpenFlow14

elif [[ $option -eq "4" ]]; then
	local depth=4
	read -p "You checked linear topology. Pass the value of switches:" depth
	sudo mn --topo=linear,$depth --controller remote,ip=$ONOS_IP --mac --switch ovs,protocols=OpenFlow14

else
	echo -e "\nNeither of mininet scripts will be activated. Closing the process..."
	sleep 2
	exit 0
fi


exit 0

