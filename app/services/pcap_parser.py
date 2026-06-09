from scapy.all import rdpcap
from scapy.layers.inet import IP, TCP, UDP, ICMP
from collections import Counter

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

def analyze_pcap(filepath):

    packets = rdpcap(filepath)

    tcp_count = 0
    udp_count = 0
    icmp_count = 0

    source_ips = []
    destination_ips = []
    destination_ports =[]

    for packet in packets:

        if packet.haslayer(TCP):
            tcp_count += 1
            destination_ports.append(packet[TCP].dport)

        elif packet.haslayer(UDP):
            udp_count += 1
            destination_ports.append(packet[UDP].dport)

        elif packet.haslayer(ICMP):
            icmp_count += 1

        if packet.haslayer(IP):
            source_ips.append(packet[IP].src)
            destination_ips.append(packet[IP].dst)

    ip_counter = Counter(source_ips)
    destination_counter = Counter(destination_ips)
    destination_port_counter = Counter(destination_ports)

    top_destination_ports = []

    for port, count in destination_port_counter.most_common(10):
        top_destination_ports.append({
            "port": port,
            "service": PORT_SERVICES.get(port, "Unknown"),
            "count": count
        })

    total_packets = tcp_count + udp_count + icmp_count
    protocol_percentages = {
        "tcp": round((tcp_count / total_packets) * 100, 2) if total_packets else 0,
        "udp": round((udp_count / total_packets) * 100, 2) if total_packets else 0,
        "icmp": round((icmp_count / total_packets) * 100, 2) if total_packets else 0
    }

    return {
        "tcp_packets": tcp_count,
        "udp_packets": udp_count,
        "icmp_packets": icmp_count,
        "top_source_ips": ip_counter.most_common(5),
        "top_destination_ips": destination_counter.most_common(5),
        "top_destination_ports": top_destination_ports,
        "protocol_percentages":protocol_percentages
    }