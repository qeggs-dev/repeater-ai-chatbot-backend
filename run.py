import os
import time
import sys
import shlex
import platform
import subprocess
from pathlib import Path
from typing import TypeVar, Iterable

# 尝试导入prompt_toolkit，如果失败则忽略
try:
    import prompt_toolkit
    from prompt_toolkit.completion import WordCompleter
    import_prompt_toolkit = True
except ImportError:
    prompt_toolkit = None
    WordCompleter = None
    import_prompt_toolkit = False

# 定义一些基础的常量 （以防有人想改的时候找不到）
BASE_VENV_PATH = Path(".venv")
BASE_WINDOWS_PYTHON = Path("python.exe")
BASE_LINUX_PYTHON = Path("python3")
SYSTEM = platform.system() # 主打一个减少计算

T = TypeVar("T")

# 定义一个退出异常，用于退出程序
class ExitException(Exception):
    """
    用于退出程序的异常
    """
    def __init__(self, code: int = 0):
        self.code = code
        super().__init__()

    def __str__(self):
        return f"ExitException(code={self.code})"

# 定义一个重启异常，用于重启程序
class RestartException(Exception):
    """
    用于重启程序逻辑的异常
    """
    pass

class ScriptStarter:
    """
    脚本启动器
    """
    def __init__(self):
        self.venv_path = BASE_VENV_PATH
        if SYSTEM == "Windows":
            self.python_path = BASE_WINDOWS_PYTHON
        else:
            self.python_path = BASE_LINUX_PYTHON
        
        self.script_path = ("run_fastapi.py")

        self.last_process_return_code = None

        self.allow_pipx: bool | None = None

        self.seek_user_consent_cache: dict[str, bool] = {}

        self.starter_run_in_virtual_environment = (
            (hasattr(sys, 'base_prefix') and sys.prefix != sys.base_prefix) or
            (os.getenv('VIRTUAL_ENV') is not None)
        )
    
    @property
    def venv_bin_path(self):
        if SYSTEM == "Windows":
            return self.venv_path / "Scripts"
        else:
            return self.venv_path / "bin"
    
    def seek_user_consent(
            self,
            prompt,
            default_item: bool = False,
            cached: bool = False,
            allow_empty_input: bool = False
        ) -> bool:
        """
        寻求用户同意
        """
        yes_characters = ["y", "yes", "yep", "1", "true"]
        no_characters = ["n", "no", "nope", "0", "false"]
        if cached:
            if prompt in self.seek_user_consent_cache:
                return self.seek_user_consent_cache[prompt]
        while True:
            if import_prompt_toolkit:
                completer = WordCompleter(yes_characters + no_characters)
                check = prompt_toolkit.prompt(f"{prompt} [{'Y/n' if default_item else 'y/N'}]: ", completer=completer)
            else:
                check = input(f"{prompt} [{'Y/n' if default_item else 'y/N'}]: ")
            if allow_empty_input or check:
                break

        if default_item:
            if check.lower() in no_characters:
                allow = False
            else:
                allow = True
        else:
            if check.lower() in yes_characters:
                allow = True
            else:
                allow = False
        
        if cached:
            self.seek_user_consent_cache[prompt] = allow
        return allow
    
    def run_command(self, command: list[str], cwd: str | Path | None = None) -> tuple[str, str]:
        """
        运行其他命令时先询问用户是否运行
        """
        print(f"{sys.argv[0]} want to run the command:")
        print(shlex.join(command))
        if cwd is not None:
            print(f"in: {cwd}")
        if self.seek_user_consent("Do you want to continue?", default_item=False):
            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, text=True)
                stdout, stderr = process.communicate()
                return stdout, stderr
            except Exception as e:
                print(f"Error: {e}")
                raise
        else:
            print("Cancelled")
            return "", ""
    
    def install_package(self, package: list[str]):
        """
        安装包时先检查是否可用pipx
        """
        if self.allow_pipx is None:
            outpu, _ = self.run_command(["pip", "list"])
            for line in outpu.splitlines():
                if "pipx" in line:
                    self.allow_pipx = True
                    break
                else:
                    self.allow_pipx = False
        
        if self.allow_pipx:
            installer = "pipx"
        else:
            installer = "pip"
        
        self.run_command([installer, "install"] + package)
    
    @staticmethod
    def choose_one(items: Iterable[T], prompt: str = "Choose one:", item_prefix: str = "> ", select_only_one: bool = True) -> T | None:
        """
        选择一个选项
        """
        if not items:
            return None
        if select_only_one and len(items) == 1:
            return items[0]
        lower_items: dict[T] = {}
        for i, item in enumerate(items):
            print(f"{item_prefix}[{i + 1}]: {item}")
            lower_items[str(item).lower()] = item
        if import_prompt_toolkit:
            completer = WordCompleter(list(lower_items.keys()))
        while True:
            try:
                if import_prompt_toolkit:
                    choice = prompt_toolkit.prompt(prompt, completer=completer)
                else:
                    choice = input(prompt)
                if choice.lower() in lower_items:
                    return lower_items[choice.lower()]
                elif choice.isdigit() and int(choice) in range(1, len(items) + 1):
                    return items[int(choice) - 1]
                else:
                    continue
            except ValueError:
                pass
    
    def check_venv(self):
        """
        检查虚拟环境是否存在
        如果不存在尝试创建一个
        """
        if not self.venv_path.exists():
            print("Virtual environment not found. Searching for venv...")
            find_venv:list[Path] = []
            for path in Path.cwd().iterdir():
                if path.is_dir() and (path / "pyvenv.cfg").exists():
                    find_venv.append(path)
            
            choose = self.choose_one(find_venv, item_prefix="Find: ")
            self.venv_path = choose
            
            if not find_venv:
                print("No venv found.")
                run = [self.python_path, "-m", "venv", ".venv", "--prompt", "venv"]
                self.run_command(run)
                if (Path.cwd() / "requirements.txt").exists():
                    print("Finded requirements.txt.")
                    print("Installing requirements...")
                    # 此处因为requirements.txt默认安装到虚拟环境，所以不使用全局包安装器
                    run = [str(self.venv_bin_path / "pip"), "install", "-r", "requirements.txt"]
                    self.run_command(run)
    
    def check_pyscript(self):
        """
        检查脚本是否存在
        """
        while True:
            if not (Path.cwd() / self.script_path).exists():
                print(f"Script {self.script_path} not found in current directory.")
                find_script: list[Path] = []
                for path in Path.cwd().iterdir():
                    if path.is_file() and path.name.endswith(".py"):
                        find_script.append(path)

                choose = self.choose_one(find_script, item_prefix="Find: ")
                self.script_path = choose

                if not find_script:
                    print("No script found.")
                    raise ExitException(1)
            else:
                break

    def prompt_restart(self):
        """
        提示用户是否重启
        """
        if self.seek_user_consent("Do you want to restart the application?", True):
            raise RestartException
        else:
            raise ExitException(0)

    def start_script(self):
        """
        主函数，用于启动应用程序
        """
        self.check_venv()
        self.check_pyscript()

        run = [str(self.venv_bin_path / self.python_path), str(self.script_path)]
        # 默认参数透传
        if len(sys.argv) >= 2:
            run.extend(sys.argv[1:])
            print(f"Running: {shlex.join(run)}")
        
        while True:
            time_start = time.time()
            try:
                if self.seek_user_consent("Is it directly connected to the current console I/O?", True, cached=True):
                    result = subprocess.run(run, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
                else:
                    result = subprocess.run(run)
            except KeyboardInterrupt:
                print("Received interrupt signal (Ctrl+C)")
                self.prompt_restart()
            finally:
                time_end = time.time()

            print("\n====== Process End ======\n")
            print(f"Time Taken: {time_end - time_start} seconds")
            print("\n")
            print(f"Exit Code: {result.returncode}")
            self.last_process_return_code = result.returncode
            
            self.prompt_restart()
    def check_import(self):
        global prompt_toolkit, WordCompleter, import_prompt_toolkit
        if not import_prompt_toolkit:
            self.install_package(["pip", "install", "prompt_toolkit"])
            try:
                import prompt_toolkit
                from prompt_toolkit.completion import WordCompleter
                import_prompt_toolkit = True
            except ImportError:
                print("Failed to install prompt_toolkit.")
                import_prompt_toolkit = False
    
    def run(self):
        """
        负责处理重启和退出逻辑
        """
        if self.starter_run_in_virtual_environment:
            print("Running in a virtual environment.")
            self.check_import()
        while True:
            try:
                self.start_script()
                break
            except KeyboardInterrupt:
                pass
            except ExitException as e:
                print(f"Exiting application with code {e.code}")
                sys.exit(e.code)
            except RestartException:
                print("Restarting application...")
                continue

if __name__ == "__main__":
    start = ScriptStarter()
    start.run()