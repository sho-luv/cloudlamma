# CloudLamma - Secure Ollama Setup Tool

A robust Python script that simplifies setting up and exposing Ollama with enterprise-grade security features. CloudLamma automatically installs Ollama and cloudflared, manages models, and creates secure tunnels with comprehensive error handling and retry logic.

## Features

### Security & Reliability
* **Input Validation:** Prevents command injection with comprehensive model name validation
* **Secure File Handling:** Uses secure temporary files instead of predictable file names
* **Network Resilience:** Automatic retry logic with exponential backoff for network operations
* **Comprehensive Error Handling:** Detailed error messages with actionable suggestions

### Installation & Management
* **Cross-Platform Installation:** Supports brew (macOS) and apt (Ubuntu/Debian) package managers
* **Smart Service Detection:** Health checks ensure services are responsive before proceeding
* **Configurable Timeouts:** Customizable timeout settings for different operations

### Model Management
* **Automatic Model Downloads:** Downloads models from the Ollama hub with progress tracking
* **Model Validation:** Ensures model names are safe and properly formatted
* **Interactive Model Running:** Run models in interactive chat mode
* **Model Listing:** View all available models on your local instance

### Cloudflare Integration
* **Secure Tunnel Creation:** Creates temporary Cloudflare tunnels with proper cleanup
* **Domain Management:** List domains in your Cloudflare account (requires API token)
* **Configurable Endpoints:** Customizable port and service configurations

### Developer-Friendly
* **Verbose Mode:** Detailed output for debugging with `-v` flag
* **Non-Interactive Mode:** `--yes` flag for automated deployments
* **Status Checking:** Quick health checks for installed services
* **Centralized Configuration:** Easy customization through configuration dataclass

## Prerequisites

* **Python 3.7+** with pip
* **Internet Connection** for downloading Ollama, cloudflared, and models
* **sudo privileges** for package installation (Linux)
* **Homebrew** (macOS) or **apt** (Ubuntu/Debian) package manager

## Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sho-luv/cloudlamma.git
   cd cloudlamma
   ```

2. **Install dependencies:**
   ```bash
   pip install requests
   ```

3. **Make executable:**
   ```bash
   chmod +x cloudlamma.py
   ```

### Basic Usage

**Setup and start tunnel (default):**
```bash
./cloudlamma.py
```

**Pull a specific model:**
```bash
./cloudlamma.py --pull llama3
```

**Run a model interactively:**
```bash
./cloudlamma.py --run llama3
```

**Check installation status:**
```bash
./cloudlamma.py --check
```

## Detailed Usage

### Command-Line Options

| Option | Description |
|--------|-------------|
| `--yes` | Automatically accept all installation prompts |
| `--check` | Check if Ollama and cloudflared are installed and running |
| `--pull [MODEL]` | Pull a specific model (default: llama3) |
| `--run [MODEL]` | Run a model in interactive mode (default: llama3) |
| `--list-models` | List all available models on local Ollama instance |
| `--list-domains` | List domains in Cloudflare account (requires API token) |
| `-v, --verbose` | Show detailed output from cloudflared tunnel |

### Examples

**Non-interactive installation:**
```bash
./cloudlamma.py --yes
```

**Pull and run a specific model:**
```bash
./cloudlamma.py --pull codellama
./cloudlamma.py --run codellama
```

**Check service status:**
```bash
./cloudlamma.py --check
# Output:
# [+] Ollama installed: True
# [+] cloudflared installed: True  
# [+] Ollama running: True
```

**List available models:**
```bash
./cloudlamma.py --list-models
```

## Configuration

CloudLamma uses a centralized configuration system that you can customize by modifying the `Config` dataclass in `cloudlamma.py`:

```python
@dataclass
class Config:
    # Network settings
    ollama_port: int = 11434
    default_model: str = "llama3"
    
    # Timeout settings (in seconds)
    install_timeout: int = 300
    api_timeout: int = 30
    health_check_timeout: int = 5
    
    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0
    retry_backoff: float = 2.0
```

### Environment Variables

For Cloudflare domain listing, set your API token:
```bash
export CLOUDFLARE_API_TOKEN="your_api_token_here"
./cloudlamma.py --list-domains
```

## Security Features

CloudLamma includes enterprise-grade security features:

- **Input Validation**: All model names are validated to prevent command injection attacks
- **Secure File Handling**: Uses Python's `tempfile` module for secure temporary file creation
- **Network Resilience**: Automatic retry logic with exponential backoff for network failures
- **Error Handling**: Comprehensive exception handling prevents information leakage
- **Timeout Protection**: All network operations have configurable timeouts

## Troubleshooting

### Common Issues

**"Permission denied" during installation:**
```bash
# Ensure you have sudo privileges
sudo -v
./cloudlamma.py --yes
```

**Network timeout errors:**
```bash
# Check internet connection and try again
./cloudlamma.py --check
./cloudlamma.py --verbose  # For detailed output
```

**Ollama not responsive:**
```bash
# CloudLamma automatically handles service startup
# If issues persist, manually restart:
killall ollama
./cloudlamma.py
```

**Model pull failures:**
```bash
# Verify model name is valid
./cloudlamma.py --list-models
./cloudlamma.py --pull llama3  # Use exact model name
```

### Support

- **Issues**: Report bugs at https://github.com/sho-luv/cloudlamma/issues
- **Documentation**: See inline help with `./cloudlamma.py --help`
- **Verbose Output**: Use `-v` flag for detailed debugging information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper error handling and input validation
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please see the repository for license details.

## Acknowledgments

- **Ollama**: For providing an excellent local LLM runtime
- **Cloudflare**: For secure tunnel infrastructure
- **Community**: For feedback and contributions

---

**Built with security and reliability in mind**
