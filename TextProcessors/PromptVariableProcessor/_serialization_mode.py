from enum import Enum

class SerializationMode(Enum):
    """Serialization mode for the prompt variable processor."""
    JSON = "json"
    YAML = "yaml"
    REPR = "repr"
    STR = "str"