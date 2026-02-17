"""Google Drive integration for hotel content automation."""

import io
import os
from typing import List, Dict, Optional
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

from .logger import get_logger

logger = get_logger()


class GoogleDriveHandler:
    """Handle Google Drive operations."""
    
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    
    def __init__(self, service_account_file: str, folder_id: str):
        """
        Initialize Google Drive handler.
        
        Args:
            service_account_file: Path to service account JSON file
            folder_id: Root folder ID in Google Drive
        """
        self.folder_id = folder_id
        self.service = self._authenticate(service_account_file)
        logger.info(f"Google Drive handler initialized for folder: {folder_id}")
    
    def _authenticate(self, service_account_file: str):
        """Authenticate with Google Drive API."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                service_account_file, scopes=self.SCOPES
            )
            service = build('drive', 'v3', credentials=credentials)
            logger.info("Successfully authenticated with Google Drive")
            return service
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Drive: {e}")
            raise
    
    def list_files_in_folder(self, folder_name: str, mime_type: Optional[str] = None) -> List[Dict]:
        """
        List files in a specific folder.
        
        Args:
            folder_name: Name of the folder to search
            mime_type: Optional MIME type filter
            
        Returns:
            List of file metadata dictionaries
        """
        try:
            # Find the folder
            folder_query = f"name='{folder_name}' and '{self.folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            folder_results = self.service.files().list(
                q=folder_query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            folders = folder_results.get('files', [])
            if not folders:
                logger.warning(f"Folder '{folder_name}' not found")
                return []
            
            folder_id = folders[0]['id']
            logger.info(f"Found folder '{folder_name}' with ID: {folder_id}")
            
            # List files in the folder
            query = f"'{folder_id}' in parents and trashed=false"
            if mime_type:
                query += f" and mimeType='{mime_type}'"
            
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, mimeType, size, createdTime, modifiedTime)',
                orderBy='modifiedTime desc'
            ).execute()
            
            files = results.get('files', [])
            logger.info(f"Found {len(files)} files in folder '{folder_name}'")
            return files
        
        except HttpError as e:
            logger.error(f"HTTP error listing files in folder '{folder_name}': {e}")
            return []
        except Exception as e:
            logger.error(f"Error listing files in folder '{folder_name}': {e}")
            return []
    
    def download_file(self, file_id: str, destination_path: str) -> bool:
        """
        Download a file from Google Drive.
        
        Args:
            file_id: Google Drive file ID
            destination_path: Local path to save the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            
            # Create parent directories if they don't exist
            Path(destination_path).parent.mkdir(parents=True, exist_ok=True)
            
            with io.FileIO(destination_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    if status:
                        logger.debug(f"Download progress: {int(status.progress() * 100)}%")
            
            logger.info(f"Successfully downloaded file to: {destination_path}")
            return True
        
        except HttpError as e:
            logger.error(f"HTTP error downloading file {file_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error downloading file {file_id}: {e}")
            return False
    
    def get_video_files(self, folder_name: str = "RAW_VIDEO") -> List[Dict]:
        """Get all video files from the RAW_VIDEO folder."""
        video_mimes = [
            'video/mp4',
            'video/quicktime',
            'video/x-msvideo',
            'video/x-matroska'
        ]
        
        all_videos = []
        for mime in video_mimes:
            videos = self.list_files_in_folder(folder_name, mime)
            all_videos.extend(videos)
        
        # If no mime type filter worked, get all files and filter by extension
        if not all_videos:
            all_files = self.list_files_in_folder(folder_name)
            video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.MP4', '.MOV']
            all_videos = [
                f for f in all_files 
                if any(f['name'].endswith(ext) for ext in video_extensions)
            ]
        
        logger.info(f"Found {len(all_videos)} video files")
        return all_videos
    
    def get_photo_files(self, folder_name: str = "RAW_PHOTO") -> List[Dict]:
        """Get all photo files from the RAW_PHOTO folder."""
        image_mimes = [
            'image/jpeg',
            'image/png',
            'image/gif',
            'image/webp'
        ]
        
        all_photos = []
        for mime in image_mimes:
            photos = self.list_files_in_folder(folder_name, mime)
            all_photos.extend(photos)
        
        # If no mime type filter worked, get all files and filter by extension
        if not all_photos:
            all_files = self.list_files_in_folder(folder_name)
            photo_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.JPG', '.JPEG', '.PNG']
            all_photos = [
                f for f in all_files 
                if any(f['name'].endswith(ext) for ext in photo_extensions)
            ]
        
        logger.info(f"Found {len(all_photos)} photo files")
        return all_photos
    
    def get_text_files(self, folder_name: str = "TEXTS") -> List[Dict]:
        """Get all text files from the TEXTS folder."""
        return self.list_files_in_folder(folder_name)
    
    def get_reference_posts(self, folder_name: str = "POSTS_REFERENCE") -> List[Dict]:
        """Get all reference post files."""
        return self.list_files_in_folder(folder_name)
