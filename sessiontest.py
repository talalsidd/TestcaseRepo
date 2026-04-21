import unittest
import winrm
import time

class TestRemoteAutomation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Sets up the WinRM session and prepares the remote environment."""
        # --- 1. Connection Details ---
        cls.host = 'qa-w1124h2-3.eng.dtexsystems.com'
        cls.username = r'dtexsystems\talal.siddiqui'
        cls.password = 'Ayeshafatima@2021'
        
        # --- 2. Configuration Constants ---
        cls.exe_path = r"C:\Program Files\Windows Event Reporting"
        cls.desktop_path = r"C:\Users\talal.siddiqui\Desktop"
        cls.folder_path = rf"{cls.desktop_path}\TempAutomationFolder"
        cls.file_path = rf"{cls.folder_path}\DataFile.txt"
        cls.new_file_path = rf"{cls.folder_path}\RenamedDataFile.txt"

        # Establish WinRM Session
        try:
            cls.session = winrm.Session(cls.host, auth=(cls.username, cls.password), transport='ntlm')
            # Test connection with a simple 'whoami'
            cls.run_remote_cmd("whoami")
        except Exception as e:
            raise unittest.SkipTest(f"Failed to establish WinRM session: {e}")

        # --- 3. Execute Remote Configuration ---
        # Note: We use 'cd' command within the same string or provide full path
        config_cmd = (
            f'cd "{cls.exe_path}" && '
            f'ConfigurationCmd.exe -a "{cls.username}" -p "{cls.password}" -set fileHashingType 1 && '
            f'ConfigurationCmd.exe -a "{cls.username}" -p "{cls.password}" -set fileHashingScopeFlags 15'
        )
        
        result = cls.run_remote_cmd(config_cmd)
        if result.status_code != 0:
            raise Exception(f"Remote configuration failed: {result.std_err}")

        # --- 4. Create Remote Folder ---
        # Using PowerShell via WinRM for easier folder management
        cls.session.run_ps(f'if (Test-Path "{cls.folder_path}") {{ Remove-Item "{cls.folder_path}" -Recurse -Force }}')
        cls.session.run_ps(f'New-Item -Path "{cls.folder_path}" -ItemType Directory')

    @classmethod
    def run_remote_cmd(cls, command):
        """Helper to run CMD commands on the remote host."""
        return cls.session.run_cmd(command)

    def test_step_1_create_remote_file(self):
        """Creates a file on the remote desktop."""
        content = "This is the initial content of the file."
        # Use PowerShell to set content remotely
        ps_cmd = f'Set-Content -Path "{self.file_path}" -Value "{content}"'
        result = self.session.run_ps(ps_cmd)
        
        self.assertEqual(result.status_code, 0, "Failed to create remote file.")

    def test_step_2_rename_remote_file(self):
        """Renames the file on the remote desktop."""
        ps_cmd = f'Rename-Item -Path "{self.file_path}" -NewName "RenamedDataFile.txt"'
        result = self.session.run_ps(ps_cmd)
        
        self.assertEqual(result.status_code, 0, "Failed to rename remote file.")

    @classmethod
    def tearDownClass(cls):
        """Cleanup: Remove the remote folder after tests."""
        time.sleep(2) # Brief pause to mimic original script
        cls.session.run_ps(f'Remove-Item -Path "{cls.folder_path}" -Recurse -Force')

if __name__ == "__main__":
    unittest.main()