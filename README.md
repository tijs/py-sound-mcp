# MCP Sound Tool

A Model Context Protocol (MCP) implementation that plays sound effects for Cursor AI and other MCP-compatible environments. This Python implementation provides audio feedback for a more interactive coding experience.

## Features

* Plays sound effects for various events (completion, error, notification)
* Uses the Model Context Protocol (MCP) for standardized integration with Cursor and other IDEs
* Cross-platform support (Windows, macOS, Linux)
* Configurable sound effects

## Installation

### From PyPI

```bash
pip install mcp-sound-tool
```

### From Source

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/mcp-sound-tool
   cd mcp-sound-tool
   ```

2. Install dependencies:

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

## Development

For development:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
