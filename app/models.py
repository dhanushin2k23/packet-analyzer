#Program used to make database columns.

from app.database import db
from datetime import datetime
from sqlalchemy import JSON
from app.extensions import bcrypt

class AnalysisReport(db.Model):
    id=db.Column(
        db.Integer,
        primary_key = True
    )

    filename = db.Column(
        db.String(100)
    )

    total_packets = db.Column(
        db.Integer
    )

    tcp_packets = db.Column(
        db.Integer
    )

    udp_packets = db.Column(
        db.Integer
    )

    icmp_packets = db.Column(
        db.Integer
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    top_source_ips = db.Column(JSON)

    top_destination_ips = db.Column(JSON)

    top_destination_ports = db.Column(JSON)

    protocol_percentages = db.Column(JSON)

    security_alerts = db.Column(JSON)

class User(db.Model):
    id = db.Column(
        db.Integer,
        primary_key = True
    )

    username=db.Column(
        db.String(100),
        unique=True,
        nullable = False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable = False
    )

    password_hash = db.Column(
        db.String(200),
        nullable = False
    )

    def set_password(self,password):
        self.password_hash = (bcrypt.generate_password_hash(password).decode("utf-8"))

    def check_password(self,password):
        return bcrypt.check_password_hash(
            self.password_hash,
            password
        )
