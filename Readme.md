# TABLE OF CONTENTS



# USEFUL COMMANDS

### ESW3
```sh
SW> show iproute		# Shows the default gateway
SW> show ipif			# Shows the ip address
SW> show fdb			# Shows the switching table
SW> show vlan-switch		# Shows the vlan table
SW> show mac-address-table	# Shows the mac address table
```

### Router
```sh
R > show ip route 		# Show routing table
```

---

# VLAN CONFIGURATION

## Configure ESW VLANs

```sh
vlan database			# Enter VLAN configuration mode
vlan <vlanID>			# Create <vlanID>
exit				# Exit vlan Database
conf t				# Enter configuration mode
interface range F1/y - z	# Selects the range of interfaces for configuration
switchport acess vlan <vlanID>	# Assigns the selected ports to <vlanID>
end				# Exit current configuration
write				# Save running configuration
```

## Virtual Interfaces Router
```sh

```
