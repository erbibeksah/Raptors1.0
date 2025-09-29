# Raptors1.0 🔍 – Smart, Extensible File Insight Tool

> **CLI Line-Limit Hackathon 2025 Submission**  
> *Exactly 250 executable lines of Python delivering maximum functionality*

Raptors1.0 is a powerful command-line tool designed to provide intelligent previews and deep analysis of diverse file types. It goes beyond traditional file viewers by integrating AI-powered content summarization and an extensible plugin system — enabling developers, analysts, and security professionals to gain rapid insights from code, configuration, logs, datasets, and binaries.

Raptors1.0 automatically detects file types (e.g., JSON, CSV, logs, Python, shell scripts, images, binaries) and renders a color-coded, human-friendly summary in the terminal. For structured formats like JSON or CSV, it highlights keys, columns, and formatting; for code, it performs lightweight syntax-aware coloring and supports AI-driven structural analysis. Security flags (e.g., world-writable files or exposed secrets) are also surfaced.

A modular plugin system allows custom handlers and processors to be added with ease — making it adaptable to any domain-specific need (e.g., YAML validation, XML transformation, or proprietary log parsing). With optional OpenAI integration, users can receive intelligent summaries, anomaly detection in logs, or even code insights on the fly.

Designed for speed, clarity, and extensibility, Raptors1.0 is ideal for DevOps workflows, data reviews, infosec triage, and file reconnaissance.

<img width="1074" height="908" alt="image" src="https://github.com/user-attachments/assets/81c5dd7a-b66b-4234-818a-acf4fac9407b" />


## ✨ Features

### 🎯 Core Capabilities
- **Type-aware previews**: Intelligent file type detection and specialized rendering
- **Comprehensive Analysis Engine**: Intelligent file type detection and specialized rendering
- **Syntax highlighting**: Color-coded output for JSON, Python, JavaScript, shell scripts
- **Binary analysis**: Hex dumps with ASCII representation for binary files
- **Image metadata**: Dimensions and format info (with PIL/Pillow)
- **Log parsing**: Timestamped log entries with error/warning highlighting
- **CSV tables**: Formatted column display with row counting

  <img width="838" height="592" alt="image" src="https://github.com/user-attachments/assets/7dcb12bc-1067-4a5b-bba5-e09688ad6daf" /> <img width="838" height="592" alt="image" src="https://github.com/user-attachments/assets/d786f34b-739a-4338-9c66-8d21d8e3ff0d" />



### 🔌 Dynamic Plugin System Architecture
- **Dynamic loading**: Load plugins at runtime with `--plugin` argument
- **Handler plugins**: Override default file type processing completely
- **Processor plugins**: Add analysis to any file type without disrupting core functionality
- **Error isolation**: Plugin failures don't crash the main application
- **Extensible**: Add new functionality without modifying core code

<img width="1150" height="800" alt="image" src="https://github.com/user-attachments/assets/97a601ca-10b5-4bbd-935a-6a4023e4265e" /> <img width="1150" height="800" alt="image" src="https://github.com/user-attachments/assets/06f1fb93-5e07-4d23-9504-8e2a644176d5" />



### 🤖 AI Integration
- **OpenAI analysis**: AI-powered content insights and summaries
- **File-specific prompts**: Tailored analysis for different file types
- **Error handling**: Graceful degradation when AI is unavailable

<img width="1548" height="848" alt="image" src="https://github.com/user-attachments/assets/3d171d2e-79a2-44bc-8d63-32bdc1382205" />


## 🚀 Quick Start Guide

### ⚡ Zero-Dependency Setup
```bash
# 1. Download/clone the project
git clone https://github.com/erbibeksah/Raptors1.0.git

# 2. Directory of the project
cd src

# 3. Verify Python 3.6+
py --version

# 4. Run immediately - no installation needed!
py preview.py --help

# 5. Test with sample files
py demo.py
```

### 🔧 Enhanced Setup (Optional)
```bash
# Install AI analysis capabilities
pip install -r requirements.txt

# Set up OpenAI integration
export OPENAI_API_KEY="your-api-key-here" or With Terminal ($env:OPENAI_API_KEY = "your-open-api-key")

# Verify enhanced features
py preview.py --ai ..\test_files/sample.py
```

### Plugin Usage
```bash
# Load a single plugin
py preview.py --plugin ..\plugins/stats_plugin.py ..\test_files/nginx.conf

# Load multiple plugins
py preview.py \
  --plugin ..\plugins/stats_plugin.py \
  --plugin ..\plugins/hash_plugin.py \
  --plugin ..\plugins/network_plugin.py \
  ..\test_files/nginx.conf

# Run the demo to see all features
py demo.py
```

## 📦 Included Plugins

### 📊 Stats Plugin (`plugins/stats_plugin.py`)
Provides comprehensive file statistics:
- **General**: Line count, word count, character count
- **Code files**: Function count, class count, comment count
- **File system**: Permissions, inode information

### 🔐 Hash Plugin (`plugins/hash_plugin.py`)
Security and integrity analysis:
- **Checksums**: MD5, SHA1, SHA256 hashes
- **Verification**: File integrity checking
- **Truncated display**: Shows first 16 characters for readability

