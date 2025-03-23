"""
Tests for the SoundPlayer class.
"""
import os
import platform
import subprocess
import pytest
from unittest.mock import patch, MagicMock

# Import the SoundPlayer class
from src.sound_tool.server import SoundPlayer


class TestSoundPlayer:
    """Test cases for the SoundPlayer class."""

    def test_play_sound_file_not_found(self, capfd):
        """Test behavior when sound file is not found."""
        # Call with non-existent file
        SoundPlayer.play_sound("nonexistent_file.mp3")
        
        # Capture output and check error message
        out, _ = capfd.readouterr()
        assert "Error: Sound file not found" in out

    @patch('os.path.exists')
    @patch('platform.system')
    @patch('subprocess.run')
    def test_play_sound_macos(self, mock_run, mock_system, mock_exists):
        """Test playing sound on macOS."""
        # Mock platform as macOS
        mock_system.return_value = "Darwin"
        mock_exists.return_value = True
        
        # Call play_sound
        SoundPlayer.play_sound("test.mp3")
        
        # Verify afplay was called with correct arguments
        mock_run.assert_called_once_with(["afplay", "test.mp3"], check=True)

    @patch('os.path.exists')
    @patch('platform.system')
    def test_play_sound_windows(self, mock_system, mock_exists):
        """Test playing sound on Windows."""
        # Mock platform as Windows
        mock_system.return_value = "Windows"
        mock_exists.return_value = True
        
        # Mock winsound module
        with patch.dict('sys.modules', {'winsound': MagicMock()}):
            import sys
            winsound_mock = sys.modules['winsound']
            
            # Call play_sound
            SoundPlayer.play_sound("test.mp3")
            
            # Verify PlaySound was called with correct arguments
            winsound_mock.PlaySound.assert_called_once_with("test.mp3", winsound_mock.SND_FILENAME)

    @patch('os.path.exists')
    @patch('platform.system')
    @patch('subprocess.run')
    def test_play_sound_linux_first_player(self, mock_run, mock_system, mock_exists):
        """Test playing sound on Linux with first player available."""
        # Mock platform as Linux
        mock_system.return_value = "Linux"
        mock_exists.return_value = True
        
        # Make first player (paplay) succeed
        mock_run.side_effect = [None, subprocess.SubprocessError]
        
        # Call play_sound
        SoundPlayer.play_sound("test.mp3")
        
        # Verify paplay was called
        mock_run.assert_called_once_with(["paplay", "test.mp3"], check=True)

    @patch('os.path.exists')
    @patch('platform.system')
    @patch('subprocess.run')
    def test_play_sound_linux_fallback(self, mock_run, mock_system, mock_exists):
        """Test playing sound on Linux with fallback to second player."""
        # Mock platform as Linux
        mock_system.return_value = "Linux"
        mock_exists.return_value = True
        
        # Make first player fail, second succeed
        mock_run.side_effect = [subprocess.SubprocessError, None]
        
        # Call play_sound
        SoundPlayer.play_sound("test.mp3")
        
        # Verify both players were tried in order
        assert mock_run.call_count == 2
        mock_run.assert_any_call(["paplay", "test.mp3"], check=True)
        mock_run.assert_any_call(["aplay", "test.mp3"], check=True)

    @patch('os.path.exists')
    @patch('platform.system')
    @patch('subprocess.run')
    def test_play_sound_error(self, mock_run, mock_system, mock_exists, capfd):
        """Test error handling when playing sound."""
        # Mock platform as macOS
        mock_system.return_value = "Darwin"
        mock_exists.return_value = True
        
        # Make subprocess.run raise an exception
        mock_run.side_effect = Exception("Test error")
        
        # Call play_sound
        SoundPlayer.play_sound("test.mp3")
        
        # Verify error message was printed
        out, _ = capfd.readouterr()
        assert "Error playing sound: Test error" in out 