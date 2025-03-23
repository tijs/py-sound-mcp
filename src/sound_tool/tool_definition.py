"""
Model Context Protocol (MCP) tool definitions for sound-tool

This file defines the schema and usage guidance for sound playing tools
that can be called by AI agents
"""

play_sound_tool_definition = {
    "name": "play_sound",
    "description": """
    Play a notification sound on the user's device.
    
    Use this tool to provide audio feedback to the user:
    - Use 'completion' when a task or command has successfully completed
    - Use 'error' when an error or failure has occurred
    - Use 'notification' for important information or alerts
    - Use 'custom' when you need to play a specific sound file
    
    AI agents should proactively use these sounds to improve user experience by
    providing audio cues for important events.
    """,
    "parameters": {
        "type": "object",
        "properties": {
            "sound_type": {
                "type": "string",
                "enum": ["completion", "error", "notification", "custom"],
                "description": "The type of sound to play. Default is 'completion'."
            },
            "custom_sound_path": {
                "type": "string",
                "description": "Path to a custom sound file (only used if sound_type is 'custom')."
            }
        },
        "required": []
    },
    "returns": {
        "type": "string",
        "description": "A message indicating the result of the operation"
    }
}

list_sounds_tool_definition = {
    "name": "list_available_sounds",
    "description": """
    List all available notification sounds.
    
    Use this tool when you need to check what sound options are available to play.
    This is helpful when determining what custom sounds might be available.
    """,
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    },
    "returns": {
        "type": "string",
        "description": "A string listing all available sound files"
    }
}

install_tool_definition = {
    "name": "install_to_user_dir",
    "description": """
    Install sound files to user's config directory.
    
    This tool should be used when the user wants to install the default sound files
    to their config directory for customization.
    """,
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    },
    "returns": {
        "type": "string",
        "description": "A message indicating the result of the operation"
    }
} 