### 🌐 Network Plugin (`plugins/network_plugin.py`)
Network configuration analysis:
- **Handler mode**: Special processing for `.conf`/`.cfg` files
- **IP extraction**: Finds IP addresses and CIDR blocks
- **Port detection**: Identifies port numbers
- **Domain discovery**: Extracts domain names
- **URL scanning**: Finds HTTP/HTTPS URLs in any file

## 🛠️ Plugin Development

### Creating a Plugin

1. **Create plugin file** (e.g., `plugins/my_plugin.py`)

```python
def register(plugin_manager):
    # Register a file type handler (overrides default processing)
    plugin_manager.register_handler('xml', handle_xml_files)
    
    # Register a processor (runs on all files)
    plugin_manager.register_processor(analyze_content)

def handle_xml_files(filepath, previewer):
    """Custom handler for XML files"""
    # Your custom XML processing logic
    pass

def analyze_content(filepath, content, file_type):
    """Processor that runs on all files"""
    # Your analysis logic
    pass
```

2. **Load the plugin**
```bash
py preview.py --plugin ..\plugins/my_plugin.py myfile.xml
```

### Plugin Types

- **Handler Plugins**: Replace default file processing entirely
  - Use `plugin_manager.register_handler(file_type, function)`
  - Function receives `(filepath, previewer_instance)`

- **Processor Plugins**: Add analysis without disrupting core functionality
  - Use `plugin_manager.register_processor(function)`
  - Function receives `(filepath, content, file_type)`

## 📁 Project Structure

```
/
├── preview.py             # Main CLI tool (250 executables lines)
├── plugins/               # Plugin directory
│   ├── stats_plugin.py    # File statistics analysis
│   ├── hash_plugin.py     # File hashing functionality
│   └── network_plugin.py  # Network configuration analysis
├── test_files/            # Sample files for testing
│   ├── sample.conf
│   ├── sample.cs
│   ├── sample.json
│   ├── sample.log
│   ├── nginx.conf
│   └── network.conf
└── README.md             # This file
```

## 🏆 Hackathon Highlights

### Creative Constraint Solutions
- **Plugin architecture** in exactly 250 lines of Python (neither 249 nor 251)
- **Dynamic loading** without sacrificing readability
- **Error isolation** preventing plugin failures from crashing the tool

### Engineering Craft
- **Clean separation** between core engine and plugins
- **Idiomatic Python** with efficient one-liners and comprehensions
- **Graceful degradation** when dependencies are missing

### Tool Utility
- **DevOps workflows**: Perfect for inspecting configs, logs, scripts
- **Security analysis**: Hash verification and network configuration review
- **Development**: Code structure analysis and syntax highlighting
- **Data exploration**: CSV parsing and JSON visualization

### Line Discipline
- **Exactly 250 lines** in the main tool (under 250-line limit)
- **No compression tricks** - clean, readable code
- **Efficient patterns** - lambda functions, tuple unpacking, method chaining

## 🎯 Supported File Types

| Type | Extension | Features |
|------|-----------|----------|
| JSON | `.json` | Syntax highlighting, structure validation |
| Python | `.py` | Keyword highlighting, function/class detection |
| JavaScript | `.js` | Syntax highlighting, keyword detection |
| Shell | `.sh` | Command highlighting, function detection |
| CSV/TSV | `.csv`, `.tsv` | Formatted tables, column analysis |
| Logs | `.log` | Timestamp parsing, error highlighting |
| Config | `.conf`, `.cfg`, `.ini` | Network analysis (with plugin) |
| Images | `.png`, `.jpg`, `.gif` | Metadata extraction |
| Binary | Any binary | Hex dump with ASCII representation |

## 📋 Requirements

### Core Dependencies
- Python 3.6+ (uses f-strings and pathlib)
- Standard library modules: `os`, `sys`, `json`, `csv`, `argparse`, `re`, `importlib`, `pathlib`, `datetime`, `hashlib`

### Optional Dependencies
- `openai` - For AI analysis features
- `PIL/Pillow` - For enhanced image preview
- Terminal with ANSI color support

## 🔧 Environment Setup

```bash
# Optional: Install AI features
pip install openai
export OPENAI_API_KEY="your-api-key-here"

# Optional: Install image analysis
pip install Pillow

# Run the tool
py preview.py --help
```

## 🎪 Demo

Run the included demo to see all features:

```bash
py demo.py
```

This demonstrates:
- JSON syntax highlighting with statistics
- Python code analysis with function counting
- Network configuration parsing with IP/domain extraction
- Plugin loading and error handling

## 🏅 CLI Line-Limit Hackathon 2025

This tool was built for the CLI Line-Limit Hackathon with the following constraints:
- **Language**: Python (250-line limit)
- **Functionality**: Real developer utility
- **Creativity**: Plugin system within constraints
- **Readability**: No compression tricks or obfuscation

**Final line count: 250 lines** ✅

---
# Raptors1.0
*Demonstrating that creative constraints drive innovation and excellence*

**Built with ❤️ for developers, DevOps engineers, and security professionals who need powerful, intelligent file inspection with unlimited extensibility.*
