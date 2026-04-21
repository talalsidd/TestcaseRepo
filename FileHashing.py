import unittest
import os
import shutil
import subprocess
from pathlib import Path

class TestAutomationScript(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Runs once before all tests. 
        Handles environment configuration and directory setup.
        """
        # --- 1. Credentials & Configuration ---
        cls.username = "YourUsername"
        cls.password = "YourPassword"
        cls.exe_path = r"C:\Program Files\Windows Event Reporting"
        cls.exe_name = "ConfigurationCmd.exe"
        
        # Desktop Paths
        cls.desktop_path = Path(os.environ["USERPROFILE"]) / "Desktop"
        cls.folder_name = "TempAutomationFolder"
        cls.full_folder_path = cls.desktop_path / cls.folder_name
        cls.file_name = "DataFile.txt"
        cls.new_file_name = "RenamedDataFile.txt"

        # --- 2. Execute Configuration (Formerly Step 1) ---
        if not os.path.exists(cls.exe_path):
            raise unittest.SkipTest(f"Directory not found: {cls.exe_path}")

        full_cmd_path = os.path.join(cls.exe_path, cls.exe_name)

        # Helper to run commands and check for errors
        def run_config(attr, value):
            cmd = [full_cmd_path, "-a", cls.username, "-p", cls.password, "-set", attr, value]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Configuration failed for {attr}: {result.stderr}")

        run_config("fileHashingType", "1")
        run_config("fileHashingScopeFlags", "15")

        # --- 3. Create Folder (Formerly Step 2) ---
        if cls.full_folder_path.exists():
            shutil.rmtree(cls.full_folder_path)
            
        os.makedirs(cls.full_folder_path, exist_ok=True)
        
        # Verify setup success
        if not cls.full_folder_path.is_dir():
            raise Exception("Failed to create the automation directory during setup.")

    def test_step_3_create_and_write_file(self):
        """Now the test only focuses on file operations."""
        file_path = self.full_folder_path / self.file_name
        content = "This is the initial content of the file."
        
        file_path.write_text(content)
        self.assertTrue(file_path.exists())
        self.assertEqual(file_path.read_text(), content)

    def test_step_4_rename_file(self):
        old_path = self.full_folder_path / self.file_name
        new_path = self.full_folder_path / self.new_file_name
        
        # Ensure the file exists from the previous step 
        # (Note: In strict unit testing, steps should be independent, 
        # but in functional scripts, they often follow a sequence).
        if not old_path.exists():
            old_path.write_text("Default content")

        os.rename(old_path, new_path)
        self.assertTrue(new_path.exists())

    @classmethod
    def tearDownClass(cls):
        """Cleanup after all tests have finished."""
        if cls.full_folder_path.exists():
            shutil.rmtree(cls.full_folder_path)

if __name__ == "__main__":
    unittest.main()