import os,sys,json,csv,argparse,re,importlib.util
from pathlib import Path
from datetime import datetime
try:
    from openai import OpenAI
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

Colors = type('', (), {'RESET':'\033[0m','BOLD':'\033[1m','RED':'\033[91m','GREEN':'\033[92m','YELLOW':'\033[93m','BLUE':'\033[94m','MAGENTA':'\033[95m','CYAN':'\033[96m','GRAY':'\033[90m'})()

class PluginManager:
    def __init__(self): self.handlers,self.processors = {},[]
    def load_plugin(self, plugin_path):
        try:
            spec = importlib.util.spec_from_file_location("plugin", plugin_path)
            if not spec: return False
            plugin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin)
            if hasattr(plugin, 'register'): plugin.register(self); return True
        except Exception as e: print(f"{Colors.RED}❌ Plugin error: {e}{Colors.RESET}")
        return False
    def register_handler(self, file_type, handler): self.handlers[file_type] = handler
    def register_processor(self, processor): self.processors.append(processor)
    def get_handler(self, file_type): return self.handlers.get(file_type)
    def process_file(self, filepath, content, file_type):
        for processor in self.processors:
            try: processor(filepath, content, file_type)
            except Exception as e: print(f"{Colors.YELLOW}⚠️ Processor error: {e}{Colors.RESET}")

