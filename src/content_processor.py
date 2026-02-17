import os
import csv
from typing import Optional
from src.logger import logger


class ContentProcessor:
    """Process different file types and extract meaningful content"""
    
    def __init__(self):
        """Initialize the content processor"""
        self.supported_extensions = ['.txt', '.csv', '.md', '.text']
    
    def process_file(self, file_path: str) -> Optional[str]:
        """
        Process a file and extract its content
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            Extracted content as string, or None if processing fails
        """
        if not os.path.exists(file_path):
            logger.error(f"❌ Файл не найден: {file_path}")
            return None
        
        try:
            # Get file extension
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            
            # Process based on file type
            if ext == '.csv':
                return self._process_csv(file_path)
            elif ext in ['.txt', '.md', '.text']:
                return self._process_text(file_path)
            else:
                logger.warning(f"⚠️ Неподдерживаемый тип файла: {ext}")
                # Try to read as text anyway
                return self._process_text(file_path)
                
        except Exception as e:
            logger.error(f"❌ Ошибка при обработке файла {file_path}: {e}")
            return None
    
    def _process_text(self, file_path: str) -> Optional[str]:
        """
        Process text-based files (.txt, .md, .text)
        
        Args:
            file_path: Path to the text file
            
        Returns:
            File content as string
        """
        try:
            # Try different encodings
            encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    
                    # Remove excessive whitespace
                    content = self._clean_text(content)
                    
                    logger.info(f"✅ Текстовый файл обработан: {os.path.basename(file_path)}")
                    return content
                    
                except UnicodeDecodeError:
                    continue
            
            logger.error(f"❌ Не удалось декодировать файл: {file_path}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Ошибка при чтении текстового файла: {e}")
            return None
    
    def _process_csv(self, file_path: str) -> Optional[str]:
        """
        Process CSV files (e.g., Google Sheets exports)
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            CSV content formatted as text
        """
        try:
            rows = []
            
            # Try different encodings
            encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding, newline='') as f:
                        reader = csv.reader(f)
                        rows = list(reader)
                    break
                except UnicodeDecodeError:
                    continue
            
            if not rows:
                logger.error(f"❌ Не удалось прочитать CSV файл: {file_path}")
                return None
            
            # Format CSV data as readable text
            content_lines = []
            
            # Add headers if present
            if rows and len(rows) > 0:
                headers = rows[0]
                content_lines.append("Данные из таблицы:\n")
                
                # Format each row
                for row in rows:
                    if row:  # Skip empty rows
                        row_text = " | ".join(str(cell).strip() for cell in row if cell)
                        if row_text:
                            content_lines.append(row_text)
            
            content = "\n".join(content_lines)
            content = self._clean_text(content)
            
            logger.info(f"✅ CSV файл обработан: {os.path.basename(file_path)} ({len(rows)} строк)")
            return content
            
        except Exception as e:
            logger.error(f"❌ Ошибка при чтении CSV файла: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text content
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        lines = [line.strip() for line in text.split('\n')]
        # Remove empty lines but keep structure
        lines = [line for line in lines if line]
        # Join with single newline
        cleaned = '\n'.join(lines)
        
        # Limit content length to avoid API limits
        max_length = 10000
        if len(cleaned) > max_length:
            logger.warning(f"⚠️ Контент обрезан с {len(cleaned)} до {max_length} символов")
            cleaned = cleaned[:max_length] + "\n...(контент обрезан)"
        
        return cleaned
    
    def extract_google_docs_content(self, file_path: str) -> Optional[str]:
        """
        Extract content from Google Docs exports (plain text format)
        This is a wrapper method for consistency
        
        Args:
            file_path: Path to the exported Google Docs file
            
        Returns:
            Extracted content
        """
        return self._process_text(file_path)
    
    def extract_google_sheets_content(self, file_path: str) -> Optional[str]:
        """
        Extract content from Google Sheets exports (CSV format)
        This is a wrapper method for consistency
        
        Args:
            file_path: Path to the exported Google Sheets file
            
        Returns:
            Extracted content formatted as text
        """
        return self._process_csv(file_path)
