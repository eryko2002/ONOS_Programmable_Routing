from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import json
import os

FILEPATH = os.path.join(os.getcwd(), "deviceInfo.json")



def startControllerOnSwitches(controller, switches):
    for i, switch in enumerate(switches):
        switch.start([controller])
        switch.cmd('ovs-vsctl set bridge s{} protocols=OpenFlow14'.format(i+1))


class MyTopo(Topo):
    def __init__(self, json_file=f'{FILEPATH}'):
        Topo.__init__(self)

        with open(json_file, 'r') as file:
            data = json.load(file)

        # Create hosts
        for host_info in data['devices']['hosts']:
            self.addHost(host_info['name'], ip=host_info['ip'])

         # Create switches
        for switches_list in data['devices']['switches']:
            for switch_name, switch_id in switches_list.items():
                # Remove "of:" prefix and convert to hexadecimal
                switch_id_hex = switch_id[3:]
                self.addSwitch(switch_name, dpid=switch_id_hex)
                print(f'Switchname: {switch_name}, SwitchID: {switch_id_hex}')


        # Create switch-to-switch links
        switch_to_switch_connections = data['connections']['switch2switch'][0]
        for source, connections in switch_to_switch_connections.items():
            for target, metric in connections.items():
                self.addLink(source, target, bw=metric, delay='2ms', loss=0.1)

        # Create switch-to-host links
        switch_to_host_connections = data['connections']['switch2host'][0]
        for switch, host in switch_to_host_connections.items():
            self.addLink(switch, host, bw=5, delay='1ms', loss=0.05)

def run(ip_address, port):
    topo = MyTopo()
    net = Mininet(topo=topo, switch=OVSSwitch,controller=RemoteController,build=False)

    # Add the remote controller
    c1 = RemoteController('c1', ip=ip_address)
    net.addController(c1)

    #net.build()
    net.start()
    c1.start()
    startControllerOnSwitches(c1,net.switches)
    CLI(net)
    net.stop()
    net.save("my_topology")

# Example usage
if __name__ == '__main__':
    setLogLevel('info')
    run(ip_address="172.16.1.52",port=6633)