class FilePreview:
    def __init__(self, use_ai=False, plugin_manager=None):
        self.max_lines,self.max_width = 50,120
        self.use_ai = use_ai and AI_AVAILABLE
        self.plugins = plugin_manager or PluginManager()
        if self.use_ai:
            api_key = os.environ.get("OPENAI_API_KEY")
            self.openai = OpenAI(api_key=api_key) if api_key else None
            self.use_ai = bool(self.openai)
    def detect_type(self, filepath):
        ext = Path(filepath).suffix.lower()
        try:
            with open(filepath, 'rb') as f: header = f.read(512)
        except: return 'binary'
        if b'\x00' in header:
            if header.startswith(b'\x89PNG'): return 'png'
            elif header.startswith((b'\xff\xd8\xff', b'JFIF')): return 'jpeg'
            elif header.startswith(b'GIF8'): return 'gif'
            elif header.startswith(b'%PDF'): return 'pdf'
            return 'binary'
        type_map = {'.json':'json','.yaml':'yaml','.yml':'yaml','.csv':'csv','.tsv':'tsv','.xml':'xml','.log':'log','.conf':'config','.cfg':'config','.py':'python','.js':'javascript','.html':'html','.css':'css','.md':'markdown','.sql':'sql','.sh':'shell','.env':'env','.ini':'config'}
        return type_map.get(ext, 'text')
    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024: return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
    def print_header(self, filepath, file_type, size):
        path = Path(filepath)
        modified = datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}📄 {path.name}{Colors.RESET}")
        print(f"{Colors.GRAY}Type: {file_type.upper()} | Size: {self.format_size(size)} | Modified: {modified}{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")
    def print_lines(self, lines, colorize_func=None):
        for i, line in enumerate(lines[:self.max_lines]):
            if len(line) > self.max_width: line = line[:self.max_width] + f"{Colors.GRAY}...{Colors.RESET}"
            colored_line = colorize_func(line) if colorize_func else line
            print(f"{Colors.GRAY}{i+1:3d}{Colors.RESET} {colored_line}")
        if len(lines) > self.max_lines: print(f"{Colors.YELLOW}... {len(lines) - self.max_lines} more lines{Colors.RESET}")
    def preview_json(self, content):
        try:
            formatted = json.dumps(json.loads(content), indent=2, ensure_ascii=False)
            lines = formatted.split('\n')
            def colorize(line): return re.sub(r'"([^"]+)":', f'{Colors.GREEN}"\\1"{Colors.RESET}:', line) if '"' in line and ':' in line else line
            self.print_lines(lines, colorize)
        except: self.preview_text(content)
    def preview_csv(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f: rows = list(csv.reader(f))
            if not rows: return
            headers = rows[0]
            print(f"{Colors.BOLD}{Colors.GREEN}Columns ({len(headers)}): {', '.join(headers)}{Colors.RESET}\n")
            for i, row in enumerate(rows[:min(10, len(rows))]):
                if i == 0:
                    print(f"{Colors.CYAN}{' | '.join(f'{cell:15.15}' for cell in row)}{Colors.RESET}")
                    print(f"{Colors.CYAN}{'-' * (len(headers) * 18)}{Colors.RESET}")
                else:
                    print(f"{Colors.GRAY}{i:2d}{Colors.RESET} {' | '.join(f'{str(cell):15.15}' for cell in row)}")
            if len(rows) > 10: print(f"{Colors.YELLOW}... {len(rows) - 10} more rows{Colors.RESET}")
        except Exception as e: print(f"{Colors.RED}Error reading CSV: {e}{Colors.RESET}")
    def preview_log(self, content):
        lines = content.split('\n')
        def colorize(line):
            line = line.strip()
            if not line: return line
            color = Colors.RESET
            if any(word in line.upper() for word in ['ERROR', 'FAIL', 'FATAL']): color = Colors.RED
            elif any(word in line.upper() for word in ['WARN', 'WARNING']): color = Colors.YELLOW
            elif any(word in line.upper() for word in ['INFO', 'SUCCESS']): color = Colors.GREEN
            elif any(word in line.upper() for word in ['DEBUG', 'TRACE']): color = Colors.GRAY
            ts_match = re.match(r'(\d{4}-\d{2}-\d{2}[\s\t]\d{2}:\d{2}:\d{2})', line)
            if ts_match:
                ts,rest = ts_match.group(1),line[len(ts_match.group(1)):]
                return f"{Colors.CYAN}{ts}{Colors.RESET}{color}{rest}{Colors.RESET}"
            return f"{color}{line}{Colors.RESET}"
        self.print_lines([line for line in lines if line.strip()], colorize)
    def preview_image(self, filepath):
        try:
            from PIL import Image
            img = Image.open(filepath)
            print(f"{Colors.GREEN}📸 Image Preview{Colors.RESET}")
            print(f"Dimensions: {img.width} × {img.height}")
            print(f"Mode: {img.mode}")
            if hasattr(img, 'getexif') and img.getexif(): print("Contains EXIF data")
        except ImportError: print(f"{Colors.YELLOW}Image file detected. Install PIL/Pillow for detailed preview.{Colors.RESET}")
        except Exception as e: print(f"{Colors.RED}Error reading image: {e}{Colors.RESET}")
    def preview_binary(self, filepath):
        try:
            with open(filepath, 'rb') as f: data = f.read(256)
            print(f"{Colors.MAGENTA}🔧 Binary Preview (first 256 bytes){Colors.RESET}")
            hex_dump = ' '.join(f'{b:02x}' for b in data)
            for i in range(0, len(hex_dump), 48):
                chunk,ascii_part = hex_dump[i:i+48],''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i//3:(i//3)+16])
                print(f"{Colors.GRAY}{i//3:08x}{Colors.RESET}  {chunk:<48} {Colors.CYAN}|{ascii_part}|{Colors.RESET}")
        except Exception as e: print(f"{Colors.RED}Error reading binary file: {e}{Colors.RESET}")
    def preview_text(self, content): self.print_lines(content.split('\n'))
    def preview_code(self, content, lang):
        keywords = {'python': ['def', 'class', 'import', 'from', 'if', 'for', 'while', 'try', 'except'],'javascript': ['function', 'const', 'let', 'var', 'if', 'for', 'while', 'try', 'catch'],'shell': ['#!/bin/bash', 'function', 'if', 'for', 'while', 'case', 'echo']}
        def colorize(line):
            colored = line
            for keyword in keywords.get(lang, []):
                colored = re.sub(rf'\b{keyword}\b', f'{Colors.BLUE}{keyword}{Colors.RESET}', colored)
            if line.strip().startswith('#'): return f"{Colors.GREEN}{line}{Colors.RESET}"
            elif line.strip().startswith(('function', 'def ', 'class ')): return f"{Colors.MAGENTA}{line}{Colors.RESET}"
            return colored
        self.print_lines(content.split('\n'), colorize)
    def analyze_file_comprehensive(self, filepath, content, file_type):
        path = Path(filepath)
        stat = path.stat()
        lines = content.count('\n') + 1 if content else 0
        words = len(content.split()) if content else 0
        stats = {'lines': lines, 'words': words, 'chars': len(content), 'size': stat.st_size, 'perms': oct(stat.st_mode)[-3:]}
        code_stats = {}
        if file_type in ['python', 'javascript', 'shell']:
            functions = len(re.findall(r'^\s*(def |function |function\s)', content, re.MULTILINE))
            classes = len(re.findall(r'^\s*class\s', content, re.MULTILINE))
            comments = len(re.findall(r'^\s*#', content, re.MULTILINE))
            imports = len(re.findall(r'^\s*(import |from )', content, re.MULTILINE))
            code_stats = {'functions': functions, 'classes': classes, 'comments': comments, 'imports': imports}
        patterns = {}
        urls = re.findall(r'https?://[^\s<>"\']+', content)
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content)
        if urls: patterns['urls'] = len(urls)
        if emails: patterns['emails'] = len(emails)
        if ips: patterns['ips'] = len(ips)
        security = {}
        mode = stat.st_mode
        if mode & 0o002: security['world_writable'] = True
        if mode & 0o004: security['world_readable'] = True
        if mode & 0o001: security['world_executable'] = True
        sensitive_patterns = ['password', 'secret', 'key', 'token', 'api', 'auth']
        sensitive_lines = [i+1 for i, line in enumerate(content.lower().split('\n')) if any(pattern in line for pattern in sensitive_patterns)]
        if sensitive_lines: security['sensitive_content'] = len(sensitive_lines)
        return stats, code_stats, patterns, security
    def show_comprehensive_analysis(self, filepath, content, file_type):
        stats, code_stats, patterns, security = self.analyze_file_comprehensive(filepath, content, file_type)
        print(f"\n{Colors.CYAN}📊 Comprehensive Analysis{Colors.RESET}")
        print(f"File: {stats['lines']:,} lines | {stats['words']:,} words | {stats['chars']:,} chars | {self.format_size(stats['size'])}")
        if code_stats:
            print(f"Code: {code_stats.get('functions', 0)} functions | {code_stats.get('classes', 0)} classes | {code_stats.get('comments', 0)} comments | {code_stats.get('imports', 0)} imports")
        if patterns:
            pattern_str = ' | '.join(f"{count} {name}" for name, count in patterns.items())
            print(f"Data: {pattern_str}")
        if security:
            security_items = []
            if security.get('world_writable'): security_items.append('world-writable')
            if security.get('world_readable'): security_items.append('world-readable')
            if security.get('world_executable'): security_items.append('world-executable')
            if security.get('sensitive_content'): security_items.append(f"{security['sensitive_content']} sensitive lines")
            if security_items: print(f"{Colors.YELLOW}Security: {' | '.join(security_items)}{Colors.RESET}")
    def ai_analyze_content(self, content, file_type, filepath):
        if not self.use_ai or not self.openai: return
        try:
            prompts = {'python':'Analyze this Python code structure','javascript':'Analyze this JavaScript functionality','shell':'Analyze this shell script','html':'Analyze this HTML structure','css':'Analyze this CSS styling','sql':'Analyze this SQL query','json':'Analyze this JSON data','csv':'Analyze this CSV dataset','log':'Analyze this log file for events and issues'}
            response = self.openai.chat.completions.create(model="gpt-4o-mini",messages=[{"role": "user", "content": f"{prompts.get(file_type, f'Summarize this {file_type} file')}:\n\n{content[:2000]}"}],max_tokens=300)
            analysis = response.choices[0].message.content
            print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}\n{Colors.MAGENTA}🤖 AI INSIGHTS: {file_type.upper()} ANALYSIS\n{'='*50}{Colors.RESET}")
            for line in analysis.split('\n'):
                if line.strip():
                    if line.startswith('#') or '**' in line or line.startswith('###'): print(f"{Colors.BOLD}{Colors.GREEN}{line}{Colors.RESET}")
                    elif any(word in line.lower() for word in ['error', 'issue', 'problem', 'warning', 'bug']): print(f"{Colors.YELLOW}{line}{Colors.RESET}")
                    elif any(word in line.lower() for word in ['key', 'important', 'critical', 'main', 'purpose']): print(f"{Colors.CYAN}{line}{Colors.RESET}")
                    else: print(f"{Colors.RESET}{line}")
            print(f"{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.RESET}\n")
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg: print(f"{Colors.YELLOW}⚠️  AI rate limit Exceeded{Colors.RESET}")
            elif "401" in error_msg: print(f"{Colors.RED}⚠️  Invalid API key{Colors.RESET}")
            elif "network" in error_msg.lower(): print(f"{Colors.YELLOW}⚠️  Network error{Colors.RESET}")
            else: print(f"{Colors.YELLOW}⚠️  AI unavailable: {error_msg[:40]}...{Colors.RESET}")
    def preview_file(self, filepath):
        try:
            if not os.path.exists(filepath): return print(f"{Colors.RED}❌ File not found: {filepath}{Colors.RESET}")
            if not os.access(filepath, os.R_OK): return print(f"{Colors.RED}❌ Permission denied: {filepath}{Colors.RESET}")
            file_type,size = self.detect_type(filepath),os.path.getsize(filepath)
            self.print_header(filepath, file_type, size)
            plugin_handler = self.plugins.get_handler(file_type)
            if plugin_handler:
                try: return plugin_handler(filepath, self)
                except Exception as e: print(f"{Colors.YELLOW}⚠️ Plugin failed, using default: {e}{Colors.RESET}")
            if file_type in ['png', 'jpeg', 'gif']: return self.preview_image(filepath)
            elif file_type == 'binary': return self.preview_binary(filepath)
            elif size > 10 * 1024 * 1024: return print(f"{Colors.YELLOW}⚠️  File too large for preview (>10MB){Colors.RESET}")
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f: content = f.read()
                if not content.strip(): return print(f"{Colors.GRAY}📭 File is empty{Colors.RESET}")
                self.plugins.process_file(filepath, content, file_type)
                if file_type == 'json': self.preview_json(content)
                elif file_type in ['csv', 'tsv']: self.preview_csv(filepath)
                elif file_type == 'log': self.preview_log(content)
                elif file_type in ['python', 'javascript', 'shell']: self.preview_code(content, file_type)
                else: self.preview_text(content)
                self.show_comprehensive_analysis(filepath, content, file_type)
                if self.use_ai and content.strip(): self.ai_analyze_content(content, file_type, filepath)
            except UnicodeDecodeError: print(f"{Colors.YELLOW}⚠️  Non-text data - showing as binary{Colors.RESET}"); self.preview_binary(filepath)
            except MemoryError: print(f"{Colors.RED}❌ File too large for memory{Colors.RESET}")
            except Exception as e: print(f"{Colors.RED}❌ Error reading: {str(e)[:60]}{Colors.RESET}")
        except Exception as e: print(f"{Colors.RED}❌ Unexpected error: {str(e)[:60]}{Colors.RESET}")

