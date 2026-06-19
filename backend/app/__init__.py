import os
import uuid
from datetime import timedelta
from pathlib import Path

from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from app.database import db
from app.models import AnalysisReport
from app.services.pcap_parser import analyze_pcap
from app.auth.routes import auth
from app.extensions import jwt, bcrypt


from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


ALLOWED_EXTENSIONS = {".pcap", ".pcapng"}
DEFAULT_MAX_UPLOAD_MB = 25


def _csv_env(name, default=""):
    return [
        item.strip()
        for item in os.getenv(name, default).split(",")
        if item.strip()
    ]


def _required_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} environment variable is required")
    return value


def _is_allowed_capture(filename):
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def _current_user_id():
    return int(get_jwt_identity())


def create_app():

    load_dotenv()
    app = Flask(__name__)

    is_production = os.getenv("FLASK_ENV") == "production"

    if is_production:
        secret_key = _required_env("SECRET_KEY")
        jwt_secret_key = _required_env("JWT_SECRET_KEY")
        database_url = _required_env("DATABASE_URL")
        default_cors_origins = ""
        _required_env("CORS_ORIGINS")
    else:
        secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
        jwt_secret_key = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-me")
        database_url = os.getenv("DATABASE_URL", "sqlite:///packet_analyzer.db")
        default_cors_origins = "http://localhost:5173,http://127.0.0.1:5173"

    cors_origins = _csv_env(
        "CORS_ORIGINS",
        default_cors_origins
    )
    if not cors_origins:
        raise RuntimeError("CORS_ORIGINS must include at least one origin")

    CORS(
        app,
        origins=cors_origins,
        supports_credentials=False
    )


    # =====================
    # JWT CONFIG
    # =====================
    app.config["SECRET_KEY"] = secret_key

    app.config["JWT_SECRET_KEY"] = jwt_secret_key

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        hours=2
    )

    app.config["MAX_CONTENT_LENGTH"] = int(
        os.getenv("MAX_UPLOAD_MB", DEFAULT_MAX_UPLOAD_MB)
    ) * 1024 * 1024


    # =====================
    # DATABASE CONFIG
    # =====================

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url

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



    # Create tables for the current lightweight deployment setup.
    with app.app_context():
        db.create_all()

    @app.errorhandler(RequestEntityTooLarge)
    def handle_large_upload(_error):
        return jsonify({
            "error": "Uploaded file is too large"
        }), 413

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok"
        })



    # =====================
    # UPLOAD PCAP
    # =====================

    @app.route("/upload", methods=["POST"])
    @jwt_required()
    def upload():

        current_user = _current_user_id()


        file = request.files.get("file")


        if file is None or file.filename == "":
            return jsonify({
                "error": "No file selected"
            }), 400



        if not _is_allowed_capture(file.filename):
            return jsonify({
                "error": "Only PCAP or PCAPNG files allowed"
            }), 400

        upload_folder = Path(os.getenv(
            "UPLOAD_FOLDER",
            "uploads"
        ))

        upload_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        original_filename = secure_filename(file.filename)
        if not original_filename:
            return jsonify({
                "error": "Invalid file name"
            }), 400

        unique_name = f"{uuid.uuid4()}_{original_filename}"

        filepath = upload_folder / unique_name

        file.save(filepath)



        try:

            result = analyze_pcap(str(filepath))


        except Exception as e:

            app.logger.exception("PCAP analysis failed")

            response = {
                "error": "Failed to analyze file",
            }
            if not is_production:
                response["details"] = str(e)

            return jsonify(response), 500

        finally:
            filepath.unlink(missing_ok=True)




        report = AnalysisReport(

            filename=original_filename,

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



        try:

            db.session.add(report)

            db.session.commit()

        except Exception as e:

            db.session.rollback()

            app.logger.exception("Failed to save analysis report")

            response = {
                "error": "Failed to save analysis report"
            }
            if not is_production:
                response["details"] = str(e)

            return jsonify(response), 500



        result["uploaded_by"] = current_user



        return jsonify({
            "id": report.id,
            "filename": original_filename,
            **result
        })




    # =====================
    # GET ALL REPORTS
    # =====================

    @app.route("/reports", methods=["GET"])
    @jwt_required()
    def get_reports():


        current_user = _current_user_id()



        reports = AnalysisReport.query.filter_by(
            user_id=current_user
        ).order_by(
            AnalysisReport.created_at.desc()
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

                "created_at": report.created_at,

                "security_alerts": report.security_alerts

            })



        return jsonify(data)





    # =====================
    # GET SINGLE REPORT
    # =====================

    @app.route("/reports/<int:report_id>", methods=["GET"])
    @jwt_required()
    def get_report(report_id):


        current_user = _current_user_id()



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
