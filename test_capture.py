from scapy.all import sniff

print("Listening for Flask traffic on port 5000...")

sniff(
    iface=r"\Device\NPF_Loopback",
    filter="tcp port 5000",
    prn=lambda p: p.show(),
    store=False
)