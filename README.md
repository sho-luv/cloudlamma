# Ollama Setup Tool

This Python script simplifies the process of setting up and exposing Ollama, a tool for running large language models locally. It can automatically install Ollama and cloudflared (for creating secure tunnels), download models, and manage their execution.

## Features

* **Easy Installation:** Automatically installs Ollama and cloudflared using your system's package manager (brew or apt).
* **Model Management:**
    * Downloads specified models from the Ollama model hub.
    * Lists available models on your local Ollama instance.
    * Runs models in interactive mode.
* **Cloudflare Tunnel Integration:** Creates a temporary Cloudflare tunnel to securely expose your local Ollama instance to the internet.
* **Domain Listing:** (Optional) Lists domains associated with your Cloudflare account (requires API token).
* **Checks:** Allows you to quickly check if Ollama and cloudflared are installed and if Ollama is running.
* **Non-Interactive Mode:** Supports a `--yes` flag to automatically accept installation prompts.
* **Verbose Output:** Provides detailed output from the cloudflared tunnel with the `-v` or `--verbose` flag.

## Prerequisites

* **Python 3:** Make sure you have Python 3 installed on your system.
* **pip:** Python's package installer (should come with Python).
* **Internet Connection:** Required for downloading Ollama, cloudflared, and models.

## Installation

1.  **Download the script:**
    ```bash
    wget [https://raw.githubusercontent.com/your-repo/ollama_setup.py](https://raw.githubusercontent.com/your-repo/ollama_setup.py) -O ollama_setup.py
    chmod +x ollama_setup.py
    ```
    *(Replace `https://raw.githubusercontent.com/your-repo/ollama_setup.py` with the actual raw URL of the script)*

2.  **Install the `requests` library:**
    ```bash
    pip install requests
    ```

## Usage

Run the script with various command-line arguments to perform different actions.

```bash
./ollama_setup.py [options]
```
