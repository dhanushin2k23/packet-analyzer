# Packet Analyzer

A full-stack network packet analysis tool. Upload a `.pcap` file and get back protocol breakdowns, top talkers, port/service mapping, and basic security alerts — behind a JWT-authenticated Flask API with a React dashboard on top.

## Features

- User authentication (register/login) with JWT
- Upload and parse `.pcap` files using Scapy
- Protocol breakdown — TCP / UDP / ICMP counts and percentages
- Top 5 source IPs and top 5 destination IPs
- Top 10 destination ports mapped to known services (HTTP, HTTPS, DNS, SSH, FTP, SMTP, POP3, IMAP)
- Basic security alerts (high TCP volume, possible ICMP flood, unusually wide port spread)
- Per-user analysis history stored in PostgreSQL
- React + Tailwind dashboard with charts (Recharts)

## Tech Stack

**Backend:** Python, Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-Bcrypt, Scapy, PostgreSQL

**Frontend:** React 19, Vite, Tailwind CSS, Axios, Recharts, React Router

## Project Structure

```text
packet_analyzer/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # app factory, config, /upload route
│   │   ├── database.py          # SQLAlchemy instance
│   │   ├── extensions.py        # bcrypt, jwt instances
│   │   ├── models.py            # User, AnalysisReport
│   │   ├── auth/
│   │   │   └── routes.py        # /register, /login
│   │   └── services/
│   │       ├── pcap_parser.py       # orchestrates analysis
│   │       ├── protocol_analyzer.py
│   │       ├── ip_analyzer.py
│   │       ├── port_analyzer.py
│   │       └── security_analyzer.py
│   ├── uploads/                 # uploaded pcap files (gitignored)
│   ├── requirements.txt
│   └── run.py
└── frontend/
    ├── src/
    │   ├── pages/                # Login, Register, Upload, Dashboard, Report, Security
    │   ├── components/           # Navbar, Sidebar, UploadBox, StatCard, AlertCard
    │   └── api/axios.js
    ├── package.json
    └── vite.config.js
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL running locally (or a connection string to one)

## Setup

### 1. Clone

```bash
git clone https://github.com/dhanushin2k23/packet-analyzer.git
cd packet-analyzer
```

### 2. Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

Create `backend/.env`:

```env
SECRET_KEY=replace-with-a-random-secret
JWT_SECRET_KEY=replace-with-a-random-secret
DATABASE_URL=postgresql://username:password@localhost:5432/packet_analyzer
UPLOAD_FOLDER=uploads
```

Run the server:

```bash
python run.py
```

API runs at `http://127.0.0.1:5000`. Tables are created automatically on first run via `db.create_all()`.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:5173`.

## API Reference

### `POST /register`

```json
{
  "username": "example",
  "email": "example@example.com",
  "password": "yourpassword"
}
```

Returns `201` on success, `409` if the email is already registered.

### `POST /login`

```json
{
  "email": "example@example.com",
  "password": "yourpassword"
}
```

Returns:

```json
{ "access_token": "<JWT>" }
```

### `POST /upload`

Requires `Authorization: Bearer <access_token>`. `multipart/form-data` with a `file` field (`.pcap` only).

```http
POST /upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <your-file>.pcap
```

**Example response:**

```json
{
  "total_packets": 77,
  "tcp_packets": 73,
  "udp_packets": 4,
  "icmp_packets": 0,
  "protocol_percentages": {
    "tcp": 94.81,
    "udp": 5.19,
    "icmp": 0
  },
  "top_source_ips": [["192.168.1.100", 56]],
  "top_destination_ips": [["172.217.0.100", 5]],
  "top_destination_ports": [
    { "port": 443, "service": "HTTPS", "count": 40 }
  ],
  "security_alerts": []
}
```

## Known Limitations

- `requirements.txt` was exported from a full Anaconda environment and includes unrelated packages with local file paths — it needs to be trimmed to actual project dependencies before this can be deployed to a fresh environment (see "Deploying" below).
- Uploaded files are written to local disk (`UPLOAD_FOLDER`), which doesn't persist across restarts/redeploys on most cloud platforms.
- No file size limit currently enforced on uploads.

## Deploying

Before deploying to Render/Railway/any fresh Linux environment:

1. Regenerate `requirements.txt` with only the packages this project actually imports (Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-Bcrypt, Flask-CORS, scapy, python-dotenv, psycopg2-binary, gunicorn).
2. Set `SECRET_KEY`, `JWT_SECRET_KEY`, and `DATABASE_URL` as environment variables on the host — don't commit `.env`.
3. Use a managed Postgres add-on rather than local Postgres.
4. Either move file uploads to object storage (S3/Supabase/Cloudinary) or accept that uploaded files won't survive a redeploy.

## License

MIT License

Copyright (c) 2026 Dhanush

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
