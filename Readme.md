# TABLE OF CONTENTS
1. **[Useful Commands](#useful-commands)**
   - [ESW3](#esw3)
   - [Router](#router)
   - [VPC](#vpc)
2. **[VLAN Configuration](#vlan-config)**
   - [Configure ESW VLANs](#esw-vlans)
   - [Set Switch Port to Trunk](#trunk)
   - [Configure IP to VLAN](#ip-to-vlan)
   - [Virtual Interfaces Router](#virtual-interfaces-router)
3. **[NAT/PAT Configuration](#natpat-config)**
4. **[DHCP Configuration](#dhcp)**
5. **[IPv6 Configuration](#ipv6)**

# USEFUL COMMANDS <a name="useful-commands"></a>
**The order of most commands is relevant!**

## ESW3 <a name="esw3"></a>
```sh
SW> show iproute					# Shows the default gateway
SW> show ipif						# Shows the ip address
SW> show vlan-switch					# Shows the vlan table
SW> show mac-address-table				# Shows the mac address table
```
ESW L3 Switch-Routers general mandatory commands:
```sh
SW> ip routing						# Allows switch to perform L3 functions
SW> ip subnet-zero 					# Allows the use of subnet zero
SW> ipv6 unicast-routing 				# Enables IPv6 Routing on the switch 
```

## Router <a name="router"></a>
```sh
R> show ip route 					# Show routing table
R(config)> service dhcp 				# Enables the DHCP service
R(config)> ip route <network> <mask> <gateway>		# Creates an ip route to  <network>
							# with such <mask> through <gateway>

### NAT/PAT ###
R> show ip nat translations 				# Shows the NAT Table
R> show ip nat statistics  				# Shows the NAT statistics

### IPv6 ###
R> show ipv6 interface 					# Detailed IPv6 configuration information for all interfaces
R> show ipv6 interface brief 				# Summary of IPv6 interface information
```


## VPC <a name="vpc"></a>
```sh 
VPC> ip dhcp 						# Acquire IPv4 Address dynamically
VPC> ip dhcp -r 					# Renew the IPv4 Address Dynamically
VPC> ip dhcp -x 					# Release the IPv4 Address Dynamically
```

---

<div style="page-break-after: always;"></div>


# VLAN CONFIGURATION <a name="vlan-config"></a>

## Configure ESW VLANs <a name="esw-vlans"/></a>

```sh
ESW> vlan database					# Enter VLAN configuration mode
ESW> vlan <vlanID>					# Create <vlanID>
ESW> exit						# Exit vlan Database
ESW> conf t						# Enter configuration mode
ESW> interface range F1/y - z				# Selects the range of interfaces for configuration
ESW> switchport acess vlan <vlanID>			# Assigns the selected ports to <vlanID>
ESW> end						# Exit current configuration
ESW> write						# Save running configuration
```

## Set Switch port to trunk <a name="trunk"/></a>
Configures the interface as a trunk port to carry traffic for multiple VLANs using 802.1Q encapsulation
```sh
ESW> interface Fx/y 					# Selects the interface
ESW> switchport mode trunk 				# Sets the selected port to trunk
```

## Configure IP to VLAN <a name="ip-to-vlan"/></a>
```sh
ESW> conf t						# Enter configuration mode
ESW> interface vlan <vlanID> 				# Select VLAN <ID> interface for configuration
ESW> ip address <addr> <mask> 				# Assigns IP addr and subnet mask to VLAN <ID>
ESW> no shutdown 					# Enables VLAN interface
ESW> end 						# Exists configuration mode
ESW> write 						# Saves configuration	
```

## Virtual Interfaces Router <a name="virtual-interfaces-router"/></a>
```sh
R> interface Fx/y					# Selects interface Fx/y
R> no shutdown       					# Enables selected interface
R> interface Fx/y.z 					# Creates sub-interface Fx/y.z
R> encapsulation dot1Q <vlanID>				# Tags the sub-interface for the specified VLAN using dot1Q
R> ip address <addr> <mask> 				# Assigns the addr and mask to the sub-interface
R> end 							# Exit current configuration
```


## DHCP<a name="dhcp"/></a>
```sh
R(config)> service dhcp 				# Enables DHCP service
R(config)> ip dhcp pool <x> 				# Creates DHCP Pool number <x>
R(dhcp-config)> network <addr> <mask>			# Mask and Subnet Mask linked to the DHCP Pool
R(dhcp-config)> default-router <addr> 			# Gateway
R(config)> ip dhcp excluded address <addr> <addr> 	# Interval of excluded addresses from the DHCP scope (x to y)
```
---
#IPv6 	<a name="ipv6"></a>

```sh
R(config)> ipv6 unicast-routing 			# Enables IPv6 routing on the router
R(config)> interface <int> 				# Selects the interface to be configured
R(config-if)> ipv6 enable				# Enables IPv6 on the selected interface
R(config-if)> no shutdown 				# Activates the interface

### Adding Specific IPv6 Addresses ###
R(config)> interface <int> 				# Selects the interface to be configured
R(config-if)> ipv6 address 2001:A:1:1::100/64 		# Assigns IPv6 addr to selected interface
R(config-if)> no shutdown 				# Activates the interface

### Configuring an Address using EUI-64 ###
R(config)> interface <int> 				# Selects the interface to be configured
R(config-if)> ipv6 address 2001:A:1:2::/64 eui-64	# Configures an IPv6 Address for the interface using EUI-64
R(config-if)> no shutdown 				# Activates the interface

###Verification Commands###
R> show ipv6 interface 					# Detailed IPv6 configuration information for all interfaces
R> show ipv6 interface brief 				# Summary of IPv6 interface information

```
