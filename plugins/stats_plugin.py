# File Statistics Plugin
import os,re
from pathlib import Path

def register(plugin_manager):
    plugin_manager.register_processor(show_stats)

def show_stats(filepath, content, file_type):
    if file_type == 'binary': return
    path = Path(filepath)
    
    # Basic stats
    lines = content.count('\n') + 1 if content else 0
    words = len(content.split()) if content else 0
    chars = len(content)
    
    # Code-specific stats
    if file_type in ['python', 'javascript', 'shell']:
        functions = len(re.findall(r'^\s*(def |function |function\s)', content, re.MULTILINE))
        classes = len(re.findall(r'^\s*class\s', content, re.MULTILINE))
        comments = len(re.findall(r'^\s*#', content, re.MULTILINE))
        
        print(f"\n\033[96m📊 Code Statistics\033[0m")
        print(f"Functions: {functions} | Classes: {classes} | Comments: {comments}")
    
    # General stats
    print(f"\033[96m📈 File Statistics\033[0m")
    print(f"Lines: {lines:,} | Words: {words:,} | Characters: {chars:,}")
    
    # File system stats
    stat = path.stat()
    print(f"Permissions: {oct(stat.st_mode)[-3:]} | Inode: {stat.st_ino}")