import dropbox
from dropbox.exceptions import AuthError, ApiError
import os
from datetime import datetime
import uuid
from flask import current_app

class DropboxService:
    def __init__(self):
        self.access_token = os.environ.get('DROPBOX_ACCESS_TOKEN')
        self.dbx = None
        self.initialize_dropbox()
    
    def initialize_dropbox(self):
        """Initialize Dropbox client"""
        if self.access_token:
            try:
                self.dbx = dropbox.Dropbox(self.access_token)
                # Test connection
                self.dbx.users_get_current_account()
                print("Dropbox connection successful")
            except AuthError as e:
                print(f"Dropbox authentication error: {e}")
                self.dbx = None
            except Exception as e:
                print(f"Dropbox initialization error: {e}")
                self.dbx = None
        else:
            print("Warning: Dropbox access token not found")
            self.dbx = None
    
    def upload_file(self, file_content, filename, folder_path="/uploads"):
        """Upload file to Dropbox and return public URL"""
        if not self.dbx:
            return None
        
        try:
            # Create unique filename
            file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
            unique_filename = f"{uuid.uuid4()}_{filename}"
            dropbox_path = f"{folder_path}/{unique_filename}"
            
            # Upload file
            self.dbx.files_upload(
                file_content,
                dropbox_path,
                mode=dropbox.files.WriteMode('overwrite'),
                autorename=True
            )
            
            # Create shared link
            try:
                shared_link = self.dbx.sharing_create_shared_link_with_settings(
                    dropbox_path,
                    settings=dropbox.sharing.SharedLinkSettings(
                        requested_visibility=dropbox.sharing.RequestedVisibility.public
                    )
                )
                # Convert to direct download link
                download_url = shared_link.url.replace('?dl=0', '?dl=1')
                return download_url
            except ApiError as e:
                # If shared link already exists, get existing one
                if 'shared_link_already_exists' in str(e):
                    links = self.dbx.sharing_list_shared_links(path=dropbox_path)
                    if links.links:
                        download_url = links.links[0].url.replace('?dl=0', '?dl=1')
                        return download_url
                raise e
                
        except Exception as e:
            print(f"Error uploading file to Dropbox: {e}")
            return None
    
    def upload_user_photo(self, file_content, user_email, filename):
        """Upload user profile photo"""
        folder_path = f"/user_photos/{user_email}"
        return self.upload_file(file_content, filename, folder_path)
    
    def upload_report(self, file_content, filename):
        """Upload report file"""
        folder_path = f"/reports/{datetime.now().strftime('%Y/%m')}"
        return self.upload_file(file_content, filename, folder_path)
    
    def delete_file(self, file_path):
        """Delete file from Dropbox"""
        if not self.dbx:
            return False
        
        try:
            self.dbx.files_delete_v2(file_path)
            return True
        except Exception as e:
            print(f"Error deleting file from Dropbox: {e}")
            return False
    
    def list_files(self, folder_path="/uploads"):
        """List files in a folder"""
        if not self.dbx:
            return []
        
        try:
            result = self.dbx.files_list_folder(folder_path)
            files = []
            for entry in result.entries:
                if isinstance(entry, dropbox.files.FileMetadata):
                    files.append({
                        'name': entry.name,
                        'path': entry.path_lower,
                        'size': entry.size,
                        'modified': entry.server_modified
                    })
            return files
        except Exception as e:
            print(f"Error listing files from Dropbox: {e}")
            return []
    
    def get_file_info(self, file_path):
        """Get file metadata"""
        if not self.dbx:
            return None
        
        try:
            metadata = self.dbx.files_get_metadata(file_path)
            return {
                'name': metadata.name,
                'path': metadata.path_lower,
                'size': metadata.size if hasattr(metadata, 'size') else 0,
                'modified': metadata.server_modified if hasattr(metadata, 'server_modified') else None
            }
        except Exception as e:
            print(f"Error getting file info from Dropbox: {e}")
            return None

# Global Dropbox service instance
dropbox_service = DropboxService()