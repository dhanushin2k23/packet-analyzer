from flask import Flask, request, jsonify
import os
from app.database import db
from app.models import AnalysisReport
from app.services.pcap_parser import analyze_pcap


def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:BASKETBALL#23@localhost/packet_analyzer"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/upload", methods=["POST"])
    def upload():

        file = request.files.get("file")

        if file is None or file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        os.makedirs("uploads", exist_ok=True)

        filepath = os.path.join(
            "uploads",
            file.filename
        )

        file.save(filepath)

        result = analyze_pcap(filepath)

        report = AnalysisReport(
            filename=file.filename,
            total_packets=result["total_packets"],
            tcp_packets=result["tcp_packets"],
            udp_packets=result["udp_packets"],
            icmp_packets=result["icmp_packets"],
            top_source_ips=result["top_source_ips"],
            top_destination_ips=result["top_destination_ips"],
            top_destination_ports=result["top_destination_ports"],
            protocol_percentages=result["protocol_percentages"],
            security_alerts=result["security_alerts"]
        )       

        db.session.add(report)
        db.session.commit()

        return jsonify(result)

    return app