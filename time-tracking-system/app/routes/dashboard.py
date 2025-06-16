from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.user import User
from app.models.timesheet import Timesheet
from datetime import datetime, date, timedelta
import json

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def login_required(f):
    """Decorator to require login for dashboard routes"""
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@bp.route('/')
@login_required
def index():
    """Main dashboard page"""
    user = User.get_by_email(session['user_email'])
    if not user:
        return redirect(url_for('auth.login'))
    
    # Get today's timesheet
    today = datetime.now().date()
    timesheet = Timesheet.get_by_user_and_date(user.user_id, today)
    
    # If no timesheet exists for today, create one
    if not timesheet:
        timesheet = Timesheet(user_id=user.user_id, date=today)
    
    # Get this week's timesheets for overview
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    week_timesheets = Timesheet.get_by_user_date_range(user.user_id, start_of_week, end_of_week)
    
    # Calculate weekly totals
    weekly_hours = sum(ts.total_hours or 0 for ts in week_timesheets)
    
    return render_template('dashboard.html', 
                         user=user, 
                         timesheet=timesheet, 
                         week_timesheets=week_timesheets,
                         weekly_hours=weekly_hours,
                         today=today)

@bp.route('/clock/<action>', methods=['POST'])
@login_required
def clock_action(action):
    """Handle clock in/out actions"""
    user = User.get_by_email(session['user_email'])
    if not user:
        return jsonify({'success': False, 'message': 'Usuário não encontrado'})
    
    today = datetime.now().date()
    timesheet = Timesheet.get_by_user_and_date(user.user_id, today)
    
    # Create timesheet if it doesn't exist
    if not timesheet:
        timesheet = Timesheet(user_id=user.user_id, date=today)
    
    success = False
    message = ''
    
    try:
        if action == 'entry':
            if timesheet.register_entry():
                success = True
                message = 'Entrada registrada com sucesso!'
            else:
                message = 'Entrada já foi registrada hoje.'
                
        elif action == 'lunch_start':
            if timesheet.register_lunch_start():
                success = True
                message = 'Início do almoço registrado!'
            else:
                message = 'Início do almoço já foi registrado.'
                
        elif action == 'lunch_end':
            if timesheet.register_lunch_end():
                success = True
                message = 'Fim do almoço registrado!'
            else:
                message = 'Fim do almoço já foi registrado ou início não foi marcado.'
                
        elif action == 'exit':
            if timesheet.register_exit():
                success = True
                message = 'Saída registrada com sucesso!'
            else:
                message = 'Saída já foi registrada hoje.'
        else:
            message = 'Ação inválida.'
            
    except Exception as e:
        message = f'Erro ao registrar ponto: {str(e)}'
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return jsonify({
        'success': success, 
        'message': message,
        'redirect': url_for('dashboard.index')
    })

@bp.route('/history')
@login_required
def history():
    """View timesheet history"""
    user = User.get_by_email(session['user_email'])
    if not user:
        return redirect(url_for('auth.login'))
    
    # Get date range from query parameters
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # Default to current month if no dates provided
    if not start_date_str or not end_date_str:
        today = datetime.now().date()
        start_date = today.replace(day=1)
        if today.month == 12:
            end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    else:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    
    timesheets = Timesheet.get_by_user_date_range(user.user_id, start_date, end_date)
    
    # Calculate totals
    total_hours = sum(ts.total_hours or 0 for ts in timesheets)
    expected_hours = len(timesheets) * 8  # Assuming 8 hours per day
    overtime_hours = max(0, total_hours - expected_hours)
    
    return render_template('history.html',
                         user=user,
                         timesheets=timesheets,
                         start_date=start_date,
                         end_date=end_date,
                         total_hours=total_hours,
                         expected_hours=expected_hours,
                         overtime_hours=overtime_hours)

@bp.route('/reports')
@login_required
def reports():
    """Generate and view reports"""
    user = User.get_by_email(session['user_email'])
    if not user:
        return redirect(url_for('auth.login'))
    
    # Get current month data for charts
    today = datetime.now().date()
    start_of_month = today.replace(day=1)
    if today.month == 12:
        end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    
    timesheets = Timesheet.get_by_user_date_range(user.user_id, start_of_month, end_of_month)
    
    # Prepare data for charts
    chart_data = {
        'dates': [ts.date.strftime('%Y-%m-%d') for ts in timesheets if ts.total_hours],
        'hours': [ts.total_hours for ts in timesheets if ts.total_hours],
        'overtime': [ts.calculate_overtime() for ts in timesheets if ts.total_hours]
    }
    
    return render_template('reports.html',
                         user=user,
                         timesheets=timesheets,
                         chart_data=json.dumps(chart_data))

@bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return redirect(url_for('auth.profile'))