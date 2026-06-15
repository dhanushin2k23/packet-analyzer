from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from app.database import db
from app.models import AnalysisReport
from app.services.pcap_parser import analyze_pcap

from app.auth.routes import auth

from app.extensions import jwt, bcrypt

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


def create_app():

    app = Flask(__name__)
    CORS(app)

    # JWT config
    app.config["JWT_SECRET_KEY"] = "packet-analyzer-secret-key"


    # Database config
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:BASKETBALL#23@localhost/packet_analyzer"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    # Initialize extensions
    db.init_app(app)

    bcrypt.init_app(app)

    jwt.init_app(app)


    # Register blueprints
    app.register_blueprint(auth)



    with app.app_context():
        db.create_all()



    @app.route("/upload", methods=["POST"])
    @jwt_required()
    def upload():


        current_user = get_jwt_identity()


        file = request.files.get("file")


        if file is None or file.filename == "":
            return jsonify({
                "error": "No file selected"
            }),400



        if not file.filename.endswith(".pcap"):
            return jsonify({
                "error": "Only PCAP files allowed"
            }),400



        os.makedirs(
            "uploads",
            exist_ok=True
        )


        filepath = os.path.join(
            "uploads",
            file.filename
        )


        file.save(filepath)



        try:

            result = analyze_pcap(filepath)


        except Exception as e:

            return jsonify({
                "error": "Failed to analyze file",
                "details": str(e)
            }),500




        report = AnalysisReport(

            filename=file.filename,

            total_packets=result["total_packets"],

            tcp_packets=result["tcp_packets"],

            udp_packets=result["udp_packets"],

            icmp_packets=result["icmp_packets"],

            protocol_percentages=result["protocol_percentages"],

            top_source_ips=result["top_source_ips"],

            top_destination_ips=result["top_destination_ips"],

            top_destination_ports=result["top_destination_ports"],

            security_alerts=result["security_alerts"]

        )


        db.session.add(report)

        db.session.commit()



        result["uploaded_by"] = current_user



        return jsonify({

            "report_id": report.id,

            **result

        })





    @app.route("/reports", methods=["GET"])
    @jwt_required()
    def get_reports():


        reports = AnalysisReport.query.all()


        data = []


        for report in reports:


            data.append({

                "id": report.id,

                "filename": report.filename,

                "total_packets": report.total_packets,

                "tcp_packets": report.tcp_packets,

                "udp_packets": report.udp_packets,

                "icmp_packets": report.icmp_packets,

                "created_at": report.created_at

            })


        return jsonify(data)





    @app.route(
        "/reports/<int:report_id>",
        methods=["GET"]
    )
    @jwt_required()
    def get_report(report_id):


        report = AnalysisReport.query.get(report_id)



        if report is None:

            return jsonify({
                "error":"Report not found"
            }),404




        return jsonify({


            "id": report.id,

            "filename": report.filename,

            "total_packets": report.total_packets,

            "tcp_packets": report.tcp_packets,

            "udp_packets": report.udp_packets,

            "icmp_packets": report.icmp_packets,

            "top_source_ips": report.top_source_ips,

            "top_destination_ips": report.top_destination_ips,

            "top_destination_ports": report.top_destination_ports,

            "protocol_percentages": report.protocol_percentages,

            "security_alerts": report.security_alerts,

            "created_at": report.created_at

        })



    return app