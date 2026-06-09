# Packet Analyzer

A Flask-based network packet analyzer that processes PCAP files and extracts meaningful traffic insights such as protocol statistics, IP analysis, and port analysis.

## Features

* Upload and analyze `.pcap` files
* TCP packet count
* UDP packet count
* ICMP packet count
* Top Source IP addresses
* Top Destination IP addresses
* Top Destination Ports
* Service name mapping (HTTP, HTTPS, DNS, SSH, etc.)
* REST API built with Flask
* Scapy-based packet parsing

---

## Tech Stack

### Backend

* Python 3
* Flask

### Packet Analysis

* Scapy

### Development Tools

* Git
* GitHub
* Postman

---

## Project Structure

```text
packet_analyzer/
│
├── app/
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       └── pcap_parser.py
│
├── uploads/
│
├── requirements.txt
├── run.py
├── .gitignore
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/dhanushin2k23/packet-analyzer.git
cd packet-analyzer
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
python run.py
```

Server will start at:

```text
http://127.0.0.1:5000
```

---

## API Endpoint

### Upload PCAP File

**Endpoint**

```http
POST /upload
```

**Request Type**

```text
multipart/form-data
```

**Form Data**

| Key  | Type |
| ---- | ---- |
| file | File |

---

## Example Response

```json
{
  "tcp_packets": 73,
  "udp_packets": 4,
  "icmp_packets": 0,
  "top_source_ips": [
    ["192.168.1.100", 56]
  ],
  "top_destination_ips": [
    ["172.217.0.100", 5]
  ],
  "top_destination_ports": [
    {
      "port": 443,
      "service": "HTTPS",
      "count": 53
    }
  ]
}
```

---

## Current Capabilities

* Protocol Distribution Analysis
* Source IP Analysis
* Destination IP Analysis
* Destination Port Analysis
* Service Identification

---

## Future Enhancements

* Source Port Analysis
* Protocol Percentage Analysis
* Packet Timeline Visualization
* Suspicious Traffic Detection
* DNS Traffic Analysis
* GeoIP Tracking
* Dashboard Frontend
* Authentication & User Management
* Report Export (PDF/CSV)

---

## Testing

The API can be tested using:

* Postman
* Thunder Client
* cURL

Example:

```bash
curl -X POST http://127.0.0.1:5000/upload \
-F "file=@sample.pcap"
```

---

## Author

Dhanush

GitHub: https://github.com/dhanushin2k23

---

## License

This project is developed for educational and learning purposes.
