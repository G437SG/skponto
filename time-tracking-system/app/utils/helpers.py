from datetime import datetime
import bcrypt

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def check_password(hashed: str, password: str) -> bool:
    """Checks a hashed password against a plain password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def format_date(date: datetime) -> str:
    """Formats a datetime object to a string."""
    return date.strftime('%Y-%m-%d %H:%M:%S')

def calculate_hours(start_time: datetime, end_time: datetime) -> float:
    """Calculates the number of hours worked between two datetime objects."""
    duration = end_time - start_time
    return duration.total_seconds() / 3600.0

def is_overtime(hours_worked: float, user_type: str) -> float:
    """Determines if hours worked are overtime based on user type."""
    if user_type == 'ADMINISTRADOR' or user_type == 'TRABALHADOR':
        standard_hours = 9.0
    elif user_type == 'ESTAGIÁRIO':
        standard_hours = 7.0
    else:
        return 0.0
    
    return max(0.0, hours_worked - standard_hours)