from werkzeug.utils import secure_filename
from app.services.dropbox_service import dropbox_service
import os

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'csv', 'xlsx'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_user_photo(file, user_email):
    """Upload user profile photo to Dropbox"""
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        return None
    
    filename = secure_filename(file.filename)
    file_content = file.read()
    
    # Upload to Dropbox
    download_url = dropbox_service.upload_user_photo(file_content, user_email, filename)
    return download_url

def upload_report_file(file_content, filename):
    """Upload report file to Dropbox"""
    download_url = dropbox_service.upload_report(file_content, filename)
    return download_url

def delete_user_photo(file_url):
    """Delete user photo from Dropbox"""
    # Extract file path from URL if needed
    # This would need to be implemented based on your URL structure
    return True

def get_file_extension(filename):
    """Get file extension"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def validate_file_size(file, max_size_mb=16):
    """Validate file size"""
    file.seek(0, 2)  # Seek to end of file
    size = file.tell()
    file.seek(0)  # Reset to beginning
    
    max_size_bytes = max_size_mb * 1024 * 1024
    return size <= max_size_bytes

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names)-1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"