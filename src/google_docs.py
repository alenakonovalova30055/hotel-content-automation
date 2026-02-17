"""Google Docs integration for reading hotel descriptions and reference posts."""

from typing import Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .logger import get_logger

logger = get_logger()


class GoogleDocsHandler:
    """Handle Google Docs operations."""
    
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
    
    def __init__(self, service_account_file: str):
        """
        Initialize Google Docs handler.
        
        Args:
            service_account_file: Path to service account JSON file
        """
        self.service = self._authenticate(service_account_file)
        logger.info("Google Docs handler initialized")
    
    def _authenticate(self, service_account_file: str):
        """Authenticate with Google Docs API."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                service_account_file, scopes=self.SCOPES
            )
            service = build('docs', 'v1', credentials=credentials)
            logger.info("Successfully authenticated with Google Docs")
            return service
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Docs: {e}")
            raise
    
    def read_document(self, document_id: str) -> Optional[str]:
        """
        Read text content from a Google Doc.
        
        Args:
            document_id: Google Docs document ID
            
        Returns:
            Document text content or None if failed
        """
        try:
            document = self.service.documents().get(documentId=document_id).execute()
            
            # Extract text from document
            content = document.get('body', {}).get('content', [])
            text_parts = []
            
            for element in content:
                if 'paragraph' in element:
                    paragraph = element['paragraph']
                    for text_element in paragraph.get('elements', []):
                        if 'textRun' in text_element:
                            text_parts.append(text_element['textRun']['content'])
            
            text = ''.join(text_parts)
            logger.info(f"Successfully read document (length: {len(text)} chars)")
            return text
        
        except HttpError as e:
            logger.error(f"HTTP error reading document {document_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading document {document_id}: {e}")
            return None
    
    def read_text_file(self, file_path: str) -> Optional[str]:
        """
        Read text content from a local file.
        
        Args:
            file_path: Path to local text file
            
        Returns:
            File text content or None if failed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            logger.info(f"Successfully read file: {file_path}")
            return text
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None
