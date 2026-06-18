#It counts the total number of TCP,UDP,ICMP and total percentages of these.

from scapy.layers.inet import TCP, UDP, ICMP

def analyze_protocols(packets):

    tcp_count = 0
    udp_count = 0
    icmp_count = 0

    for packet in packets:

        if packet.haslayer(TCP):
            tcp_count += 1

        elif packet.haslayer(UDP):
            udp_count += 1

        elif packet.haslayer(ICMP):
            icmp_count += 1

    total_packets = tcp_count + udp_count + icmp_count
    protocol_percentages = {
        "tcp": round((tcp_count / total_packets) * 100, 2) if total_packets else 0,
        "udp": round((udp_count / total_packets) * 100, 2) if total_packets else 0,
        "icmp": round((icmp_count / total_packets) * 100, 2) if total_packets else 0
    }

    return {
        "total_packets": total_packets,
        "tcp_packets": tcp_count,
        "udp_packets": udp_count,
        "icmp_packets": icmp_count,
        "protocol_percentages": protocol_percentages
    }