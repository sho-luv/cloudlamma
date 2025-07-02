#!/usr/bin/env python3
"""
Ollama Setup Tool - Installs, configures, and exposes Ollama via Cloudflare Tunnel
with model download and management functionality.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from typing import List, Optional, Tuple

# Try to import requests, provide helpful error if missing
try:
    import requests
except ImportError:
    print("\033[91m[!]\033[0m Missing dependency: requests")
    print("Please install it with: pip install requests")
    sys.exit(1)

# Constants
OLLAMA_PORT = 11434
DEFAULT_MODEL = "llama3"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


class OllamaSetup:
    """Main class for Ollama setup and management"""

    def __init__(self):
        self.parser = self._create_argument_parser()

    def _create_argument_parser(self) -> argparse.ArgumentParser:
        """Create the command line argument parser"""
        parser = argparse.ArgumentParser(
            description="Set up and expose Ollama via Cloudflare Tunnel with model management"
        )
        parser.add_argument(
            "--yes", action="store_true", help="Automatically say yes to all install prompts"
        )
        parser.add_argument(
            "--check",
            action="store_true",
            help="Only check if Ollama and cloudflared are installed and running",
        )
        parser.add_argument(
            "--list-domains",
            action="store_true",
            help="List domains in your Cloudflare account (requires API token)",
        )
        parser.add_argument(
            "--pull",
            metavar="MODEL",
            help=f"Pull a specific model (default: {DEFAULT_MODEL})",
            nargs="?",
            const=DEFAULT_MODEL,
        )
        parser.add_argument(
            "--run",
            metavar="MODEL",
            help=f"Run a specific model (default: {DEFAULT_MODEL})",
            nargs="?",
            const=DEFAULT_MODEL,
        )
        parser.add_argument(
            "--list-models",
            action="store_true",
            help="List all available models on Ollama",
        )
        parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Show detailed output from cloudflared tunnel",
        )
        return parser

    def print_message(self, message: str, level: str = "info") -> None:
        """Print formatted messages"""
        prefix = {
            "info": f"{GREEN}[+]{RESET}",
            "warn": f"{YELLOW}[!]{RESET}",
            "error": f"{RED}[!]{RESET}",
            "question": f"{YELLOW}[?]{RESET}",
        }
        print(f"{prefix.get(level, prefix['info'])} {message}")

    def validate_model_name(self, model_name: str) -> bool:
        """Validate model name to prevent command injection and ensure reasonable format"""
        if not model_name or not isinstance(model_name, str):
            return False
        
        # Check for dangerous characters that could be used for command injection
        dangerous_chars = [';', '&', '|', '`', '$', '(', ')', '<', '>', '"', "'", '\\', '\n', '\r']
        if any(char in model_name for char in dangerous_chars):
            return False
        
        # Model names should be reasonable (alphanumeric, dots, dashes, underscores, colons for tags)
        if not re.match(r'^[a-zA-Z0-9._:-]+$', model_name):
            return False
        
        # Reasonable length limits
        if len(model_name) > 100:
            return False
            
        return True

    def sanitize_model_name(self, model_name: str) -> str:
        """Sanitize and validate model name, raising ValueError if invalid"""
        if not self.validate_model_name(model_name):
            raise ValueError(f"Invalid model name: '{model_name}'. Model names must contain only letters, numbers, dots, dashes, underscores, and colons.")
        return model_name.strip()

    def is_installed(self, command: str) -> bool:
        """Check if a command is installed"""
        return shutil.which(command) is not None

    def install_ollama(self) -> None:
        """Install Ollama using the appropriate package manager"""
        self.print_message("Installing Ollama...")
        if self.is_installed("brew"):
            subprocess.run(["brew", "install", "ollama"], check=True)
        elif self.is_installed("apt"):
            subprocess.run(["sudo", "apt", "update"], check=True)
            self.print_message(
                "Ollama is not available in the default apt repositories. "
                "Installing via install script...",
                "warn"
            )
            install_script = subprocess.run(
                ["curl", "-fsSL", "https://ollama.com/install.sh"],
                capture_output=True,
                check=True
            ).stdout.decode()
            subprocess.run(["sh"], input=install_script, text=True, check=True)
        else:
            self.print_message(
                "Unsupported package manager. Please install Ollama manually.",
                "error"
            )
            sys.exit(1)

    def install_cloudflared(self) -> None:
        """Install cloudflared using the appropriate package manager"""
        self.print_message("Installing cloudflared...")
        if self.is_installed("brew"):
            subprocess.run(["brew", "install", "cloudflared"], check=True)
        elif self.is_installed("apt"):
            subprocess.run(["sudo", "apt", "update"], check=True)
            
            # Determine architecture for correct package
            arch = subprocess.check_output(["uname", "-m"]).decode().strip()
            url = self._get_cloudflared_url(arch)
            if not url:
                self.print_message(
                    f"Unsupported architecture for automatic cloudflared installation: {arch}",
                    "error"
                )
                sys.exit(1)

            subprocess.run(["curl", "-L", "--output", "cloudflared.deb", url], check=True)
            subprocess.run(["sudo", "dpkg", "-i", "cloudflared.deb"], check=True)
            self._setup_cloudflared_config()
        else:
            self.print_message(
                "Unsupported package manager. Please install cloudflared manually.",
                "error"
            )
            sys.exit(1)

    def _get_cloudflared_url(self, arch: str) -> Optional[str]:
        """Get the appropriate cloudflared download URL based on architecture"""
        urls = {
            "x86_64": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb",
            "amd64": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb",
            "aarch64": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb",
            "arm64": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb",
            "armv7l": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-armhf.deb",
            "armhf": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-armhf.deb",
            "i386": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386.deb",
            "i686": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386.deb",
        }
        return urls.get(arch)

    def _setup_cloudflared_config(self) -> None:
        """Create the default configuration for cloudflared"""
        self.print_message("Generating default config.yml for cloudflared...")
        config_dir = os.path.expanduser("~/.cloudflared")
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, "config.yml")
        
        with open(config_path, "w") as f:
            f.write("tunnel: ollama-tunnel\n")
            f.write("credentials-file: ~/.cloudflared/ollama-tunnel.json\n")
            f.write("ingress:\n")
            f.write("  - service: http://localhost:11434\n")
        
        subprocess.run(["sudo", "cloudflared", "service", "install"], check=True)

    def is_ollama_running(self) -> bool:
        """Check if Ollama is currently running on the configured port"""
        result = subprocess.run(
            ["lsof", "-i", f":{OLLAMA_PORT}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0

    def start_ollama(self) -> None:
        """Start the Ollama server"""
        if not self.is_ollama_running():
            self.print_message("Starting Ollama on 0.0.0.0...")
            subprocess.Popen(
                ["ollama", "serve"],
                env={**os.environ, "OLLAMA_HOST": "0.0.0.0"},
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # Give Ollama a moment to start up
            time.sleep(2)

    def start_temp_tunnel(self) -> None:
        """Start a temporary Cloudflare tunnel to expose Ollama"""
        self.print_message("Starting temporary Cloudflare tunnel...")
        
        # Create secure temporary config file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yml') as temp_config:
            temp_config_path = temp_config.name
            
        try:
            process = subprocess.Popen(
                ["cloudflared", "tunnel", "--config", temp_config_path, "--url", f"http://localhost:{OLLAMA_PORT}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            # Wait for the tunnel URL to be printed
            tunnel_url = None
            for _ in range(30):  # timeout after 30 seconds
                if process.poll() is not None:
                    self.print_message("Cloudflared process terminated unexpectedly", "error")
                    break
                    
                line = process.stdout.readline().strip()
                if line:
                    # Only print detailed output if verbose mode is enabled
                    if self.parser.parse_args().verbose:
                        print(line)
                    # Extract URL regardless of verbose mode
                    match = re.search(r"https://.*?\.trycloudflare\.com", line)
                    if match:
                        tunnel_url = match.group(0)
                        break
                time.sleep(1)
                
            if tunnel_url:
                print()  # Add space above URL
                self.print_message(f"Temporary tunnel URL: {YELLOW}{tunnel_url}{RESET}")
                print("\nTunnel is now active. Press Ctrl+C to stop.\n")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    self.print_message("Stopping tunnel...")
                    process.terminate()
                    process.wait()
            else:
                self.print_message("Failed to obtain tunnel URL", "error")
        finally:
            # Clean up the temporary config file
            try:
                os.unlink(temp_config_path)
            except OSError:
                pass  # Ignore if file doesn't exist

    def list_cloudflare_domains(self) -> None:
        """List domains registered in the Cloudflare account"""
        token = os.environ.get("CLOUDFLARE_API_TOKEN")
        if not token:
            self.print_message("CLOUDFLARE_API_TOKEN environment variable not set.", "error")
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get("https://api.cloudflare.com/client/v4/zones", headers=headers)

        if response.status_code != 200:
            self.print_message("Failed to fetch domains from Cloudflare.", "error")
            print(response.text)
            return

        zones = response.json().get("result", [])
        self.print_message("Domains under your Cloudflare account:")
        for zone in zones:
            print(f" - {zone['name']}")

    def pull_model(self, model_name: str) -> None:
        """Pull a specific model from Ollama's model hub"""
        try:
            model_name = self.sanitize_model_name(model_name)
        except ValueError as e:
            self.print_message(str(e), "error")
            return
            
        self.print_message(f"Pulling model: {model_name}...")
        
        # Ensure Ollama is running before pulling
        if not self.is_ollama_running():
            self.start_ollama()
            # Wait for Ollama to initialize
            time.sleep(3)
        
        # Pull the model
        process = subprocess.Popen(
            ["ollama", "pull", model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Track progress without showing repeating "pulling manifest" messages
        last_message = ""
        manifest_count = 0
        
        for line in process.stdout:
            line = line.strip()
            
            # Handle repetitive "pulling manifest" messages
            if line == "pulling manifest":
                manifest_count += 1
                if manifest_count == 1:
                    print(f"Pulling manifest{'.' * min(manifest_count, 3)}", end="\r")
                elif manifest_count % 5 == 0:  # Update progress dots every 5 iterations
                    print(f"Pulling manifest{'.' * min(manifest_count//5, 10)}", end="\r")
                continue
            
            # For non-manifest messages, print normally if they're not repeats
            if line != last_message and line:
                if manifest_count > 0:
                    print()  # End the previous line if we were showing manifest progress
                    manifest_count = 0
                print(line)
                last_message = line
        
        # Ensure we end with a newline
        if manifest_count > 0:
            print()
        
        # Wait for the process to complete
        exit_code = process.wait()
        if exit_code == 0:
            self.print_message(f"Successfully pulled model: {model_name}")
        else:
            self.print_message(f"Failed to pull model: {model_name}", "error")

    def run_model(self, model_name: str) -> None:
        """Run a specific model in interactive mode"""
        try:
            model_name = self.sanitize_model_name(model_name)
        except ValueError as e:
            self.print_message(str(e), "error")
            return
            
        self.print_message(f"Running model: {model_name}...")
        
        # Ensure Ollama is running
        if not self.is_ollama_running():
            self.start_ollama()
            # Wait for Ollama to initialize
            time.sleep(3)
        
        # Run the model in interactive mode
        try:
            subprocess.run(["ollama", "run", model_name], check=True)
        except subprocess.CalledProcessError:
            self.print_message(f"Error running model: {model_name}", "error")

    def list_models(self) -> None:
        """List all available models on the local Ollama instance"""
        # Ensure Ollama is running
        if not self.is_ollama_running():
            self.start_ollama()
            # Wait for Ollama to initialize
            time.sleep(3)
        
        try:
            result = subprocess.run(
                ["ollama", "list"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            print("\nAvailable models on your Ollama instance:")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            self.print_message(f"Error listing models: {e.stderr}", "error")
    
    def get_installed_models(self) -> List[str]:
        """Return a list of installed model names"""
        # Ensure Ollama is running
        if not self.is_ollama_running():
            self.start_ollama()
            # Wait for Ollama to initialize
            time.sleep(3)
        
        try:
            result = subprocess.run(
                ["ollama", "list"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            
            models = []
            # Skip the header line and extract model names
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:  # There's at least one model
                for line in lines[1:]:  # Skip header
                    parts = line.split()
                    if parts:  # Non-empty line with parts
                        models.append(parts[0])
            
            return models
        except subprocess.CalledProcessError:
            return []
            
    def ensure_default_model(self) -> None:
        """Check if any models are installed, pull the default if none"""
        models = self.get_installed_models()
        
        if not models:
            self.print_message(f"No models found. Pulling default model ({DEFAULT_MODEL})...")
            self.pull_model(DEFAULT_MODEL)
        else:
            self.print_message(f"Found {len(models)} installed models: {', '.join(models)}")

    def prompt_for_confirmation(self, message: str) -> bool:
        """Prompt user for confirmation"""
        response = input(f"{YELLOW}[?]{RESET} {message} [Y/n]: ").strip().lower()
        return response in ("", "y", "yes")

    def run(self) -> None:
        """Main execution function"""
        args = self.parser.parse_args()
        
        # Handle special commands first
        if args.list_domains:
            self.list_cloudflare_domains()
            return
            
        if args.check:
            self.print_message(f"Ollama installed: {self.is_installed('ollama')}")
            self.print_message(f"cloudflared installed: {self.is_installed('cloudflared')}")
            self.print_message(f"Ollama running: {self.is_ollama_running()}")
            return
            
        if args.list_models:
            self.list_models()
            return
            
        # Handle model-specific commands
        if args.pull:
            # Install Ollama if needed
            if not self.is_installed("ollama"):
                if args.yes or self.prompt_for_confirmation("Ollama not found. Install it?"):
                    self.install_ollama()
                else:
                    self.print_message("Skipping Ollama installation.", "warn")
                    return
            self.pull_model(args.pull)
            return
            
        if args.run:
            # Install Ollama if needed
            if not self.is_installed("ollama"):
                if args.yes or self.prompt_for_confirmation("Ollama not found. Install it?"):
                    self.install_ollama()
                else:
                    self.print_message("Skipping Ollama installation.", "warn")
                    return
            
            # Make sure we have at least one model before running
            models = self.get_installed_models()
            if not models:
                self.print_message(f"No models found. Pulling {args.run} first...")
                self.pull_model(args.run)
            elif args.run not in models:
                self.print_message(f"Model {args.run} not found. Pulling it first...")
                self.pull_model(args.run)
                
            self.run_model(args.run)
            return
            
        # Default behavior: setup and start tunnel
        auto_run = True
        
        if auto_run:
            # Install Ollama if needed
            if not self.is_installed("ollama"):
                if args.yes or self.prompt_for_confirmation("Ollama not found. Install it?"):
                    self.install_ollama()
                else:
                    self.print_message("Skipping Ollama installation.", "warn")
                    return
            else:
                self.print_message("Ollama already installed.")

            # Install cloudflared if needed
            if not self.is_installed("cloudflared"):
                if args.yes or self.prompt_for_confirmation("cloudflared not found. Install it?"):
                    self.install_cloudflared()
                else:
                    self.print_message("Skipping cloudflared installation.", "warn")
                    return
            else:
                self.print_message("cloudflared already installed.")

            # Start Ollama if not running
            if not self.is_ollama_running():
                self.start_ollama()
            else:
                self.print_message("Ollama already running.")
                
            # Check if any models are installed
            self.ensure_default_model()

            # Start tunnel
            self.start_temp_tunnel()


if __name__ == "__main__":
    try:
        setup = OllamaSetup()
        setup.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"{RED}[!]{RESET} An error occurred: {e}")
        sys.exit(1)
