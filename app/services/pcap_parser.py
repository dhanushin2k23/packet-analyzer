from scapy.all import rdpcap

from app.services.protocol_analyzer import analyze_protocols
from app.services.ip_analyzer import analyze_ips
from app.services.port_analyzer import analyze_ports
from app.services.security_analyzer import detect_suspicious_activity


def analyze_pcap(filepath):

    packets = rdpcap(filepath)

    protocol_data = analyze_protocols(packets)
    ip_data = analyze_ips(packets)
    port_data = analyze_ports(packets)
    security_data = detect_suspicious_activity(protocol_data,port_data)


    return {
        **protocol_data,
        **ip_data,
        **port_data,
        **security_data
    }