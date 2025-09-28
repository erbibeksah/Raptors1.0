# Network Analysis Plugin
import re

def register(plugin_manager):
    plugin_manager.register_handler('config', analyze_network_config)
    plugin_manager.register_processor(find_network_refs)

def analyze_network_config(filepath, previewer):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content)
        ports = re.findall(r':\d{2,5}\b', content)
        domains = re.findall(r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', content)
        
        print(f"\033[93m🌐 Network Configuration Analysis\033[0m")
        if ips: print(f"IP Addresses: {', '.join(set(ips[:5]))}")
        if ports: print(f"Ports: {', '.join(set(ports[:5]))}")
        if domains: print(f"Domains: {', '.join(set(domains[:3]))}")
        
        previewer.preview_text(content)
    except Exception as e:
        print(f"\033[91m❌ Network analysis error: {e}\033[0m")

def find_network_refs(filepath, content, file_type):
    urls = re.findall(r'https?://[^\s<>"\']+', content)
    if urls:
        print(f"\n\033[93m🔗 URLs Found ({len(urls)})\033[0m")
        for url in urls[:3]:
            print(f"  {url}")
        if len(urls) > 3:
            print(f"  ... and {len(urls)-3} more")