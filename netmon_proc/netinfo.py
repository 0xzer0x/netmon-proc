from scapy.interfaces import ifaces

MAC_ADDRS: set[str] = {iface.mac for iface in ifaces.values()}
