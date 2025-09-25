# A lightly dependent Python script launcher!
# Python Simple Launcher For Virtual Environment Scripts
# Sloves Starter !!!

__version__ = "0.3.1"

import platform
import subprocess
from pathlib import Path
import json
import shlex
import os
from typing import Any, Generic, TypeVar, Union, Optional, overload
import platform
import sys
import time
from enum import Enum
import atexit

SYSTEM: str = platform.system()

T_CPV = TypeVar('T_CPV')

class ExitCode(Enum):
    ONLY_PAUSE = None
    SUCCESS = 0
    CONFIG_NOT_FOUND = 1
    CONFIG_DECODE_ERROR = 2
    CONFIG_ENCODE_ERROR = 3
    CONFIG_WRITE_ERROR = 4
    CONFIG_READ_ERROR = 5
    CONFIG_PERMISSION_ERROR = 6
    SCRIPT_NOT_FOUND = 7
    SCRIPT_NAME_TYPE_ERROR = 8
    SCRIPT_NAME_IS_EMPTY = 9
    SCRIPT_NAME_NOT_PROVIDED = 10
    USER_TERMINATED = 11

    UNKNOWN_ERROR = 255


class CrossPlatformValue(Generic[T_CPV]):
    """Cross-platform value container that returns the corresponding value based on the current operating system."""
    
    def __init__(
        self,
        windows: Optional[T_CPV] = None,
        linux: Optional[T_CPV] = None,
        macos: Optional[T_CPV] = None,
        jvm: Optional[T_CPV] = None,
        default: Optional[T_CPV] = None
    ):
        self._windows_value: Optional[T_CPV] = windows
        self._linux_value: Optional[T_CPV] = linux
        self._macos_value: Optional[T_CPV] = macos
        self._jvm_value: Optional[T_CPV] = jvm
        self._default_value: Optional[T_CPV] = default
    
    @property
    def windows(self) -> Optional[T_CPV]:
        if self._windows_value is not None:
            return self._windows_value
        elif self._default_value is not None:
            return self._default_value
        else:
            raise ValueError("No value provided for the current platform.")
    
    @windows.setter
    def windows(self, value: T_CPV):
        self._windows_value = value
    
    @property
    def linux(self) -> Optional[T_CPV]:
        if self._linux_value is not None:
            return self._linux_value
        elif self._default_value is not None:
            return self._default_value
        else:
            raise ValueError("No value provided for the current platform.")
    
    @linux.setter
    def linux(self, value: T_CPV):
        self._linux_value = value
    
    @property
    def macos(self) -> Optional[T_CPV]:
        if self._macos_value is not None:
            return self._macos_value
        elif self._default_value is not None:
            return self._default_value
        else:
            raise ValueError("No value provided for the current platform.")
    
    @macos.setter
    def macos(self, value: T_CPV):
        self._macos_value = value

    @property
    def jvm(self) -> Optional[T_CPV]:
        if self._jvm_value is not None:
            return self._jvm_value
        elif self._default_value is not None:
            return self._default_value
        else:
            raise ValueError("No value provided for the current platform.")

    @jvm.setter
    def jvm(self, value: T_CPV):
        self._jvm_value = value
    
    @property
    def value(self) -> T_CPV:
        """Get the value corresponding to the current platform."""
        if SYSTEM == "Windows" and self._windows_value is not None:
            return self._windows_value
        elif SYSTEM == "Linux" and self._linux_value is not None:
            return self._linux_value
        elif SYSTEM == "Darwin" and self._macos_value is not None:
            return self._macos_value
        elif SYSTEM == "Java" and self._jvm_value is not None:
            return self._jvm_value
        elif self._default_value is not None:
            return self._default_value
        else:
            raise ValueError("No value provided for the current platform.")
    
    def get_value_or(self, default: T_CPV) -> T_CPV:
        """Get the value, return the provided default value if it is undefined."""
        try:
            return self.value
        except ValueError:
            return default
    
    def is_defined_for_current_platform(self) -> bool:
        """Check if there are defined values in the current platform."""
        if SYSTEM == "Windows":
            return self._windows_value is not None
        elif SYSTEM == "Linux":
            return self._linux_value is not None
        elif SYSTEM == "Darwin":
            return self._macos_value is not None
        elif SYSTEM == "Java":
            return self._jvm_value is not None
        return False
    
    def dump(self) -> dict[str, T_CPV | None]:
        """Dump the values to a dictionary."""
        return {
            "windows": self.windows,
            "linux": self.linux,
            "macos": self.macos,
            "jvm": self.jvm,
            "default": self._default_value
        }
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return (
            f"CrossPlatformValue("
            f"windows={self._windows_value}, "
            f"linux={self._linux_value}, "
            f"macos={self._macos_value}, "
            f"jvm={self._jvm_value}, "
            f"default={self._default_value}"
            f")"
        )
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CrossPlatformValue):
            return False
        return (self._windows_value == other._windows_value and
                self._linux_value == other._linux_value and
                self._macos_value == other._macos_value and
                self._jvm_value == other._jvm_value and
                self._default_value == other._default_value)

