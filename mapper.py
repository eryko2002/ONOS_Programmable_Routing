import json
import os

global data

def readJson(FILENAME):
	result=None
	with open(f'{os.path.join(os.getcwd(),FILENAME)}',"r") as file:
		result=json.load(file)
	return result

    
def get_ip_addresses(hosts, switch_list):
    ip_addresses = []
    for switch_id in switch_list:
        for host in hosts:
            for location in host["locations"]:
                if location["elementId"] == switch_id:
                    ip_addresses.extend(host["ipAddresses"])
                    break
    return ip_addresses

def getNodesFromJson(FILENAME):
	result=None
	nodes=[]
	with open(os.path.join(os.getcwd(),FILENAME),"r") as file:
		result = json.load(file)
		for switch in result["devices"]:
			nodes.append(switch["id"])
	
	return nodes

def getLinksFromJson(FILENAME):
    result = None
    links = []
    
    with open(os.path.join(os.getcwd(), FILENAME), "r") as file:
        try:
            result = json.load(file)
            links = result.get("links", [])
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    return links
	
def getDevices(FILENAME):
	result=None
	nodes=[]
	with open(os.path.join(os.getcwd(),FILENAME),"r") as file:
		result = json.load(file)
		for switch in result["devices"]:
			nodes.append(switch)
			print(switch)
	return nodes	

def getDeviceInfoSwitch(FILENAME):
	result=None
	nodes=[]
	with open(os.path.join(os.getcwd(),FILENAME),"r") as file:
		result = json.load(file)
		result=result["devices"]["switches"][0]
		for name,id in result.items():
			print(f'switch_name:{name},switch.ID:{id}')
			
	return None
	    
def map_switch_to_host(switch_id, json_file):
    data=None
    result=None
    with open(json_file, 'r') as file:
        data = json.load(file)

    switch_to_host_connections = data['connections']['switch2host'][0]
    switches_id = data['devices']['switches'][0]
    for switch_name, host_name in switch_to_host_connections.items():
        switchID_default = switches_id[f'{switch_name}']
        if switchID_default == switch_id:
            host_switch = switch_to_host_connections[f'{switch_name}']
            for host in data['devices']['hosts']:
                if host['name'] == host_name:
                    result=host['ip']
        else:
        	pass
        
    return result
    
    
def split_ip_address(ip_address):
    # Split the IP address into octets
    octets = ip_address.split('.')
    
    # Check if the IP address has four octets
    if len(octets) == 4:
        # Join the first three octets to form the network part
        network_part = '.'.join(octets[:3])

        # The fourth octet represents the host part
        host_part = octets[3]

        return network_part, host_part
    else:
        return None
    
def extract_ip_without_mask(ip_with_mask):
    # Split the IP address and mask
    ip_parts = ip_with_mask.split('/')
    
    # Check if the IP address has both parts
    if len(ip_parts) == 2:
        return ip_parts[0]  # Return only the IP address part
    else:
        return None
	
def run():
    # data=readJson("hosts.json")
    # result = get_ip_addresses(data["hosts"], lista)
    # print(result)

    # Example usage:
    # ip_address = "192.168.0.10"
    '''
    ip_address=str(input("Pass IP Address:"))
    network_part, host_part = split_ip_address(ip_address)

    if network_part is not None:
        print(f"Network Part: {network_part}")
        print(f"Host Part: {host_part}")
    else:
        print("Invalid IP address format.")    
    '''
    # Example usage:
    ip_with_mask = str(input("Pass ip_address/mask:"))
    ip_without_mask = extract_ip_without_mask(ip_with_mask)

    if ip_without_mask is not None:
        print(f"IP Address without Mask: {ip_without_mask}")
    else:
        print("Invalid IP address format.")


def run1():
	lista = ["of:0000000000000002", "of:0000000000000001", "of:0000000000000005"]
	for switch_id in lista:
		host_ip = map_switch_to_host(switch_id, json_file="deviceInfo.json")
		#print("Switch ID: {}, Host IP: {}".format(switch_id, host_ip))
		print(host_ip)
		
		    
if __name__ == "__main__":
	run()    


