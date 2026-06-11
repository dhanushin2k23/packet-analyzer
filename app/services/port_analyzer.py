from collections import Counter
from scapy.layers.inet import TCP, UDP

PORT_SERVICES = {
    80: "HTTP",
    443: "HTTPS",
    53: "DNS",
    22: "SSH",
    21: "FTP",
    25: "SMTP",
    110: "POP3",
    143: "IMAP"
}


def analyze_ports(packets):

    destination_ports = []

    for packet in packets:

        if packet.haslayer(TCP):
            destination_ports.append(packet[TCP].dport)

        elif packet.haslayer(UDP):
            destination_ports.append(packet[UDP].dport)

    destination_port_counter = Counter(destination_ports)

    top_destination_ports = []

    for port, count in destination_port_counter.most_common(10):

        top_destination_ports.append({
            "port": port,
            "service": PORT_SERVICES.get(port, "Unknown"),
            "count": count
        })

    return {
        "top_destination_ports": top_destination_ports
    }