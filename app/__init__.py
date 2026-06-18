from flask import Flask, request, jsonify
import os
import uuid
from datetime import timedelta
from dotenv import load_dotenv
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
    load_dotenv()
    CORS(
        app,
        origins=[
            "http://localhost:5173"
        ]
    )


    # =====================
    # JWT CONFIG
    # =====================
    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY"
    )

    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY"
    )

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        hours=2
    )


    # =====================
    # DATABASE CONFIG
    # =====================

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



    # =====================
    # INIT EXTENSIONS
    # =====================

    db.init_app(app)

    bcrypt.init_app(app)

    jwt.init_app(app)



    # =====================
    # BLUEPRINTS
    # =====================

    app.register_blueprint(auth)



    # Create tables
    with app.app_context():
        db.create_all()



    # =====================
    # UPLOAD PCAP
    # =====================

    @app.route("/upload", methods=["POST"])
    @jwt_required()
    def upload():

        current_user = get_jwt_identity()


        file = request.files.get("file")


        if file is None or file.filename == "":
            return jsonify({
                "error": "No file selected"
            }), 400



        if not file.filename.endswith(".pcap"):
            return jsonify({
                "error": "Only PCAP files allowed"
            }), 400



        UPLOAD_FOLDER = os.getenv(
            "UPLOAD_FOLDER",
            "uploads"
        )

        os.makedirs(
            UPLOAD_FOLDER,
            exist_ok=True
        )

        unique_name = f"{uuid.uuid4()}_{file.filename}"

        filepath = os.path.join(
            UPLOAD_FOLDER,
            unique_name
        )


        file.save(filepath)



        try:

            result = analyze_pcap(filepath)


        except Exception as e:

            return jsonify({
                "error": "Failed to analyze file",
                "details": str(e)
            }), 500




        report = AnalysisReport(

            filename=file.filename,

            user_id=current_user,

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




    # =====================
    # GET ALL REPORTS
    # =====================

    @app.route("/reports", methods=["GET"])
    @jwt_required()
    def get_reports():


        current_user = get_jwt_identity()



        reports = AnalysisReport.query.filter_by(
            user_id=current_user
        ).all()



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





    # =====================
    # GET SINGLE REPORT
    # =====================

    @app.route("/reports/<int:report_id>", methods=["GET"])
    @jwt_required()
    def get_report(report_id):


        current_user = get_jwt_identity()



        report = AnalysisReport.query.filter_by(

            id=report_id,

            user_id=current_user

        ).first()



        if report is None:

            return jsonify({
                "error": "Report not found"
            }), 404




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