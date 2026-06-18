#This program works for the security check. Checks counts and return statement accordingly.

def detect_suspicious_activity(protocol_data,port_data):

    alerts = []


    if len(port_data["top_destination_ports"]) >= 8:
        alerts.append("Large number of destination ports detected")

    if protocol_data["tcp_packets"] > 1000:
        alerts.append("High TCP traffic detected")

    if protocol_data["icmp_packets"] > 100:
        alerts.append("Possible ICMP flood detected")

    return {
        "security_alerts": alerts
    }