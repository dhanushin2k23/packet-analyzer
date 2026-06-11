from collections import Counter
from scapy.layers.inet import IP


def analyze_ips(packets):

    source_ips = []
    destination_ips = []

    for packet in packets:

        if packet.haslayer(IP):
            source_ips.append(packet[IP].src)
            destination_ips.append(packet[IP].dst)

    source_ip_counter = Counter(source_ips)
    destination_ip_counter = Counter(destination_ips)

    return {
        "top_source_ips": source_ip_counter.most_common(5),
        "top_destination_ips": destination_ip_counter.most_common(5)
    }