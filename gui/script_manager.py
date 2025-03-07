# Copyright (C) 2024 Bellande Application Interoperability Xenogen Research Innovation Center, Ronaldson Bellande

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from header_imports import *

class ScriptManager:
    def __init__(self):
        self.active_processes: Dict[int, subprocess.Popen] = {}
        self.script_history: List[str] = []
        self.settings = self.load_settings()

    def load_settings(self) -> dict:
        settings_file = "bellos_settings.json"
        default_settings = {
            "default_shell": "bellos",
            "default_timeout": 30,
            "script_extension": ".bellos"
        }
        
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return default_settings
        return default_settings

    def run_script(self, script_content: str, timeout: Optional[int] = None) -> str:
        if timeout is None:
            timeout = self.settings.get("default_timeout", 30)

        # Create a temporary script file
        script_file = f"temp_script{self.settings.get('script_extension', '.bellos')}"
        try:
            with open(script_file, 'w') as f:
                f.write(script_content)

            # Make the script executable
            os.chmod(script_file, 0o755)

            # Run the script with the specified shell
            shell = self.settings.get("default_shell", "bellos")
            process = subprocess.Popen(
                [shell, script_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            self.active_processes[process.pid] = process

            # Set up timeout handling
            timer = threading.Timer(timeout, self.kill_process, args=[process.pid])
            timer.start()

            try:
                stdout, stderr = process.communicate()
                timer.cancel()  # Cancel the timeout if process completes normally
            except subprocess.TimeoutExpired:
                return f"Script execution timed out after {timeout} seconds"

            if process.pid in self.active_processes:
                del self.active_processes[process.pid]

            # Add to history
            self.script_history.append(script_content)

            # Return combined output
            output = stdout
            if stderr:
                output += f"\nErrors:\n{stderr}"
            return output

        finally:
            # Clean up temporary script file
            if os.path.exists(script_file):
                os.remove(script_file)

    def kill_process(self, pid: int):
        if pid in self.active_processes:
            process = self.active_processes[pid]
            try:
                os.kill(pid, signal.SIGTERM)
                process.wait(timeout=1)  # Give it a second to terminate gracefully
            except (ProcessLookupError, subprocess.TimeoutExpired):
                try:
                    os.kill(pid, signal.SIGKILL)  # Force kill if necessary
                except ProcessLookupError:
                    pass
            finally:
                del self.active_processes[pid]

    def kill_all_processes(self):
        for pid in list(self.active_processes.keys()):
            self.kill_process(pid)

    def get_script_history(self) -> List[str]:
        return self.script_history

    def clear_history(self):
        self.script_history.clear()

    def validate_script(self, script_content: str) -> bool:
        # Basic script validation
        try:
            shell = self.settings.get("default_shell", "bellos")
            process = subprocess.run(
                [shell, "-n"],
                input=script_content,
                text=True,
                capture_output=True
            )
            return process.returncode == 0
        except Exception:
            return False

    def get_active_processes(self) -> Dict[int, subprocess.Popen]:
        # Clean up finished processes
        for pid in list(self.active_processes.keys()):
            if self.active_processes[pid].poll() is not None:
                del self.active_processes[pid]
        return self.active_processes
