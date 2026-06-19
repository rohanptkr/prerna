from datetime import date
from flask import Blueprint, render_template
from flask_login import current_user, login_required

from application import db
from models import Booking, Member, Payment, Seat, User

main_bp = Blueprint("main", __name__, template_folder="../templates")


def calculate_metrics():
    total_members = Member.query.count()
    active_members = Member.query.filter_by(membership_status="Active").count()
    expired_members = Member.query.filter_by(membership_status="Expired").count()
    total_seats = Seat.query.count()
    occupied_seats = Seat.query.filter_by(status="Occupied").count()
    available_seats = total_seats - occupied_seats
    monthly_revenue = Payment.query.filter(Payment.payment_date >= date(date.today().year, date.today().month, 1)).with_entities(db.func.coalesce(db.func.sum(Payment.amount), 0)).scalar()
    total_revenue = Payment.query.with_entities(db.func.coalesce(db.func.sum(Payment.amount), 0)).scalar()
    return {
        "total_members": total_members,
        "active_members": active_members,
        "expired_members": expired_members,
        "total_seats": total_seats,
        "occupied_seats": occupied_seats,
        "available_seats": available_seats,
        "monthly_revenue": monthly_revenue,
        "total_revenue": total_revenue,
    }


@main_bp.route("/")
@login_required
def index():
    metrics = calculate_metrics()
    if current_user.role.role_name == "Admin":
        return render_template("dashboard/admin_dashboard.html", metrics=metrics)
    return render_template("dashboard/member_dashboard.html", metrics=metrics)