class SlovesStarter:
    YES_CHARSET: list[str] = ["y", "yes", "true", "t", "1"]
    NO_CHARSET: list[str] = ["n", "no", "false", "f", "0"]
    def __init__(self):
        self.python_name: CrossPlatformValue[str] = CrossPlatformValue(
            windows = "python",
            linux = "python3",
            default = "python3"
        )
        self.pip_name: CrossPlatformValue[str] = CrossPlatformValue(
            windows = "pip",
            linux = "pip3",
            default = "pip3"
        )
        self.requirements_file: CrossPlatformValue[str] = CrossPlatformValue(
            default = "requirements.txt"
        )
        self.venv_prompt: str = "venv"
        self.script_name: str | list[str] | None = None
        self.argument: list[str] | None = None
        self.title: str = "Sloves Python Script Starter"
        self.process_title: str = "Python Script"
        self.process_exit_title: str = self.title
        self.exit_title: str = self.title
        self.use_venv: bool = True
        self.cwd = Path.cwd()
        self.work_directory: Path = self.cwd
        self.restart:bool = False
        self.run_cmd_need_to_ask: bool = True
        self.run_cmd_ask_default_values: dict[str, bool] = {}
        self.divider_line_char: str = "="
        self.inject_environment_variables: dict[str, str] = {}

        self.set_title(self.title)

        try:
            self.parse_config(self.load_config())
        except FileNotFoundError:
            suffix:int = 0
            while True:
                if suffix == 0:
                    config_file = Path(f"config.json")
                else:
                    config_file = Path(f"config_{suffix}.json")
                
                if not config_file.exists():
                    self.create_configuration(config_file)
                    break
                else:
                    suffix += 1
            print("Continuing to run the program will operate with the default configuration...")
            self.pause_program(ExitCode.ONLY_PAUSE)
    
    @staticmethod
    def is_venv():
        return hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
        )

    @classmethod
    def load_config(cls):
        suspected_configuration_file: list[Path] = []
        for file in Path.cwd().glob("*.json"):
            suspected_configuration_file.append(file)
        
        if len(suspected_configuration_file) == 1:
            config_file = suspected_configuration_file[0]
        elif len(suspected_configuration_file) > 1:
            print("Multiple configuration files found. Please choose one:")
            for index, file in enumerate(suspected_configuration_file, start=1):
                print(f"  - [{index}] {file.name}")
            
            while True:
                user_choice = input("Choose one: ")
                try:
                    user_choice_index = int(user_choice)
                    if user_choice_index not in range(1, len(suspected_configuration_file) + 1):  # noqa: E501
                        print("Invalid choice. Please choose a number from the list.")
                        continue
                    config_file = suspected_configuration_file[user_choice_index - 1]
                    break
                except ValueError:
                    path = Path(user_choice)
                    if path in suspected_configuration_file:
                        config_file = path
                        break
                    else:
                        print("Invalid choice. Please try again.")
                        continue
        else:
            raise FileNotFoundError("No configuration file found.")
        
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as file:
                    config = json.load(file)
                    return config
            except json.JSONDecodeError:
                print("Invalid configuration file. Please check the file and try again.")
                cls.pause_program(ExitCode.CONFIG_DECODE_ERROR)
            except FileNotFoundError:
                print("Configuration file not found.")
                cls.pause_program(ExitCode.CONFIG_NOT_FOUND)
            except PermissionError:
                print("Permission denied. Please check the file permissions and try again.")
                cls.pause_program(ExitCode.CONFIG_PERMISSION_ERROR)
            except IOError as e:
                print("An error occurred while reading the configuration file.")
                print(e)
                cls.pause_program(ExitCode.UNKNOWN_ERROR)
        else:
            raise FileNotFoundError("Configuration file not found.")
        
    def parse_config(self, config: dict) -> None:
        if not isinstance(config, dict):
            raise TypeError("Config must be a dict")
        def exists_and_is_designated_type(key: str, types: type | tuple[type, ...]) -> bool:
            return key in config and isinstance(config[key], types)
        
        if exists_and_is_designated_type("title", str):
            self.title = config["title"]
            self.process_exit_title = self.title
            self.exit_title = self.title
        
        if exists_and_is_designated_type("process_title", str):
            self.process_title = config["process_title"]
        
        if exists_and_is_designated_type("process_exit_title", str):
            self.process_exit_title = config["process_exit_title"]
        
        if exists_and_is_designated_type("exit_title", str):
            self.exit_title = config["exit_title"]
        
        if exists_and_is_designated_type("python_name", dict):
            try:
                self.python_name = CrossPlatformValue(**config["python_name"])
            except Exception:
                pass
        
        if exists_and_is_designated_type("pip_name", dict):
            try:
                self.pip_name = CrossPlatformValue(**config["pip_name"])
            except Exception:
                pass
        
        if exists_and_is_designated_type("requirements_file", dict):
            try:
                self.requirements_file = CrossPlatformValue(**config["requirements_file"])
            except Exception:
                pass
        
        if exists_and_is_designated_type("venv_prompt", str):
            self.venv_prompt = config["venv_prompt"]
        
        if exists_and_is_designated_type("script_name", str | list):
            self.script_name = config["script_name"]
        
        if exists_and_is_designated_type("argument", list):
            self.argument = config["argument"]
        
        if exists_and_is_designated_type("use_venv", bool):
            self.use_venv = config["use_venv"]
        
        if exists_and_is_designated_type("cwd", str):
            self.cwd = Path(config["cwd"])
            self.work_directory = self.cwd
        
        if exists_and_is_designated_type("work_directory", str):
            self.work_directory = Path(config["work_directory"])
            
        if exists_and_is_designated_type("restart", bool):
            self.restart = config["restart"]
        
        if exists_and_is_designated_type("run_cmd_need_to_ask", bool):
            self.run_cmd_need_to_ask = config["run_cmd_need_to_ask"]
        
        if exists_and_is_designated_type("run_cmd_ask_default_values", dict):
            type_correct: bool = True
            for key, value in config["run_cmd_ask_default_values"].items():
                if not isinstance(key, str):
                    type_correct = False
                    break
                if not isinstance(value, bool):
                    type_correct = False
                    break
            if type_correct:
                self.run_cmd_ask_default_values = config["run_cmd_ask_default_values"]
        
        if exists_and_is_designated_type("divider_line_char", str):
            if len(config["divider_line_char"]) == 1:
                self.divider_line_char = config["divider_line_char"]
        
        if exists_and_is_designated_type("inject_environment_variables", dict):
            type_correct: bool = True
            for key, value in config["inject_environment_variables"].items():
                if not isinstance(key, str):
                    type_correct = False
                    break
                if not isinstance(value, str):
                    type_correct = False
                    break
            if type_correct:
                self.inject_environment_variables = config["inject_environment_variables"]
    
    def create_configuration(self, output: str | Path | None = None):
        config = {
            "title": self.title,
            "process_title": self.process_title,
            "process_exit_title": self.process_exit_title,
            "exit_title": self.exit_title,
            "python_name": self.python_name.dump(),
            "pip_name": self.pip_name.dump(),
            "requirements_file": self.requirements_file.dump(),
            "cwd": str(self.cwd),
            "work_directory": str(self.work_directory),
            "use_venv": self.use_venv,
            "venv_prompt": self.venv_prompt,
            "script_name": self.script_name,
            "argument": self.argument,
            "restart": self.restart,
            "run_cmd_need_to_ask": self.run_cmd_need_to_ask,
            "run_cmd_ask_default_values": self.run_cmd_ask_default_values,
            "divider_line_char": self.divider_line_char,
            "inject_environment_variables": self.inject_environment_variables,
        }
        if output is None:
            return config
        else:
            with open(output, "w", encoding="utf-8") as f:
                f.write(json.dumps(config, indent=4, ensure_ascii=False))

    @staticmethod
    def pause_program(code: ExitCode | int = ExitCode.SUCCESS, prompt: str | None = None):
        if isinstance(code, ExitCode) and code == ExitCode.ONLY_PAUSE:
            print(prompt or "Press Ctrl+C to continue.")
        else:
            print(prompt or f"Press Ctrl+C to Exit with code {code.value if isinstance(code, ExitCode) else code}{f'({code.name})' if isinstance(code, ExitCode) else ''}.")
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            if isinstance(code, ExitCode) and code != ExitCode.ONLY_PAUSE:
                exit(code.value)
            if isinstance(code, int):
                exit(code)
            else:
                return
    
    def run_cmd(self, cmd: list[str], reason: str, cwd: Path | None = None, default: bool = True, print_return_code: bool = True, env: dict[str, str] | None = None):
        print(f"Running command: {shlex.join(cmd)}")
        run = default
        if self.run_cmd_need_to_ask:
            if default:
                y_n_str = "[Y/n]"
            else:
                y_n_str = "[y/N]"
            if reason in self.run_cmd_ask_default_values:
                value = self.run_cmd_ask_default_values[value]
                if isinstance(value, bool):
                    print(f"{reason} {y_n_str}: ", end=f"{value}\n")
                    run = value
                else:
                    print(f"{reason} {y_n_str}: ", end=f"{value}\n")
                    return value
            else:
                user_input = input(f"{reason} {y_n_str}:")
                if default:
                    if user_input.lower() in self.NO_CHARSET:
                        run = False
                    else:
                        run = True
                else:
                    if user_input.lower() in self.YES_CHARSET:
                        run = True
                    else:
                        run = False
        
        if run:
            result = subprocess.run(cmd, cwd=cwd, env=env)
            if print_return_code:
                print(f"Command returned with code {result.returncode}")
            return result
        else:
            return None

    # Initialize virtual environment
    def init_venv(self, ignore_existing: bool = True):
        if not (ignore_existing and (Path.cwd() / ".venv" / "pyvenv.cfg").exists()):
            if self.run_cmd([self.python_name.value, "-m", "venv", ".venv", "--prompt", self.venv_prompt], reason="Initializing virtual environment", cwd=self.cwd) is not None:
                if SYSTEM == "Windows":
                    venv_bin_path = Path.cwd() / ".venv" / "Scripts"
                else:
                    venv_bin_path = Path.cwd() / ".venv" / "bin"
                if (Path.cwd() / self.requirements_file.value).exists():
                    if self.run_cmd([str(venv_bin_path / self.pip_name.value), "install", "-r", self.requirements_file.value], reason="Installing requirements", cwd=self.cwd) is None:
                        print("Failed to install requirements.")
            else:
                print("Failed to initialize virtual environment.")
    
    # Run the program
    def get_start_cmd(self):
        def choose_script_file(script_list: list[Path]) -> Path | None:
            if len(script_list) == 0:
                return None
            elif len(script_list) == 1:
                return script_list[0]
            else:
                print("Choose one of the following scripts:")
                for index, script in enumerate(script_list, start=1):
                    print(f"  - [{index}] {script.name}")
                while True:
                    choice = input("Enter the name of the script you want to run: ")
                    try:
                        choice_index = int(choice)
                        if choice_index in range(1, len(script_list) + 1):
                            script_name = script_list[choice_index - 1]
                            break
                        else:
                            print("Index out of range. Please try again.")
                    except ValueError:
                        paths = {str(i.name).lower(): i for i in script_list}
                        if choice.lower() in paths:
                            if paths[choice.lower()].exists():
                                script_name = paths[choice.lower()]
                                break
                            else:
                                print("Script not found. Please try again.")
                        else:
                            print("Invalid choice. Please try again.")
                return script_name
        
        if self.script_name is None:
            suspected_script_file:list[Path] = []
            self_path = Path(sys.argv[0])
            for file in Path.cwd().glob("*.py"):
                if file != self_path:
                    suspected_script_file.append(file)
            if len(suspected_script_file) == 0:
                print("No Python script files found in the current directory.")
                sys.exit(1)
            script_name = choose_script_file(suspected_script_file)
        elif isinstance(self.script_name, list):
            if len(self.script_name) == 1:
                script_name = Path(self.script_name[0])
            elif len(self.script_name) == 0:
                print("`script_name` is empty")
                self.pause_program(ExitCode.SCRIPT_NAME_IS_EMPTY)
            else:
                script_name = choose_script_file(self.script_name)
        elif isinstance(self.script_name, str | Path):
            if Path(self.script_name).exists():
                script_name = Path(self.script_name)
            else:
                print("Error: Script not found!")
                self.pause_program(ExitCode.SCRIPT_NOT_FOUND)
        else:
            print("`script_name` must be a string or a list/tuple of strings")
            self.pause_program(ExitCode.SCRIPT_NAME_TYPE_ERROR)
        
        if script_name is None:
            print("Error: No script name provided")
            self.pause_program(ExitCode.SCRIPT_NAME_NOT_PROVIDED)
        
        if self.use_venv:
            if SYSTEM == "Windows":
                start = [str(Path.cwd() / ".venv" / "Scripts" / self.python_name.value), str(script_name)]
            else:
                start = [str(Path.cwd() / ".venv" / "bin" / self.python_name.value), str(script_name)]
        else:
            start = [self.python_name.value, str(script_name)]

        if self.argument:
            start.extend(self.argument)
            print("Use argument:")
            print(shlex.join(self.argument))
        else:
            if len(sys.argv) > 1:
                argument = sys.argv[1:]
                print("Use argument:")
                print(shlex.join(argument))
                start.extend(argument)
        return start
    
    @staticmethod
    def set_title(title: str):
        if SYSTEM == "Windows":
            try:
                import ctypes
                # Win API
                ctypes.windll.kernel32.SetConsoleTitleW(title)
            except Exception:
                os.system(f'title "{title}"')
        else:
            sys.stdout.write(f"\033]2;{title}\007")
            sys.stdout.flush()
    
    def print_divider_line(self, char: str | None = None):
        print((char or self.divider_line_char) * os.get_terminal_size().columns)
    
    @staticmethod
    def center_print(text: str):
        print(text.center(os.get_terminal_size().columns))

    def main(self):
        self.center_print(self.title)
        if self.is_venv():
            print("Starter Run in Virtual Environment")
        self.set_title(self.title)
        if self.use_venv:
            self.print_divider_line()
            self.init_venv()
        return_code = ExitCode.SUCCESS
        while True:
            try:
                start = self.get_start_cmd()
                self.print_divider_line()
                result = self.run_cmd(
                    start,
                    reason = "Running the program",
                    cwd = self.work_directory,
                    print_return_code = False,
                    env = self.inject_environment_variables
                )
                self.print_divider_line()
                if result is not None:
                    if result.returncode != 0:
                        print("An error occurred while running the program.")
                        return_code = result.returncode
            except KeyboardInterrupt:
                self.print_divider_line()
                print("Program terminated by user.")
            finally:
                # Reset Title
                self.set_title(self.title)
                if self.restart:
                    user_input = input("Re-select? (y/N): ").lower()
                    if user_input in ["y", "yes"]:
                        continue
                    else:
                        break
                else:
                    break
        
        self.pause_program(return_code)
    
    @atexit.register
    def exit_handler(self):
        self.set_title(self.exit_title)

if __name__ == "__main__":
    try:
        starter = SlovesStarter()
        starter.main()
    except KeyboardInterrupt:
        print("Program terminated by user.")
        exit(ExitCode.USER_TERMINATED)
    except Exception as e:
        import traceback
        traceback.print_exc()
        SlovesStarter.pause_program(ExitCode.UNKNOWN_ERROR)