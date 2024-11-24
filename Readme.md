# TABLE OF CONTENTS
1. **[Useful Commands](#useful-commands)**
   - [VPC](#vpc)
   - [Router](#router)
   - [ESW3](#esw3)
2. **[VLAN Configuration](#vlan-config)**
   - [Configure ESW VLANs](#esw-vlans)
   - [Set Port to Trunk](#trunk)
   - [Configure IP to VLAN](#ip-to-vlan)
   - [Virtual Interfaces](#virtual-interfaces)
3. **[NAT/PAT Configuration](#natpat-config)**
   - [Dynamic NAT/PAT](#dynamic-natpat)
   - [Static NAT/PAT](#static-natpat)
4. **[DHCP Configuration](#dhcp)**
5. **[IPv6 Configuration](#ipv6)**


# USEFUL COMMANDS <a name="useful-commands"></a>
**The order of most commands is relevant!**

To "undo" a command, or to simply delete something just attach the `no` prefix
```sh
R(config-if)> no ipv6 address 2001:A:1:1::100/64 	# Undo's the assignment of IPv6 addr
```

## VPC <a name="vpc"></a>
```sh
##### VPC Commands #####
VPC> show 						# Shows VPC Interface details
VPC> show ip						# Shows Address/MAC/Gateway/DNS ...
VPC> ip <addr> <mask> <gateway>				# Configures VPC to <addr> <mask> <gateway>

### DHCP ###
VPC> ip dhcp 						# Acquire IPv4 Address dynamically
VPC> ip dhcp -r 					# Renew the IPv4 Address Dynamically
VPC> ip dhcp -x 					# Release the IPv4 Address Dynamically
```

## Router <a name="router"></a>
```sh
##### Router Commands #####
R> show ip route 					# Show routing table
R> show interfaces 					# Details of each interface
R(config)> ip route <network> <mask> <gateway>		# Creates an ip route to  <network>
							# with such <mask> through <gateway>

### NAT/PAT ###
R> show ip nat translations 				# Shows the NAT Table
R> show ip nat statistics  				# Shows the NAT statistics

### IPv6 ###
R> show ipv6 route 
R> show ipv6 interface 					# Detailed IPv6 configuration information for all interfaces
R> show ipv6 interface brief 				# Summary of IPv6 interface information
R> ipv6 route <network>/<mask> <gateway> 		# Creates an ip route to  <network>
							# with such <mask> through <gateway>

### General Mandatory Commands ###
R(config)> service dhcp					# Enables DHCP
R(config)> ip subnet zero				# Allows the use of subnet 0
R(config)> ipv6 unicast-routing				# Enables IPv6 Routing

```

## ESW <a name="esw3"></a>

```sh
##### Switch Layer 3 Commands #####
SW> show run						# Shows configuration file
SW> show ip route					# Shows the IPv4 routing table
SW> show ipv6 route 					# Shows the IPv6 routing Table
SW> show vlan-switch					# Shows the vlan table
SW> show mac-address-table				# Shows the mac address table
SW(config)> ip route <network> <mask> <gateway>		# Creates an ip route to  <network>
							# with such <mask> through <gateway>
SW(config)> ipv6 route <network>/<mask> <gateway> 	# Creates an ip route to  <network>
							# with such <mask> through <gateway>

### Configure interface/vlan with more than 2 Addrs ###
SW> conf t
SW(config)> int <interface>
SW(config-if)> ip address <addr> <mask>
SW(config-if)> ip adddress <addr> <mask> secondary

### General Mandatory Commands ###
SW(config)> ip routing					# Allows switch to perform L3 functions
SW(config)> service dhcp				# Enables DHCP
SW(config)> ip subnet-zero 				# Allows the use of subnet zero
SW(config)> ipv6 unicast-routing 			# Enables IPv6 Routing 
```
---

<div style="page-break-after: always;"></div>

# VLAN CONFIGURATION <a name="vlan-config"></a>
## Configure VLANs <a name="esw-vlans"/></a>
```sh
ESW> vlan database					# Enter VLAN configuration mode
ESW> vlan <vlanID>					# Create <vlanID>
ESW> exit						# Exit vlan Database

ESW(config)> ip routing					# Enable IP Routing
ESW> interface range Fx/y - z				# Selects the range of interfaces for configuration
# Choose one, either ↓ or ↑
ESW> interface Fx/y					# Selects the interface
ESW> switchport mode access				# Putting ports into access mode
ESW> switchport acess vlan <vlanID>			# Assigns the selected ports to <vlanID>
ESW> end						# Exit current configuration
ESW> write						# Save running configuration
```

## Set  port to trunk <a name="trunk"/></a>
Configures the interface as a trunk port to carry traffic for multiple VLANs using 802.1Q encapsulation

**Importante Note:**
- Ports on acess mode can only belong to one specific VLAN and the incoming and outgoing Ethernet
frames **DO NOT** have **VLAN TAG**
- Ports on trunk mode may input and output Ethernet Frames from different VLANs and those ethernet frames
**SHOULD BE TAGGED**, as such:
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

## Virtual Interfaces <a name="virtual-interfaces"/></a>
Configure sub-interface to send and received tagged frames (`encapsulation dot1Q <vlanid>`) 

It's possible to add more sub-interfaces to the same physical interface (e.g `F1/0.3`, `F1/0.450`). The ID
of the interface (`0.3`, `0.450`) **doesn't** need to match the `<vlanID>`.
```sh
R(config)> interface Fx/y				# Selects interface Fx/y
R(config)> no shutdown       				# Enables selected interface
R(config)> interface Fx/y.z 				# Creates sub-interface Fx/y.z
R(config-subif)> no shutdown 				# Enables selected interface
R(config-subif)> encapsulation dot1Q <vlanID>		# Tags the sub-interface for the specified VLAN using dot1Q
R(config-subif)> ip address <addr> <mask> 		# Assigns the addr and mask to the sub-interface
R> end 							# Exit current configuration
```
---
# NAT/PAT Configuration<a name="natpat-config"/></a>

## Dynamic NAT/PAT <a name="dynamic-natpat"/></a>
To define a pool of addresses to be allocated by dynamic NAT process:
```sh
R(config)> ip nat pool <poolName> <start-IP> <end-IP> netmask <subnet-mask>
```

Creates an acess list to specify which IP addresses are eligible for NAT Translation:
- `<listnum>` number of the list
- `<addr>` network address to be eligible for NAT Translation
- `<wildcard-mask>` host bits (e.g `0.0.0.255`)
```sh
R(config)> access-list <listNum> permit <addr> <wildcard-mask>
```

Establish the dynamic source translation, link the acess list `<listNum>` to the name of the NAT Pool `<poolName>`:
- Add the option `overload` to enable PAT (NAT Overload)
```sh
R(config)> ip nat inside source list <listNum> pool <poolName> (overload)
```

```sh
R(config)> int fx/y					# Router Interface on the private network
R(config-if)> ip nat inside 				# Specifies interface to  be used by inside network hosts

R(config)> int fx/y					# Router Interface on the public network
R(config-if)> ip nat outsidem 				# Specifies interface to  be used by outside
```
```sh
R> show ip nat translations 				# Shows the NAT Table
R> show ip nat statistics  				# Shows the NAT statistics
R> clear ip nat translation *				# Clear NAT Translation Table
R> ip nat translation timeout x 			# Change NAT timeout to x seconds 
```

## Static NAT/PAT<a name="static-natpat"/></a>
Static translation 
```sh
R(config)> ip nat inside source static <private addr> <public addr>
```
---

# DHCP<a name="dhcp"/></a>
To verify the configuration and status of the DHCP Server
```sh
show ip dhcp pool 					# Returns the configured DHCP Pools
show ip dhcp server statistics 				# Statics of the DHCP Server (Num of address pools; 
							# Num of DHCP Discovers; Offer;	Request; Acknowlodge etc)
show ip dhcp binding 					# Addresses given to the different hardware
```
Configure the DHCP Server
```sh
R(config)> service dhcp 				# Enables DHCP service
R(config)> ip dhcp excluded address <addr> <addr> 	# Interval of excluded addresses from the DHCP scope (x to y)
R(config)> ip dhcp pool <x> 				# Creates DHCP Pool number <x>
R(dhcp-config)> network <addr> <mask>			# Mask and Subnet Mask linked to the DHCP Pool
R(dhcp-config)> default-router <addr> 			# Gateway
```
---
# IPv6 	<a name="ipv6"></a>

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

### Verification Commands ###
R> show ipv6 interface 					# Detailed IPv6 configuration information for all interfaces
R> show ipv6 interface brief 				# Summary of IPv6 interface information

```
