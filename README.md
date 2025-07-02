# CloudLamma

![License](https://img.shields.io/github/license/sho-luv/cloudlamma)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey)
![Status](https://img.shields.io/badge/status-active-brightgreen)

**Quick, free LLM deployment for rapid prototyping and experimentation.**

CloudLamma lets you spin up a local LLM using Ollama and expose it to the internet via Cloudflare tunnels - all for free. Deploy and tear down language models in under 5 minutes without any hosting costs.

🚀 **Zero to internet-accessible LLM in under 5 minutes**  
💰 **Zero hosting costs** - uses local hardware + free Cloudflare tunnels  
🔒 **Enterprise-grade security** with input validation and secure file handling  
⚡ **One-command deployment** with automatic installation and configuration

## Table of Contents
[Installation](#installation) • [Quick Start](#quick-start) • [Usage](#usage) • [Configuration](#configuration) • [Security](#security-features) • [Contributing](#contributing)

## Why CloudLamma?

Traditional LLM deployment for testing involves expensive cloud instances and complex setup. CloudLamma solves this by using your local hardware with free Cloudflare tunnels.

**Perfect for:** Prototyping • Model testing • Demos • Education • Cost-conscious development

## Features

✅ **One-command deployment** with automatic installation  
✅ **Cross-platform support** for macOS and Linux  
✅ **Secure tunneling** via Cloudflare with HTTPS endpoints  
✅ **Input validation** and command injection prevention  
✅ **Network resilience** with automatic retry logic  
✅ **Model management** - pull, run, and switch between models  
✅ **Health checking** ensures services are responsive  
✅ **Clean teardown** with Ctrl+C

## Installation

### Prerequisites
- Python 3.7+ with pip
- Internet connection
- sudo privileges (Linux) or Homebrew (macOS)

### Install CloudLamma

```bash
# Clone the repository
git clone https://github.com/sho-luv/cloudlamma.git
cd cloudlamma

# Install dependencies
pip install requests

# Make executable
chmod +x cloudlamma.py
```

## Quick Start

### Deploy Everything (5 minutes)
```bash
# One command to deploy everything
./cloudlamma.py --yes
```

CloudLamma will automatically:
1. Install Ollama and cloudflared
2. Download the default model (llama3)
3. Start services and health checks
4. Create secure Cloudflare tunnel
5. Display your HTTPS URL

### Common Commands
```bash
# Deploy with auto-install
./cloudlamma.py --yes

# Check status
./cloudlamma.py --check

# Use different model
./cloudlamma.py --pull codellama
./cloudlamma.py --yes

# Stop everything
# Press Ctrl+C (automatic cleanup)
```

## Usage

### Command Reference

| Command | Description |
|---------|-------------|
| `--yes` | Auto-accept installation prompts |
| `--check` | Check installation status |
| `--pull [MODEL]` | Download specific model |
| `--run [MODEL]` | Run model interactively |
| `--list-models` | Show available models |
| `--list-domains` | Show Cloudflare domains |
| `-v, --verbose` | Detailed output |

### Examples

```bash
# Full deployment
./cloudlamma.py --yes

# Model management
./cloudlamma.py --pull llama3
./cloudlamma.py --list-models

# Status and debugging
./cloudlamma.py --check
./cloudlamma.py --verbose
```

## Configuration

### Default Settings
CloudLamma works out-of-the-box but can be customized by editing the `Config` class:

```python
ollama_port: int = 11434          # Ollama service port
default_model: str = "llama3"     # Default model to download
install_timeout: int = 300        # Installation timeout (seconds)
max_retries: int = 3              # Network retry attempts
```

### Environment Variables
```bash
# For Cloudflare domain listing
export CLOUDFLARE_API_TOKEN="your_token"
./cloudlamma.py --list-domains
```

## Security Features

🔒 **Input validation** prevents command injection  
🔒 **Secure file handling** with proper temp file management  
🔒 **Network resilience** with retry logic and timeouts  
🔒 **Comprehensive error handling** with actionable messages

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Permission denied | Run `sudo -v` then retry |
| Network timeouts | Check connection, use `--verbose` |
| Ollama unresponsive | CloudLamma auto-handles, or `killall ollama` |
| Model pull fails | Verify name with `--list-models` |

**Need help?** Open an issue at https://github.com/sho-luv/cloudlamma/issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Contributions are welcome! Please ensure proper error handling and security practices.

## License

This project is open source. See the repository for license details.

---

**Liked the work? Give the repository a ⭐**

Built with ❤️ for the developer community. Supports **Ollama** and **Cloudflare** infrastructure.
