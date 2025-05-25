from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.user import User
from app.models.timesheet import Timesheet
from app.services.database import get_user_timesheets
from app.utils.helpers import hash_password

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Handle clock in/out logic here
        user_id = request.form.get('user_id')
        action = request.form.get('action')  # 'clock_in' or 'clock_out'
        # Implement clock in/out functionality
        flash('Ponto registrado com sucesso!', 'success')
        return redirect(url_for('dashboard.dashboard'))

    user_id = request.args.get('user_id')  # Get user ID from query parameters
    timesheets = get_user_timesheets(user_id)  # Fetch user's timesheets
    return render_template('dashboard.html', timesheets=timesheets)