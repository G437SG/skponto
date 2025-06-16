from firebase_admin import firestore
from datetime import datetime, timedelta
from app.models.user import initialize_firebase
from typing import Optional, List, Dict, Any

class Timesheet:
    def __init__(self, user_id=None, date=None, entry_time=None, lunch_start=None, 
                 lunch_end=None, exit_time=None, total_hours=None, status='EM_ANDAMENTO',
                 created_at=None, timesheet_id=None):
        self.user_id = user_id
        self.date = date or datetime.now().date()
        self.entry_time = entry_time
        self.lunch_start = lunch_start
        self.lunch_end = lunch_end
        self.exit_time = exit_time
        self.total_hours = total_hours
        self.status = status  # EM_ANDAMENTO, FINALIZADO, AJUSTE_PENDENTE
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.timesheet_id = timesheet_id

    def calculate_total_hours(self):
        """Calculate total working hours excluding lunch break"""
        if not self.entry_time or not self.exit_time:
            return 0
        
        # Convert times to datetime for calculation
        entry = datetime.combine(self.date, self.entry_time)
        exit = datetime.combine(self.date, self.exit_time)
        
        total_time = exit - entry
        
        # Subtract lunch break if both times are recorded
        if self.lunch_start and self.lunch_end:
            lunch_start = datetime.combine(self.date, self.lunch_start)
            lunch_end = datetime.combine(self.date, self.lunch_end)
            lunch_duration = lunch_end - lunch_start
            total_time -= lunch_duration
        
        # Convert to hours (float)
        self.total_hours = total_time.total_seconds() / 3600
        return self.total_hours

    def calculate_overtime(self, expected_hours=8):
        """Calculate overtime hours"""
        if not self.total_hours:
            self.calculate_total_hours()
        
        if self.total_hours > expected_hours:
            return self.total_hours - expected_hours
        return 0

    def is_complete(self):
        """Check if timesheet has all required entries"""
        return all([self.entry_time, self.exit_time])

    def to_dict(self):
        """Convert timesheet object to dictionary for Firestore"""
        return {
            'user_id': self.user_id,
            'date': self.date,
            'entry_time': self.entry_time.strftime('%H:%M') if self.entry_time else None,
            'lunch_start': self.lunch_start.strftime('%H:%M') if self.lunch_start else None,
            'lunch_end': self.lunch_end.strftime('%H:%M') if self.lunch_end else None,
            'exit_time': self.exit_time.strftime('%H:%M') if self.exit_time else None,
            'total_hours': self.total_hours,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data, timesheet_id=None):
        """Create timesheet object from Firestore document"""
        def parse_time(time_str):
            if time_str:
                return datetime.strptime(time_str, '%H:%M').time()
            return None
        
        return cls(
            user_id=data.get('user_id'),
            date=data.get('date'),
            entry_time=parse_time(data.get('entry_time')),
            lunch_start=parse_time(data.get('lunch_start')),
            lunch_end=parse_time(data.get('lunch_end')),
            exit_time=parse_time(data.get('exit_time')),
            total_hours=data.get('total_hours'),
            status=data.get('status', 'EM_ANDAMENTO'),
            created_at=data.get('created_at'),
            timesheet_id=timesheet_id
        )

    def save(self):
        """Save timesheet to Firestore"""
        try:
            initialize_firebase()
            db = firestore.client()
            timesheets_ref = db.collection('timesheets')
            
            self.updated_at = datetime.utcnow()
            
            if self.timesheet_id:
                # Update existing timesheet
                timesheets_ref.document(self.timesheet_id).set(self.to_dict())
            else:
                # Create new timesheet
                doc_ref = timesheets_ref.add(self.to_dict())
                self.timesheet_id = doc_ref[1].id
            
            return True
        except Exception as e:
            print(f"Error saving timesheet: {e}")
            return False

    @classmethod
    def get_by_user_and_date(cls, user_id, date):
        """Get timesheet by user ID and date"""
        try:
            initialize_firebase()
            db = firestore.client()
            timesheets_ref = db.collection('timesheets')
            
            query = timesheets_ref.where('user_id', '==', user_id).where('date', '==', date).limit(1)
            docs = query.stream()
            
            for doc in docs:
                return cls.from_dict(doc.to_dict(), doc.id)
            
            return None
        except Exception as e:
            print(f"Error getting timesheet: {e}")
            return None

    @classmethod
    def get_by_user_date_range(cls, user_id, start_date, end_date):
        """Get timesheets by user ID within date range"""
        try:
            initialize_firebase()
            db = firestore.client()
            timesheets_ref = db.collection('timesheets')
            
            query = (timesheets_ref
                    .where('user_id', '==', user_id)
                    .where('date', '>=', start_date)
                    .where('date', '<=', end_date)
                    .order_by('date'))
            
            timesheets = []
            docs = query.stream()
            
            for doc in docs:
                timesheets.append(cls.from_dict(doc.to_dict(), doc.id))
            
            return timesheets
        except Exception as e:
            print(f"Error getting timesheets by date range: {e}")
            return []

    @classmethod
    def get_all_by_date_range(cls, start_date, end_date):
        """Get all timesheets within date range (admin use)"""
        try:
            initialize_firebase()
            db = firestore.client()
            timesheets_ref = db.collection('timesheets')
            
            query = (timesheets_ref
                    .where('date', '>=', start_date)
                    .where('date', '<=', end_date)
                    .order_by('date'))
            
            timesheets = []
            docs = query.stream()
            
            for doc in docs:
                timesheets.append(cls.from_dict(doc.to_dict(), doc.id))
            
            return timesheets
        except Exception as e:
            print(f"Error getting all timesheets by date range: {e}")
            return []

    @classmethod
    def get_by_id(cls, timesheet_id):
        """Get timesheet by ID"""
        try:
            initialize_firebase()
            db = firestore.client()
            
            doc = db.collection('timesheets').document(timesheet_id).get()
            if doc.exists:
                return cls.from_dict(doc.to_dict(), doc.id)
            
            return None
        except Exception as e:
            print(f"Error getting timesheet by ID: {e}")
            return None

    def delete(self):
        """Delete timesheet from Firestore"""
        try:
            if not self.timesheet_id:
                return False
                
            initialize_firebase()
            db = firestore.client()
            db.collection('timesheets').document(self.timesheet_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting timesheet: {e}")
            return False

    def register_entry(self):
        """Register entry time"""
        if not self.entry_time:
            self.entry_time = datetime.now().time()
            return self.save()
        return False

    def register_lunch_start(self):
        """Register lunch start time"""
        if not self.lunch_start:
            self.lunch_start = datetime.now().time()
            return self.save()
        return False

    def register_lunch_end(self):
        """Register lunch end time"""
        if not self.lunch_end and self.lunch_start:
            self.lunch_end = datetime.now().time()
            return self.save()
        return False

    def register_exit(self):
        """Register exit time and calculate total hours"""
        if not self.exit_time:
            self.exit_time = datetime.now().time()
            self.calculate_total_hours()
            self.status = 'FINALIZADO'
            return self.save()
        return False

    def get_status_display(self):
        """Get user-friendly status display"""
        status_map = {
            'EM_ANDAMENTO': 'Em Andamento',
            'FINALIZADO': 'Finalizado',
            'AJUSTE_PENDENTE': 'Ajuste Pendente'
        }
        return status_map.get(self.status, self.status)

    def __repr__(self):
        return f'<Timesheet {self.user_id} - {self.date}>'