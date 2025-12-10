import os
from pathlib import Path

def clear_empty_dir(path: str | os.PathLike):
    path = Path(path)
    
    if not path.is_dir():
        raise ValueError("path is not a directory")
    
    # Recursively clear empty subdirectories first
    for item in path.iterdir():
        if item.is_dir():
            clear_empty_dir(item)
    
    # After clearing subdirectories, check if current directory is now empty
    if path.is_dir():
        # Use list comprehension to check for remaining items
        remaining_items = list(path.iterdir())
        if len(remaining_items) == 0:
            print(f"clear empty dir: {path}")
            path.rmdir()
            return True  # Directory was deleted
    return False  # Directory was not empty or doesn't exist

if __name__ == "__main__":
    clear_empty_dir(Path.cwd())