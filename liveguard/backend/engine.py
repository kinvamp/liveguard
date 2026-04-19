import shutil
import os
from datetime import datetime

def trigger_manual_backup(source_path, dest_parent):
    """Copies a directory and appends a timestamp, ignoring junk files."""
    try:
        abs_source = os.path.abspath(source_path)
        folder_basename = os.path.basename(abs_source)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f"{folder_basename}_backup_{timestamp}"
        
        dest_path = os.path.join(dest_parent, folder_name)
        
        ignore_patterns = shutil.ignore_patterns('.git', '__pycache__', 'node_modules', '.venv')
        
        shutil.copytree(source_path, dest_path, ignore=ignore_patterns)
        return True, f"Backed up {folder_basename} to {folder_name}"
    
    except Exception as e:
        return False, f"Error: {str(e)}"