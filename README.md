# MCP Sound Tool

A Model Context Protocol (MCP) implementation that plays sound effects for Cursor AI and other MCP-compatible environments. This Python implementation provides audio feedback for a more interactive coding experience.

## Features

* Plays sound effects for various events (completion, error, notification)
* Uses the Model Context Protocol (MCP) for standardized integration with Cursor and other IDEs
* Cross-platform support (Windows, macOS, Linux)
* Configurable sound effects

## Installation

### Python Version Compatibility

This package is tested with Python 3.8-3.11. If you encounter errors with Python 3.12+ (particularly `BrokenResourceError` or `TaskGroup` exceptions), please try using an earlier Python version.

### Recommended: Install with pipx

The recommended way to install mcp-sound-tool is with [pipx](https://pypa.github.io/pipx/), which installs the package in an isolated environment while making the commands available globally:

```bash
# Install pipx if you don't have it
python -m pip install --user pipx
python -m pipx ensurepath

# Install mcp-sound-tool
pipx install mcp-sound-tool
```

This method ensures that the tool has its own isolated environment, avoiding conflicts with other packages.

### Alternative: Install with pip

You can also install directly with pip:

```bash
pip install mcp-sound-tool
```

### From Source

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/mcp-sound-tool
   cd mcp-sound-tool
   ```

2. Install with pipx directly from the source directory:

   ```bash
   pipx install .
   ```

   Or with pip:

   ```bash
   pip install -e .
   ```

## Usage

### Adding Sound Files

Place your sound files in the `sounds` directory. The following sound files are expected:

* `completion.mp3` - Played after code generation
* `error.mp3` - Played when an error occurs
* `notification.mp3` - Used for general notifications

You can find free sound effects on websites like freesound.org.

### Running the MCP Server

Run the MCP server:

```bash
mcp-sound-tool
```

The server will start and listen for events from Cursor or other MCP-compatible clients through the stdio transport.

### Configuration in Cursor

To use this server with Cursor, add it to your MCP configuration file:

On macOS:

```json
// ~/Library/Application Support/Cursor/mcp.json
{
  "mcpServers": {
    "sound": {
      "command": "mcp-sound-tool",
      "args": [],
      "type": "stdio",
      "pollingInterval": 5000,
      "startupTimeout": 10000,
      "restartOnFailure": true
    }
  }
}
```

On Windows:

```json
// %APPDATA%/Cursor/mcp.json
{
  "mcpServers": {
    "sound": {
      "command": "mcp-sound-tool",
      "args": [],
      "type": "stdio",
      "pollingInterval": 5000,
      "startupTimeout": 10000,
      "restartOnFailure": true
    }
  }
}
```

When installed with `pipx`, the `mcp-sound-tool` command will be available in your PATH, so Cursor will be able to find and execute it without specifying the full path.

## Sound MCP Usage Guidelines for AI Models

This MCP server provides audio feedback capabilities for AI interactions. It's designed to enhance the user experience by providing clear audio cues that indicate the status of operations without requiring the user to read text.

### When to Use Sound Feedback

AI agents should use the sound tools proactively at appropriate moments:

1. **Success Sounds (`completion`)**:
   * After a task or command has successfully completed
   * When a significant operation has finished successfully
   * When confirming a user's request has been fulfilled

2. **Error Sounds (`error`)**:
   * When a command has failed or encountered an error
   * When warning the user about a problem
   * When an operation couldn't be completed as requested

3. **Notification Sounds (`notification`)**:
   * When alerting the user to important information
   * When prompting for user attention or input
   * For status updates on long-running operations

### Example Usage

```python
# When a command completes successfully
@mcp.tool()
def execute_command(command):
    result = run_command(command)
    if result.success:
        play_sound("completion")  # Indicate success with audio
        return "Command executed successfully"
    else:
        play_sound("error")  # Indicate failure with audio
        return f"Error: {result.error_message}"
```

### Available Tools

1. `play_sound(sound_type="completion", custom_sound_path=None)`: Play a sound effect
2. `list_available_sounds()`: List all available sound files
3. `install_to_user_dir()`: Install sound files to user's config directory

For more details, connect to the MCP server and check the tool descriptions.

## Development

For development:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Acknowledgments

* [SIAM-TheLegend](https://github.com/SIAM-TheLegend) for creating the original [sound-mcp](https://github.com/SIAM-TheLegend/sound-mcp) JavaScript implementation that inspired this Python version
* The MCP protocol developers for creating a powerful standard for AI tool interactions
* Contributors to the testing and documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.