def main():
    try:
        parser = argparse.ArgumentParser(description='🔍 Smart File Preview Tool with Plugin Support')
        parser.add_argument('file', help='File to preview')
        parser.add_argument('-n', '--lines', type=int, default=50, help='Max lines (default: 50)')
        parser.add_argument('-w', '--width', type=int, default=120, help='Max width (default: 120)')
        parser.add_argument('--ai', action='store_true', help='Enable AI analysis (requires OpenAI API key)')
        parser.add_argument('--plugin', action='append', help='Load plugin file(s)')
        args = parser.parse_args()
        if args.lines <= 0 or args.width <= 0: print(f"{Colors.RED}❌ Lines and width must be positive{Colors.RESET}"); sys.exit(1)
        plugin_manager = PluginManager()
        if args.plugin:
            for plugin_path in args.plugin:
                if os.path.exists(plugin_path):
                    if plugin_manager.load_plugin(plugin_path): print(f"{Colors.GREEN}✅ Loaded plugin: {plugin_path}{Colors.RESET}")
                    else: print(f"{Colors.RED}❌ Failed to load plugin: {plugin_path}{Colors.RESET}")
                else: print(f"{Colors.RED}❌ Plugin not found: {plugin_path}{Colors.RESET}")
        previewer = FilePreview(use_ai=args.ai, plugin_manager=plugin_manager)
        previewer.max_lines,previewer.max_width = min(args.lines, 1000),min(args.width, 500)
        previewer.preview_file(args.file)
    except KeyboardInterrupt: print(f"\n{Colors.YELLOW}⚠️  Cancelled by user{Colors.RESET}"); sys.exit(0)
    except Exception as e: print(f"{Colors.RED}❌ Application error: {str(e)[:60]}{Colors.RESET}"); sys.exit(1)

if __name__ == '__main__': main()