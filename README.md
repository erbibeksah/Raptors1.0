# Raptors1.0 🔍 CLI Preview Tool with Plugin System

A powerful, type-aware file preview CLI tool with AI +  dynamic plugin extensibility. Built for the **Raptors Hackathon SEP/2025** - delivering maximum functionality in minimal lines.

## ✨ Features

### 🎯 Core Capabilities
- **Type-aware previews**: Intelligent file type detection and specialized rendering
- **Syntax highlighting**: Color-coded output for JSON, Python, JavaScript, shell scripts
- **Binary analysis**: Hex dumps with ASCII representation for binary files
- **Image metadata**: Dimensions and format info (with PIL/Pillow)
- **Log parsing**: Timestamped log entries with error/warning highlighting
- **CSV tables**: Formatted column display with row counting

### 🔌 Plugin System
- **Dynamic loading**: Load plugins at runtime with `--plugin` argument
- **Handler plugins**: Override default file type processing completely
- **Processor plugins**: Add analysis to any file type without disrupting core functionality
- **Error isolation**: Plugin failures don't crash the main application
- **Extensible**: Add new functionality without modifying core code

### 🤖 AI Integration
- **OpenAI analysis**: AI-powered content insights and summaries
- **File-specific prompts**: Tailored analysis for different file types
- **Error handling**: Graceful degradation when AI is unavailable

## 🚀 Installation & Usage

### Basic Usage
```bash
# Preview any file
py preview.py sample.json

# Customize output
py preview.py --lines 30 --width 100 sample.json

# Enable AI analysis (requires OPENAI_API_KEY)
py preview.py --ai sample.json
```

### Plugin Usage
```bash
# Load a single plugin
py preview.py --plugin plugins/stats_plugin.py config.yaml

# Load multiple plugins
py preview.py \
  --plugin plugins/stats_plugin.py \
  --plugin plugins/hash_plugin.py \
  --plugin plugins/network_plugin.py \
  sample.conf

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
py preview.py --plugin plugins/my_plugin.py myfile.xml
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
├── preview.py             # Main CLI tool (228 executables lines)
├── plugins/               # Plugin directory
│   ├── stats_plugin.py    # File statistics analysis
│   ├── hash_plugin.py     # File hashing functionality
│   └── network_plugin.py  # Network configuration analysis
├── test_files/            # Sample files for testing
│   ├── sample.conf
│   ├── sample.cs
│   ├── sample.json
│   ├── sample.log
│   ├── sample.png
│   └── network.conf
└── README.md             # This file
```

## 🏆 Hackathon Highlights

### Creative Constraint Solutions
- **Plugin architecture** in exactly 228 lines of Python
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
- **Exactly 228 lines** in the main tool (under 250-line limit)
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

**Final line count: 228 lines** ✅

---

*Built with ❤️ for developers who need quick, intelligent file inspection with the power of extensibility.*