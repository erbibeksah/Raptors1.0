#!/usr/bin/env python3
"""
Demo script showcasing the Raptors1.0
"""
import subprocess
import os
import time

def run_demo():
    print("🚀 Raptors1.0 System Demo")
    print("=" * 50)
    
    # Demo files to preview
    demo_files = [
        ("test_files/sample.json", "JSON with syntax highlighting"),
        ("test_files/sample.py", "Python code with statistics"),
        ("test_files/network.conf", "Network config with handler"),
        ("preview.py", "Main tool with plugins"),
    ]
    
    for filepath, description in demo_files:
        if os.path.exists(filepath):
            print(f"\n📁 {description}")
            print("-" * 30)
            
            # Run with plugins
            cmd = [
                "py", "preview.py",
                "--plugin", "..\plugins/stats_plugin.py",
                "--plugin", "..\plugins/hash_plugin.py", 
                "--plugin", "..\plugins/network_plugin.py",
                "--lines", "15",
                filepath
            ]

            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, env=env, encoding="utf-8")
                if result.returncode == 0:
                    print(result.stdout)
                else:
                    print(f"Error: {result.stderr}")
            except subprocess.TimeoutExpired:
                print("Demo timeout - continuing...")
            except Exception as e:
                print(f"Demo error: {e}")
            
            time.sleep(2)
    
    print("\n🎉 Demo completed! Try running:")
    print("py preview.py --plugin plugins/stats_plugin.py --plugin plugins/hash_plugin.py your_file.txt")

if __name__ == "__main__":
    run_demo()