# File Hash Plugin
import hashlib

def register(plugin_manager):
    plugin_manager.register_processor(show_hashes)

def show_hashes(filepath, content, file_type):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        
        md5 = hashlib.md5(data).hexdigest()[:16]
        sha1 = hashlib.sha1(data).hexdigest()[:16]
        sha256 = hashlib.sha256(data).hexdigest()[:16]
        
        print(f"\n\033[95m🔐 File Hashes (truncated)\033[0m")
        print(f"MD5: {md5}... | SHA1: {sha1}... | SHA256: {sha256}...")
    except Exception as e:
        print(f"\033[91m❌ Hash error: {e}\033[0m")