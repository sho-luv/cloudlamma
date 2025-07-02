# CloudLamma - Secure Ollama Setup Tool

**Quick, free LLM deployment for rapid prototyping and experimentation.**

CloudLamma was created to solve a simple problem: I wanted a tool that could quickly spin up a local LLM using Ollama and expose it to the internet via Cloudflare tunnels - all for free. Whether you're prototyping AI applications, testing models, or need temporary LLM access, CloudLamma lets you deploy and tear down language models in minutes without any hosting costs.

This robust Python script automatically installs Ollama and cloudflared, manages models, and creates secure tunnels with enterprise-grade security features and comprehensive error handling.

## Why CloudLamma?

**The Problem:** Setting up LLMs for quick testing or temporary projects often involves:
- Complex cloud provider setup and billing
- Expensive GPU instances that run 24/7
- Time-consuming configuration for internet access
- Manual teardown processes that waste money

**The Solution:** CloudLamma provides:
- **Zero hosting costs** - Uses your local hardware + free Cloudflare tunnels
- **Rapid deployment** - From zero to accessible LLM in under 5 minutes
- **Easy teardown** - Simple Ctrl+C to stop and clean up everything
- **Internet accessibility** - Secure HTTPS endpoints for testing webhooks, APIs, or sharing
- **Multiple models** - Switch between different LLMs without cloud migration

**Perfect for:**
- AI application prototyping and development
- Testing different models before committing to cloud hosting
- Temporary demos and presentations
- Educational projects and experimentation
- Cost-conscious development workflows

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

**Get from zero to internet-accessible LLM in under 5 minutes:**

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

3. **Deploy everything with one command:**
   ```bash
   chmod +x cloudlamma.py
   ./cloudlamma.py --yes
   ```

That's it! CloudLamma will:
- Install Ollama and cloudflared automatically
- Download the default model (llama3)
- Start the services
- Create a secure Cloudflare tunnel
- Give you an HTTPS URL to access your LLM

### Quick Commands

**Deploy with auto-install:**
```bash
./cloudlamma.py --yes
```

**Test a different model:**
```bash
./cloudlamma.py --pull codellama
./cloudlamma.py --yes  # Restart tunnel with new model
```

**Quick status check:**
```bash
./cloudlamma.py --check
```

**Stop everything:**
```bash
# Just press Ctrl+C in the terminal running CloudLamma
# Everything stops and cleans up automatically
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
