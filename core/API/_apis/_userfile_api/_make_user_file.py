from typing import BinaryIO
from ....User_Config_Manager import (
    UserConfigs
)
from ....Context_Manager import (
    ContextObject
)
import zipfile
import orjson
from ._readable_context import readable_context
import yaml

def make_user_file(file: BinaryIO, context: ContextObject, prompt: str, user_configs: UserConfigs) -> None:
    with zipfile.ZipFile(file, "w") as zipf:
        zipf.writestr(
            "user_context.json",
            orjson.dumps(
                context.context
            )
        )
        zipf.writestr(
            "user_context_readable.txt",
            readable_context(
                context
            )
        )
        zipf.writestr(
            "user_prompt.json",
            orjson.dumps(
                prompt
            )
        )
        zipf.writestr(
            "user_prompt_readable.txt",
            prompt
        )
        zipf.writestr(
            "user_config.json",
            orjson.dumps(
                user_configs.model_dump(
                    exclude_defaults=True
                )
            )
        )
        zipf.writestr(
            "user_config_readable.yaml",
            (
                yaml.dump(
                    user_configs.model_dump(
                        exclude_defaults=True
                    ),
                    indent = 2,
                    allow_unicode = True
                )
            )
        )
    file.seek(0)