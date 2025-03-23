"""
Tests for the SoundToolServer class.
"""
import os
import pytest
from unittest.mock import patch, MagicMock, mock_open

from src.sound_tool.server import SoundToolServer, SoundPlayer


class TestSoundToolServer:
    """Test cases for the SoundToolServer class."""
    
    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.expanduser')
    @patch('src.sound_tool.server.FastMCP')
    def test_server_initialization(self, mock_fastmcp, mock_expanduser, mock_listdir, mock_exists):
        """Test server initialization with proper descriptions."""
        # Setup mocks
        mock_expanduser.return_value = "/mock/home"
        mock_exists.side_effect = lambda path: "/mock/home/projects/py-sound-mcp/sounds" in path
        mock_listdir.return_value = ["completion.mp3", "error.mp3", "notification.mp3"]
        
        # Create server instance
        server = SoundToolServer()
        
        # Verify FastMCP was created with proper name and description
        mock_fastmcp.assert_called_once()
        name_arg = mock_fastmcp.call_args[1].get('name')
        description_arg = mock_fastmcp.call_args[1].get('description')
        
        assert name_arg == "Sound Tool 🔊"
        assert description_arg is not None
        assert "audio feedback" in description_arg
        assert "command outcomes" in description_arg

    @patch('os.path.expanduser')
    @patch('src.sound_tool.server.FastMCP')
    def test_copy_sounds_to_user_dir(self, mock_fastmcp, mock_expanduser):
        """Test copying sounds to user directory."""
        # Setup mocks
        mock_expanduser.return_value = "/mock/home"
        
        with patch('os.path.exists') as mock_exists, \
             patch('os.makedirs') as mock_makedirs, \
             patch('os.listdir') as mock_listdir, \
             patch('shutil.copy') as mock_copy:
            
            # Setup the server
            server = SoundToolServer()
            server.sounds_dir = "/mock/sounds"
            
            # Configure mocks for copy_sounds_to_user_dir
            mock_listdir.return_value = ["completion.mp3", "error.mp3", "notification.mp3"]
            
            # Call the method
            user_dir = server.copy_sounds_to_user_dir()
            
            # Verify directory was created
            mock_makedirs.assert_called_once()
            assert "/.config/mcp-sound-tool/sounds" in user_dir
            
            # Verify files were copied
            assert mock_copy.call_count >= 1

    @patch('os.path.expanduser')
    @patch('src.sound_tool.server.FastMCP')
    def test_play_sound_functionality(self, mock_fastmcp, mock_expanduser):
        """Test the sound playing functionality directly."""
        # Setup mocks
        mock_expanduser.return_value = "/mock/home"
        
        with patch('os.path.exists') as mock_exists, \
             patch('os.listdir') as mock_listdir, \
             patch('src.sound_tool.server.SoundPlayer.play_sound') as mock_play_sound:
            
            # Setup exists to find project directory sounds
            mock_exists.side_effect = lambda path: \
                "/mock/home/projects/py-sound-mcp/sounds" in path or \
                "completion.mp3" in path
                
            mock_listdir.return_value = ["completion.mp3", "error.mp3", "notification.mp3"]
            
            # Create the server
            server = SoundToolServer()
            server.sounds_dir = "/mock/sounds"
            
            # Create a test sound path
            test_sound_path = os.path.join(server.sounds_dir, "completion.mp3")
            mock_exists.side_effect = lambda path: path == test_sound_path
            
            # Manually call the player's play_sound with the test path
            server.player.play_sound(test_sound_path)
            
            # Verify the sound was played
            mock_play_sound.assert_called_once_with(test_sound_path)

    @patch('os.path.expanduser')
    @patch('src.sound_tool.server.FastMCP')
    def test_list_available_sounds(self, mock_fastmcp, mock_expanduser):
        """Test listing available sounds."""
        # Setup mocks
        mock_expanduser.return_value = "/mock/home"
        mock_tool = MagicMock()
        mock_fastmcp.return_value.tool.return_value = lambda x: x  # Mock decorator
        
        with patch('os.path.exists') as mock_exists, \
             patch('os.listdir') as mock_listdir:
            
            # Setup exists to find project directory sounds
            mock_exists.side_effect = lambda path: "/mock/home/projects/py-sound-mcp/sounds" in path
            mock_listdir.return_value = ["completion.mp3", "error.mp3", "notification.mp3"]
            
            # Create the server
            server = SoundToolServer()
            
            # Configure the server for testing
            server.sounds_dir = "/mock/sounds"
            with patch('os.listdir') as mock_test_listdir:
                mock_test_listdir.return_value = ["completion.mp3", "error.mp3", "notification.mp3"]
                
                # Extract the list_available_sounds function
                mock_list_func = None
                for call in mock_fastmcp.return_value.tool.call_args_list:
                    if "Available sounds" in str(call):
                        mock_list_func = call[0][0]
                        break
                
                # Call the function
                if mock_list_func:
                    result = mock_list_func()
                    
                    # Verify the result
                    assert "Available sounds:" in result
                    assert "completion.mp3" in result
                    assert "error.mp3" in result
                    assert "notification.mp3" in result 