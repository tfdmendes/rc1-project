# TABLE OF CONTENT



# USEFUL COMMANDS

### ESW3
```sh
SW> show iproute			# Shows the default gateway
SW> show ipif				# Shows the ip address
SW> show fdb				# Shows the switching table
SW> show vlan-switch			# Shows the vlan table
SW> show mac-address-table		# Shows the mac address table
```

### Router
```sh
R> show ip route 			# Show routing table
```

---

<div style="page-break-after: always;"></div>


# VLAN CONFIGURATION

## Configure ESW VLANs

```sh
SW> vlan database			# Enter VLAN configuration mode
SW> vlan <vlanID>			# Create <vlanID>
SW> exit				# Exit vlan Database
SW> conf t				# Enter configuration mode
SW> interface range F1/y - z		# Selects the range of interfaces for configuration
SW> switchport acess vlan <vlanID>	# Assigns the selected ports to <vlanID>
SW> end					# Exit current configuration
SW> write				# Save running configuration
```

## Set Switch port to trunk
Configures the interface as a trunk port to carry traffic for multiple VLANs using 802.1Q encapsulation
```sh
SW> interface Fx/y 			# Selects the interface
SW> switchport mode trunk 		# Sets the selected port to trunk
```

## Configure IP to VLAN 
```sh
SW> conf t				# Enter configuration mode
SW> interface vlan <vlanID> 		# Select VLAN <ID> interface for configuration
SW> ip address <addr> <mask> 		# Assigns IP addr and subnet mask to VLAN <ID>
SW> no shutdown 			# Enables VLAN interface
SW> end 				# Exists configuration mode
SW> write 				# Saves configuration	
```

## Virtual Interfaces Router
```sh
R> interface Fx/y			# Selects interface Fx/y
R> no shutdown       			# Enables selected interface
R> interface Fx/y.z 			# Creates sub-interface Fx/y.z
R> encapsulation dot1Q <vlanID>		# Tags the sub-interface for the specified VLAN using dot1Q
R> ip address <addr> <mask> 		# Assigns the addr and mask to the sub-interface
R> end 					# Exit current configuration
```
