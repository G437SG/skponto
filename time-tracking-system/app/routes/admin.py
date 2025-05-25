from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from app.models.user import User
from app.models.timesheet import TimeEntry, DailyReport
from app.services.notifications import NotificationService
from app.utils.file_utils import upload_report_file
from datetime import datetime, timedelta
import csv
from io import StringIO, BytesIO

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session or session.get('user_type') != 'ADMINISTRADOR':
            flash('Acesso negado!', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@bp.route('/dashboard')
@admin_required
def dashboard():
    # Get all users
    users = User.get_all_users()
    
    # Get today's entries
    today = datetime.now().date()
    entries = TimeEntry.get_all_entries(today, today)
    
    # Statistics
    total_users = len(users)
    active_today = len(set(entry.user_email for entry in entries))
    
    # Users by type
    user_types = {}
    for user in users:
        user_types[user.user_type] = user_types.get(user.user_type, 0) + 1
    
    return render_template('admin/dashboard.html', 
                         users=users, 
                         entries=entries,
                         total_users=total_users,
                         active_today=active_today,
                         user_types=user_types)

@bp.route('/users')
@admin_required
def users():
    all_users = User.get_all_users()
    return render_template('admin/users.html', users=all_users)

@bp.route('/reports')
@admin_required
def reports():
    # Get date range from query params
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    user_email = request.args.get('user_email')
    
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        # Default to current month
        today = datetime.now().date()
        start_date = today.replace(day=1)
        end_date = today
    
    # Get entries
    if user_email:
        entries = TimeEntry.get_user_entries(user_email, start_date, end_date)
    else:
        entries = TimeEntry.get_all_entries(start_date, end_date)
    
    # Get all users for filter
    users = User.get_all_users()
    
    # Group entries by user and date
    user_reports = {}
    for entry in entries:
        if entry.user_email not in user_reports:
            user_reports[entry.user_email] = {}
        
        entry_date = entry.timestamp.date()
        if entry_date not in user_reports[entry.user_email]:
            user_reports[entry.user_email][entry_date] = []
        
        user_reports[entry.user_email][entry_date].append(entry)
    
    # Calculate daily reports for each user
    processed_reports = {}
    for user_email, date_entries in user_reports.items():
        processed_reports[user_email] = {}
        for date, daily_entries in date_entries.items():
            processed_reports[user_email][date] = DailyReport(user_email, date, daily_entries)
    
    return render_template('admin/reports.html',
                         user_reports=processed_reports,
                         users=users,
                         selected_user=user_email,
                         start_date=start_date,
                         end_date=end_date)

@bp.route('/export_csv')
@admin_required
def export_csv():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    user_email = request.args.get('user_email')
    
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        today = datetime.now().date()
        start_date = today.replace(day=1)
        end_date = today
    
    # Get entries
    if user_email:
        entries = TimeEntry.get_user_entries(user_email, start_date, end_date)
    else:
        entries = TimeEntry.get_all_entries(start_date, end_date)
    
    # Create CSV content
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Data', 'Usuario', 'Tipo', 'Horario', 'Observacoes'])
    
    for entry in entries:
        writer.writerow([
            entry.timestamp.strftime('%Y-%m-%d'),
            entry.user_email,
            entry.entry_type,
            entry.timestamp.strftime('%H:%M:%S'),
            entry.notes
        ])
    
    csv_content = output.getvalue()
    
    # Upload to Dropbox
    filename = f'relatorio_{start_date}_a_{end_date}.csv'
    download_url = upload_report_file(csv_content.encode('utf-8'), filename)
    
    if download_url:
        # Redirect to Dropbox download
        return redirect(download_url)
    else:
        # Fallback to direct download
        response = make_response(csv_content)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response

@bp.route('/notifications', methods=['GET', 'POST'])
@admin_required
def notifications():
    notification_service = NotificationService()
    
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        notification_type = request.form['type']  # 'global', 'group', 'individual'
        target = request.form.get('target', '')
        
        if notification_type == 'global':
            notification_service.send_global_notification(title, message)
        elif notification_type == 'group':
            notification_service.send_group_notification(title, message, target)
        elif notification_type == 'individual':
            notification_service.send_individual_notification(title, message, target)
        
        flash('Notificação enviada com sucesso!', 'success')
    
    # Get recent notifications
    recent_notifications = notification_service.get_recent_notifications()
    users = User.get_all_users()
    
    return render_template('admin/notifications.html', 
                         notifications=recent_notifications,
                         users=users)

@bp.route('/user/<user_email>/toggle_status')
@admin_required
def toggle_user_status(user_email):
    user = User.get_by_email(user_email)
    if user:
        user.is_active = not user.is_active
        user.save()
        status = "ativado" if user.is_active else "desativado"
        flash(f'Usuário {status} com sucesso!', 'success')
    else:
        flash('Usuário não encontrado!', 'error')
    
    return redirect(url_for('admin.users'))