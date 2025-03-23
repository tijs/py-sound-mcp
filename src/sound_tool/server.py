from mcp.server.fastmcp import FastMCP
import os
import platform
import subprocess
import time
import shutil
from typing import Optional, Literal
from importlib import resources
import importlib.resources as pkg_resources


class SoundPlayer:
    """Class to handle sound playback on different platforms."""
    
    @staticmethod
    def play_sound(sound_file: str) -> None:
        """Play a sound file using the appropriate method for the current platform."""
        if not os.path.exists(sound_file):
            print(f"Error: Sound file not found: {sound_file}")
            return
        
        system = platform.system()
        
        try:
            if system == "Darwin":  # macOS
                subprocess.run(["afplay", sound_file], check=True)
            elif system == "Windows":
                import winsound
                winsound.PlaySound(sound_file, winsound.SND_FILENAME)
            elif system == "Linux":
                # Try different players until one works
                for player in ["paplay", "aplay", "mpg123", "mpg321"]:
                    try:
                        subprocess.run([player, sound_file], check=True)
                        break
                    except (subprocess.SubprocessError, FileNotFoundError):
                        continue
                else:
                    print("Error: Could not find a suitable audio player on Linux")
        except Exception as e:
            print(f"Error playing sound: {e}")


class SoundToolServer:
    """MCP server for playing sounds in response to model events."""
    
    def __init__(self):
        """Initialize the MCP server with sound capabilities."""
        # Initialize the MCP server with more detailed name and description
        self.mcp = FastMCP(
            name="Sound Tool 🔊", 
            description="""
            This MCP server provides audio feedback capabilities for AI interactions.
            
            IMPORTANT USAGE GUIDELINES:
            - AI agents should play sounds to provide audio feedback based on command outcomes
            - Use 'completion' sounds when successfully completing a task or command
            - Use 'error' sounds when a command fails or an error occurs
            - Use 'notification' sounds for important alerts or information
            
            These sounds enhance the user experience by providing clear audio cues
            about the status of operations without requiring the user to read text.
            """
        )
        
        # Try several sound locations in order:
        # 1. User config directory
        # 2. Package data
        # 3. The original project location
        user_sounds_dir = os.path.join(os.path.expanduser("~"), ".config", "mcp-sound-tool", "sounds")
        project_sounds_dir = os.path.join(os.path.expanduser("~"), "projects", "py-sound-mcp", "sounds")
        
        if os.path.exists(user_sounds_dir) and any(f.endswith(('.mp3', '.wav')) for f in os.listdir(user_sounds_dir)):
            # Use user's custom sounds
            self.sounds_dir = user_sounds_dir
            print(f"Using sounds from user config directory: {user_sounds_dir}")
        elif os.path.exists(project_sounds_dir) and any(f.endswith(('.mp3', '.wav')) for f in os.listdir(project_sounds_dir)):
            # Use the project's sounds
            self.sounds_dir = project_sounds_dir
            print(f"Using sounds from project directory: {project_sounds_dir}")
        else:
            # Use package data
            try:
                # For Python 3.9+
                self.sounds_dir = str(resources.files("sound_tool").joinpath("sounds"))
                print(f"Using sounds from package resources: {self.sounds_dir}")
            except (AttributeError, ImportError):
                # For older Python versions
                self.sounds_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")
                print(f"Using sounds from package directory: {self.sounds_dir}")
                
        self.player = SoundPlayer()
        
        # Log available sounds for reference
        try:
            sounds = [f for f in os.listdir(self.sounds_dir) if f.endswith(('.mp3', '.wav'))]
            print(f"Available sounds: {', '.join(sounds)}")
        except Exception:
            pass
            
        # Register tools
        self.register_tools()
        
        # Print initialization message
        print(f"Sound Tool MCP server initialized - use sounds to provide audio feedback on command outcomes")

    def copy_sounds_to_user_dir(self):
        """Copy bundled sounds to user config directory."""
        user_sounds_dir = os.path.join(os.path.expanduser("~"), ".config", "mcp-sound-tool", "sounds")
        os.makedirs(user_sounds_dir, exist_ok=True)
        
        # Get list of sound files
        try:
            # Try with Python 3.9+ method
            sound_files = resources.files("sound_tool").joinpath("sounds").iterdir()
            for sound_file in sound_files:
                if sound_file.name.endswith((".mp3", ".wav")):
                    shutil.copy(sound_file, os.path.join(user_sounds_dir, sound_file.name))
        except (AttributeError, ImportError):
            # Fallback for older Python
            sounds_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")
            if os.path.exists(sounds_dir):
                for sound_file in os.listdir(sounds_dir):
                    if sound_file.endswith((".mp3", ".wav")):
                        shutil.copy(
                            os.path.join(sounds_dir, sound_file), 
                            os.path.join(user_sounds_dir, sound_file)
                        )
        
        return user_sounds_dir
        
    def register_tools(self):
        """Register all MCP tools."""
        @self.mcp.tool(description="""
        Play a notification sound on the user's device.
        
        WHEN TO USE THIS TOOL:
        - Use 'completion' sound when a task or command has SUCCESSFULLY completed
        - Use 'error' sound when a command has FAILED or an error has occurred
        - Use 'notification' sound for important alerts or information that needs attention
        - Use 'custom' sound only when you need a specific sound not covered by the standard types
        
        AI agents SHOULD proactively use these sounds to provide audio feedback based on
        the outcome of commands or operations, enhancing the user experience with
        non-visual status indicators.
        
        Example usage: After executing a terminal command, play a 'completion' sound if 
        successful or an 'error' sound if it failed.
        """)
        def play_sound(sound_type: Literal["completion", "error", "notification", "custom"] = "completion",
                   custom_sound_path: Optional[str] = None) -> str:
            if sound_type == "custom" and custom_sound_path:
                sound_path = custom_sound_path
            else:
                # Try MP3 file first, then WAV if MP3 doesn't exist
                mp3_filename = f"{sound_type}.mp3"
                wav_filename = f"{sound_type}.wav"
                mp3_path = os.path.join(self.sounds_dir, mp3_filename)
                wav_path = os.path.join(self.sounds_dir, wav_filename)
                
                # Check which file exists
                if os.path.exists(mp3_path):
                    sound_path = mp3_path
                elif os.path.exists(wav_path):
                    sound_path = wav_path
                else:
                    # Print debug information
                    print(f"Sounds directory: {self.sounds_dir}")
                    print(f"Sound files available: {os.listdir(self.sounds_dir)}")
                    return f"Error: Sound files not found: {mp3_path} or {wav_path}"
            
            # Play the sound
            try:
                self.player.play_sound(sound_path)
                return f"Successfully played {sound_type} sound"
            except Exception as e:
                return f"Error playing sound: {e}"
        
        @self.mcp.tool(description="""
        List all available notification sounds.
        
        WHEN TO USE THIS TOOL:
        - When you need to check what sound options are available
        - When determining if a specific sound file exists
        - Before using a custom sound to verify available options
        
        This tool helps you discover what sounds are available for providing audio feedback.
        """)
        def list_available_sounds() -> str:
            try:
                sounds = [f for f in os.listdir(self.sounds_dir) if f.endswith(('.mp3', '.wav'))]
                if sounds:
                    return "Available sounds:\n" + "\n".join(sounds)
                else:
                    return "No sound files found in the sounds directory."
            except Exception as e:
                return f"Error listing sounds: {e}"

        @self.mcp.tool(description="""
        Install sound files to user's config directory.
        
        WHEN TO USE THIS TOOL:
        - When the user wants to customize the sound files
        - When setting up the sound tool for the first time
        - When troubleshooting missing sound files
        
        This tool copies the default sound files to the user's configuration directory
        where they can be modified or replaced with custom sounds.
        """)
        def install_to_user_dir() -> str:
            try:
                user_dir = self.copy_sounds_to_user_dir()
                return f"Sound files installed to {user_dir}"
            except Exception as e:
                return f"Error installing sound files: {e}"


def main():
    """Main entry point for the sound tool server."""
    server = SoundToolServer()
    # Start the server and block until it's terminated
    print("Starting Sound Tool MCP server - press Ctrl+C to exit")
    try:
        server.mcp.run()
    except KeyboardInterrupt:
        print("\nShutting down Sound Tool MCP server...")
    except Exception as e:
        if "BrokenResourceError" in str(e) or "unhandled errors in a TaskGroup" in str(e):
            print("\nConnection closed. Shutting down Sound Tool MCP server...")
        else:
            print(f"\nError in Sound Tool MCP server: {e}")
    print("Sound Tool MCP server stopped.")


if __name__ == "__main__":
    main() 