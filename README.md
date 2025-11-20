# @复读机Repeater
**- Only Chat, Focus Chat. -**

*注：本仓库仅为后端实现，NoneBot插件部分请查看[`Repater-Nonebot-Plugin`](https://github.com/qeggs-dev/repeater-qq-ai-chatbot-nonebot-plugins)*

一个基于[`NoneBot`](https://nonebot.dev/)和[`OpenAI SDK`](https://pypi.org/project/openai/)开发的**实验性**QQ聊天机器人
**此仓库仅为后端实现，NoneBot插件部分请查看[`Repater-Nonebot-Plugin`](https://github.com/qeggs-dev/repeater-qq-ai-chatbot-nonebot-plugins)**
将原始会话数据的处理直接公开给用户使用
接近直接操作API的灵活度体验

与其他QQ机器人相比，复读机具有以下特点：

 - 平行数据管理：支持平行数据管理，用户可以随意切换平行数据，而不需要担心数据丢失。
 - 多模型支持：支持OpenAI接口的模型即可调用，可以根据需要选择不同的模型进行对话。
 - 超高自由度：用户可以自定义会话注入、切换、删除，以及自定义提示词
 - MD图片渲染：可以将回复以图片的形式渲染发送，降低其妨碍用户正常聊天的程度（但鬼知道为什么这东西竟然不支持Emoji渲染！！！）
 - 命令别名触发：不管是缩写还是全文，都可以触发命令操作
 - 用户自治设计：用户可以自己管理自己的所有用户数据
 - 多预设人设：复读机支持多预设人设，用户可以自由选择自己喜欢的人设进行对话
> 注：拟人化并非复读机的赛道，复读机不对拟人化需求做过多保证，如有需要请自行引导或编写提示词。

## 注意事项:
 - 本服务由一位 `16岁自学开发者`(现在17了) 使用AI协作开发，公益项目，如果你愿意捐赠，可以在机器人的**QQ空间**中找到赞赏码以支持项目运营(或是支持开发者)。
 - 使用者需确认生成内容的合法性，并自行承担使用本服务可能产生的风险。
 - 如果你觉得这个Bot非常好用，请去看一下[`Deepseek`](https://www.deepseek.com/)的官网吧，这个Bot最初就是基于他们的模型API文档开发的。

---

## License
这个项目基于[MIT License](LICENSE)发布。

---

### 依赖项:
| Name              | Version  | License                              | License Link                                                                        | Where it is used                   | Reasons                               |
|-------------------|----------|--------------------------------------|-------------------------------------------------------------------------------------|------------------------------------|---------------------------------------|
| Markdown          | 3.8.2    | BSD 3-Clause License                 | [BSD-3-Clause](https://github.com/Python-Markdown/markdown/blob/master/LICENSE.md)  | `Markdown`                         | Parses Markdown text into HTML        |
| pyyaml            | 6.0.2    | MIT License                          | [MIT](https://github.com/yaml/pyyaml/blob/main/LICENSE)                             | `API` & `ConfigManager`            | Read configuration file               |
| aiofiles          | 24.1.0   | Apache Software License              | [Apache-2.0](https://github.com/Tinche/aiofiles/blob/main/LICENSE)                  | `core.DataManager`                 | Asynchronous file support             |
| environs          | 14.2.0   | MIT License                          | [MIT](https://github.com/sloria/environs/blob/main/LICENSE)                         | `run_fastapi.py` & `ConfigManager` | Support for environment variables     |
| fastapi           | 0.115.13 | MIT License                          | [MIT](https://github.com/fastapi/fastapi/blob/master/LICENSE)                       | `API`                              | Build API                             |
| httpx             | 0.28.1   | BSD License                          | [BSD-3-Clause](https://github.com/encode/httpx/blob/master/LICENSE.md)              | `core.FuncerClient`                | Asynchronous HTTP client              |
| imgkit            | 1.2.3    | MIT License                          | [MIT](https://github.com/jarrekk/imgkit/blob/master/LICENSE)                        | `Markdown`                         | Render HTML as an image               |
| loguru            | 0.7.3    | MIT License                          | [MIT](https://github.com/Delgan/loguru/blob/master/LICENSE)                         | *Entire Project*                   | Logging                               |
| openai            | 1.90.0   | Apache Software License              | [Apache-2.0](https://github.com/openai/openai-python/blob/main/LICENSE)             | `core.CallAPI`                     | Call the OpenAI API                   |
| orjson            | 3.10.18  | Apache Software License; MIT License | [Apache-2.0](https://github.com/ijl/orjson/blob/master/LICENSE-APACHE) / [MIT](https://github.com/ijl/orjson/blob/master/LICENSE-MIT) | `core.DataManager` | High-performance JSON  resolution |
| pydantic          | 2.11.7   | MIT License                          | [MIT](https://github.com/pydantic/pydantic/blob/main/LICENSE)                       | `core.ConfigManager` & `API`       | Simple and convenient data validation |
| python-multipart  | 0.0.20   | Apache Software License              | [Apache-2.0](https://github.com/Kludex/python-multipart/blob/master/LICENSE.txt)    | `core.DataManager` & `API`         | Support for form data                 |
| uvicorn           | 0.34.3   | BSD License                          | [BSD-3-Clause](https://github.com/Kludex/uvicorn/blob/main/LICENSE.md)              | `run_fastapi.py`                   | Run FastAPI                           |
| numpy             | 2.3.4    | BSD License                          | [BSD-3-Clause](https://github.com/numpy/numpy/blob/main/LICENSE.txt)                | *Entire Project*                   | Speed up batch computing of data      |
| deprecated        | 1.2.18   | MIT License                          | [MIT](https://github.com/laurent-laporte-pro/deprecated/blob/master/README.md)      | *Not in use yet*                   | Mark Obsolete Code                    |

---

## 安装部署

**至少需要确保安装了Python3.11以上版本**

### 自动安装

1. 将项目克隆到本地
2. 进入项目目录
5. 运行`run.py`启动器（不用担心，这个启动器可以在全局环境运行，它只有标准库依赖）

### 手动安装

1. 将项目克隆到本地
2. 进入项目目录
3. 执行`python3 -m venv .venv`创建虚拟环境
4. 执行`.venv/bin/activate`激活虚拟环境(Windows下则是`.venv\Scripts\activate`)
5. 执行`pip install -r requirements.txt`安装依赖
6. 执行`python3 run_fastapi.py`启动服务

PS: `run.py`启动器会在完成所有操作后启动主程序，而这只需要你保证你的配置正确
并且每一次你都可以通过启动器来启动程序

---

## 环境变量表

| 环境变量 | 描述 | 是否必填 | 默认值(*示例值*) |
| :---: | :---: | :---: | :---: |
| `*API_KEY` | API_Key (具体变量名由`API_INFO.API_FILE_PATH`指向 文件中`ApiKeyEnv`字段的名称) | **必填** | *\*可从[Deepseek开放平台/API Keys](https://platform.deepseek.com/api_keys)页面获取* |
| `ADMIN_API_KEY` | 管理员API_Key (用于框架的管理员操作身份验证) | **选填但生产环境建议填写** | *\*自动生成随机 API Key* |
| `CONFIG_FILE_PATH` | 配置文件路径 | **选填** | `./config/project_config.json` |
| `CONFIG_ENVIRONMENT` | 配置文件环境 | **选填** | `DEV` |
| `HOST` | 服务监听的IP | **选填** | `0.0.0.0` |
| `PORT` | 服务监听的端口 | **选填** | `8080` |
| `WORKERS` | 服务监听的进程数 | **选填** | `1` |
| `RELOAD` | 是否自动重启 | **选填** | `false` |

## 配置选项表

| 选项 | 描述 | 是否必填 | **默认值**(*示例值*) | 类型 | 单位 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| `RENDER.MARKDOWN.WKHTMLTOIMAGE_PATH` | 渲染图片依赖的[`Wkhtmltopdf`](https://wkhtmltopdf.org/downloads.html)中`wkhtmltoimage`的路径 | **必填** | *`/usr/local/bin/wkhtmltoimage`* | str | |
| `RENDER.OUTPUT_IMAGE_DIR` | 渲染图片的缓存位置 | **必填** | *`./workspace/temp/render`* | str | |
| `STATIC.BASE_PATH` | 静态资源位置 | **必填** | *`./static`* | str | |
| `API_INFO.API_FILE_PATH` | API信息文件路径 | *选填* | `./config/apiconfig.json` | str | |
| `API_INFO.DEFAULT_MODEL_UID` | 调用时默认使用的模型UID | *选填* | `deepseek-chat` | str | |
| `BLACKLIST.FILE_PATH` | 黑名单文件位置 | *选填* | `./config/blacklist.regex` | str | |
| `BLACKLIST.MATCH_TIMEOUT` | 黑名单匹配超时时间 | *选填* | `10` | int | 秒 |
| `BOT_INFO.NAME` | 机器人名字 | *选填* | `Bot` | str | |
| `BOT_INFO.BIRTHDAY.YEAR` | 机器人出生年份 | *选填* | *`2024`* | int | 年 |
| `BOT_INFO.BIRTHDAY_MONTH` | 机器人出生月份 | *选填* | *`01`* | int | 月 |
| `BOT_INFO.BIRTHDAY_DAY` | 机器人出生日期 | *选填* | *`01`* | int | 日 |
| `CALLAPI.MAX_CONCURRENCY` | 最大并发数(仅适用于主请求API，也就是Chat API) | *选填* | `1000` | int | 请求数 |
| `CONFIG_CACHE.DEBONCE_SAVE_WAIT_TIME` | 配置管理器缓存延迟保存时间 | *选填* | `600.0` | float | 秒 |
| `CONFIG_CACHE.DOWNGRADE_WAIT_TIME` | 配置管理器缓存降级等待时间 | *选填* | `600.0` | float | 秒 |
| `CORE.VERSION` | 版本号(用于替换Core中的版本号数据，以及提示词变量中的版本号) | *选填* | \*由代码自动生成 | str | |
| `LOGGER.LOG_LEVEL` | 日志级别 | *选填* | `INFO` | str | |
| `LOGGER.LOG_FILE_DIR` | 日志文件位置 | *选填* | `./logs` | str | |
| `LOGGER.LOG_FILE_PREFIX` | 日志文件前缀 | *选填* | `repeater_log_` | str | |
| `LOGGER.LOG_FILE_SUFFIX` | 日志文件后缀 | *选填* | `.log` | str | |
| `LOGGER.ROTATION` | 日志文件轮换配置 | *选填* | `10 MB` | str | 日志大小、时间长度等 |
| `LOGGER.LOG_RETENTION` | 日志文件保留时间 | *选填* | `14 days` | str | 时间 |
| `MODEL.DEFAULT_TEMPERATURE` | 默认模型温度 | *选填* | `1.0` | float | |
| `MODEL.DEFAULT_TOP_P` | 默认模型`Top_P` | *选填* | `1.0` | float | |
| `MODEL.DEFAULT_FREQUENCY_PENALTY` | 默认模型频率惩罚 | *选填* | `0.0` | float | |
| `MODEL.DEFAULT_PRESENCE_PENALTY` | 默认模型存在惩罚 | *选填* | `0.0` | float | |
| `MODEL.DEFAULT_MAX_TOKENS` | 默认模型最大输出token<br/>(部分API不支持 `DEFAULT_MAX_COMPLETION_TOKENS`设置 提供此项以兼容) | *选填* | `1024` | int | Token |
| `MODEL.DEFAULT_MAX_COMPLETION_TOKENS` | 默认模型最大生成token | *选填* | `1024` | int | Token |
| `MODEL.DEFAULT_STOP` | 默认模型停止词 | *选填* | [] | list[str] | |
| `MODEL.STREAM` | 是否内部启用流式输出(此选项仅告知框架是否启用流式生成，但框架内部存在缓冲区，开启此选项后如果请求时没有设置`stream`参数，会等待生成完毕) | *选填* | `true` | bool |
| `MODEL.AUTO_SHRINK_LENGTH` | 默认的自动Shrink阈值上下文长度 | *选填* | 0 | int | 上下文条数(为0时不自动限制长度) |
| `README.FILE_PATH` | README文件位置 | *选填* | `./README.md` | str | |
| `RENDER.DEFAULT_IMAGE_TIMEOUT` | 渲染图片的默认保留时间(图片生成后给予客户端的图片链接有效时间) | *选填* | 60 | float | 秒 |
| `RENDER.MARKDOWN.TO_IMAGE.DEFAULT_STYLES` | Markdown默认渲染图片的样式 | *选填* | `light` | str | |
| `RENDER.MARKDOWN.TO_IMAGE.STYLES_DIR` | Markdown渲染图片的样式文件夹 | *选填* | `./styles` | str | |
| `RENDER.MARKDOWN.TO_IMAGE.PREPROCESS_MAP.BEFORE` | Markdown渲染预处理映射（键会被替换为值的内容） | *选填* | *`{"\n": "<br/>"}`* | str | |
| `RENDER.MARKDOWN.TO_IMAGE.PREPROCESS_MAP.AFTER` | Markdown渲染后处理映射（键会被替换为值的内容） | *选填* | *`{"<code>": "<pre><code>", "</code>": "</code></pre>"}`* | str | |
| `REQUESTLOG.AUTO_SAVE` | 是否将记录到主API的请求日志自动保存到文件 | *选填* | `True` | bool | |
| `REQUESTLOG.DEBONCE.SAVE_WAIT_TIME` | 请求日志持久化存储的防抖时间 | *选填* | `1200.0` | float | 秒 |
| `REQUESTLOG.MAX_CACHE_SIZE` | 请求日志缓存的最大数量 | *选填* | `1000` | int | 日志数量 |
| `REQUESTLOG.PATH` | 主API请求日志的持久化存储目录 | *选填* | *`./workspace/request_log`* | str | |
| `SERVER.HOST` | 服务监听的IP(此选项会覆盖环境变量中的配置) | *选填* | 环境变量`HOST` | str | |
| `SERVER.PORT` | 服务监听端口(此选项会覆盖环境变量中的配置) | *选填* | 环境变量`PORT` | int | |
| `SERVER.WORKERS` | 服务工作进程数(此选项会覆盖环境变量中的配置) | *选填* | 环境变量`WORKERS` | int | |
| `SERVER.RELOAD` | 是否自动重启 | *选填* | 环境变量`RELOAD` | bool | |
| `PROMPT.DEFAULT_DIR` | 默认提示词文件夹 | *选填* | `./Prompt/Presets` | str | |
| `PROMPT.PARSET_NAME` | 默认提示词文件名(不包括文件后缀) | *选填* | `default` | str | |
| `PROMPT.DEFAULT_SUFFIX` | 默认提示词文件后缀 | *选填* | `.md` | str | |
| `TIME.TIMEZONE` | 时区 | *选填* | `8` | int | 偏移小时数 |
| `USER_DATA.SUB_DIR_NAME` | 用户子数据文件夹名称 | *选填* | `ParallelData` | str | |
| `USER_DATA.DIR` | 用户数据存放位置 | *选填* | `./data/userdata` | str | |
| `USER_DATA.METADATA_FILENAME` | 用户数据元数据文件名 | *选填* | `metadata.json` | str | |
| `USER_DATA.CACHE_METADATA` | 是否缓存用户数据元数据 | *选填* | `False` | bool | |
| `USER_DATA.CONTEXT_USERDATA.CACHE_METADATA` | 控制用户数据元数据缓存是否开启 | *选填* | \*`USER_DATA.CACHE_METADATA`的值 | bool | |
| `USER_DATA.PROMPT_USERDATA.CACHE_METADATA` | 控制提示词数据元数据缓存是否开启 | *选填* | \*`USER_DATA.CACHE_METADATA`的值 | bool | |
| `USER_DATA.USERCONFIG_USERDATA.CACHE_METADATA` | 配置用户数据元数据缓存是否开启 | *选填* | \*`USER_DATA.CACHE_METADATA`的值 | bool | |
| `USER_DATA.CACHE_DATA` | 是否缓存用户数据 | *选填* | `False` | bool | |
| `USER_DATA.CONTEXT_USERDATA.CACHE_DATA` | 控制用户数据缓存是否开启 | *选填* | \*`USER_DATA.CACHE_DATA`的值 | bool | |
| `USER_DATA.PROMPT_USERDATA.CACHE_DATA` | 控制提示词数据缓存是否开启 | *选填* | \*`USER_DATA.CACHE_DATA`的值 | bool | |
| `USER_DATA.USERCONFIG_USERDATA.CACHE_DATA` | 配置用户数据缓存是否开启 | *选填* | \*`USER_DATA._CACHE_DATA`的值 | bool | |
| `USER_NICKNAME_MAPPING.FILE_PATH` | 用户昵称映射表文件位置 | *选填* | `./config/UserNicknameMapping.json` | str | |
| `WEB.INDEX_WEB_FILE` | 首页文件位置 | *选填* | | str | |

PS: 配置读取时默认不区分大小写

---

## 各种配置文件的数据格式

1. 配置文件格式：
```yaml
- name: LOG_LEVEL
  values:
    - type: str
      environment: DEV # 此字段可以让配置加载器根据是否与`CONFIG_ENVIRONMENT`环境变量相同来限制加载
      value: DEBUG
    - type: str
      environment: PROD
      value: INFO
    - type: str
      value: INFO

- name: RENDER.MARKDOWN.WKHTMLTOIMAGE_PATH
  values:
    - type: path
      system: Windows # 此字段可以控制该值在指定系统下生效
      value: C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe
    - type: path
      system: Linux
      value: /usr/local/bin/wkhtmltoimage
    - type: path
      system: '*'
      value: ./wkhtmltopdf/wkhtmltoimage
  annotations: 需要写明Wkhhtmltopdf的路径 # 此字段为预留字段，可填写任意内容，与程序运行逻辑无关。
```
JSON同理，配置管理器同时支持JSON和YAML两种格式。

2. api_info文件格式：
```json
[
    {
        "Name": "Deepseek",
        "ApiKeyEnv": "DEEPSEEK_API_KEY",
        "URL": "https://api.deepseek.com",
        "models": [
            {
                "Name": "Deepseek Think Model",
                "Id": "deepseek-reasoner",
                "Uid": "deepseek-reasoner",
                "TaskType": "LLM Chat"
            },
            {
                "Name": "Deepseek Chat Model",
                "Id": "deepseek-chat",
                "Uid": "deepseek-chat",
                "TaskType": "LLM Chat"
            }
        ]
    },
    {
        "Name": "Open AI",
        "ApiKeyEnv": "OPENAI_API_KEY",
        "URL": "https://api.openai.com/v1",
        "models": [
            {
                "Name": "GPT-3.5 Turbo",
                "Id": "gpt-3.5-turbo",
                "Uid": "gpt-3.5-turbo",
                "TaskType": "LLM Chat"
            },
            {
                "Name": "GPT-4",
                "Id": "gpt-4",
                "Uid": "gpt-4",
                "TaskType": "LLM Chat"
            }
        ]
    }
]
```
YAML同理
PS: 目前仅支持LLM Chat的任务类型(系统不会检查该字段，但APIINFO模块会收集相关组)
models中定义该模型的url时会覆盖上层的url
支持兼容OpenAI接口的Chat.Completion模型

3. blacklist.regex (或其他任何RegexChecker处理的文件格式)文件:
```re
[REGEX PARALLEL FILE]
.*example.*
```
PS: 首行必须是`[REGEX PARALLEL FILE]`或`[REGEX SERIES FILE]`，表示该文件是`并行`还是`串行`匹配
之后每行都是`正则表达式`，匹配到的`昵称`或`user_id`的请求将会被**拒绝**

4. UserNicknameMapping.json 文件格式：
```json
{
    "old_nickname": "new_nickname",
    "user_id": "new_nickname"
}
```
`原始昵称`到`模型看到的昵称`的映射关系
键可以是`昵称`或`user_id`，值是`新的昵称`


5. 启动器配置文件格式

```json
{
    "title": "Repeater LLM Chat Backend Starter",
    "process_title": "Repeater LLM Chat Backend",
    "process_exit_title": "Repeater LLM Chat Backend Starter",
    "console_title": "Repeater LLM Chat Backend",
    "exit_title": "Repeater LLM Chat Backend Starter",
    "python_name": {
        "windows": "python",
        "linux": "python3",
        "macos": "python3",
        "jvm": "python3",
        "default": "python3"
    },
    "pip_name": {
        "windows": "pip",
        "linux": "pip3",
        "macos": "pip3",
        "jvm": "pip3",
        "default": "pip3"
    },
    "requirements": [],
    "requirements_file": "requirements.txt",
    "cwd": "./",
    "work_directory": "./",
    "use_venv": true,
    "venv_prompt": "venv",
    "script_name": null,
    "argument": null,
    "restart": false,
    "reselect": false,
    "run_cmd_need_to_ask": true,
    "run_cmd_ask_default_values": {},
    "divider_line_char": "=",
    "inject_environment_variables": {},
    "text_encoding": "utf-8",
    "print_return_code": true,
    "print_runtime": true,
    "automatic_exit": false,
    "allow_print": true
}
```
注：所有选项均为选填，按照需求填写内容即可

---

## Markdown图片渲染样式

| 风格 | 译名 |
| :---: | :---: |
| **`light`** | 亮色 |
| `dark` | 暗色 |
| `red` | 红色 |
| `pink` | 粉色 |
| `blue` | 蓝色 |
| `green` | 绿色 |
| `purple` | 紫色 |
| `yellow` | 黄色 |
| `orange` | 橙色 |
| `dark-red` | 暗红色 |
| `dark-pink` | 暗粉色 |
| `dark-blue` | 暗蓝色 |
| `dark-green` | 暗绿色 |
| `dark-purple` | 暗紫色 |
| `dark-yellow` | 暗黄色 |
| `dark-orange` | 暗橙色 |

---

## 人格预设

| 预设 | 描述 |
| :---: | :---: |
| `default` | 默认 |
| `sister` | 姐姐 |
| `english` | 英语 |
| `japanese` | 日语 |
| `french` | 法语 |
| `russian` | 俄语 |
| `arabic` | 阿拉伯语 |
| `spanish` | 西班牙语 |

(求翻译，我只会中文一个语言)

---

## 变量表

| 变量 | 描述 | 参数 |
| :---: | :---: | :---: |
| `user_id` | 用户ID | 无 |
| `user_name` | 用户名 | 无 |
| `BirthdayCountdown` | 复读机生日倒计时 | 无 |
| `model_type` | 模型类型 | 无 |
| `birthday` | 复读机生日 | 无 |
| `zodiac` | 复读机星座 | 无 |
| `time` | 当前时间 | 无 |
| `age` | 复读机年龄 | 无 |
| `random` | 随机数 | 随机数范围 |
| `randfloat` | 随机浮点数 | 随机数范围 |
| `randchoice` | 随机选择 | 项目内容 |

变量传参方式：
使用空格分割
```Plaintext
{random 1 10}
{randchoice a b c d e}
```

---

## 接口表

| 请求 | URL | 参数类型 | 参数(*可选*) | 描述 | 响应类型 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| `GET` | `/` | 无 | 无 | 获取Index Web | `Web页面` |
| `GET` | `/index.html` | 无 | 无 | (同上) 获取Index Web | `Web页面` |
| `GET` | `/docs` | 无 | 无 | 获取接口文档 | `Web页面` |
| `POST` | `/chat/completion/{user_id:str}` | JSON请求体 | *`message(str)`*<br/>*`user_name(str)`*<br/>*`role(str) = 'user'`*<br/>*`role_name(str)`*<br/>*`model_type(str)`*<br/>*`load_prompt(bool) = true`*<br/>*`save_context(bool) = true`*<br/>*`reference_context_id(str)`*<br/>*`continue_completion(bool)`*  | AI聊天 | `JSON响应对象` 或 `流式Delta对象` |
| `POST` | `/render/{user_id:str}`| JSON请求体 | **`text(str)`**<br/>*`style(str)`*<br/>*`timeout(float)`* | 文本渲染 | `JSON对象` |
| `POST` | `/userdata/variable/expand/{user_id:str}` | JSON请求体 | *`username(str)`*<br/>`text(str)` | 变量解析 | `JSON对象` |
| `GET` | `/userdata/context/get/{user_id:str}` | | | 获取上下文 | `JSON列表` |
| `GET` | `/userdata/context/length/{user_id:str}` | | | 获取上下文长度 | `JSON对象` |
| `GET` | `/userdata/context/userlist` | | | 获取用户列表 | `JSON列表` |
| `POST` | `/userdata/context/withdraw/{user_id:str}` | 表单 | `context_pair_num(int)` | 撤回上下文(按照上下文对) | `JSON对象` |
| `POST` | `/userdata/context/inject/{user_id:str}` | JSON请求体 | `user_content(str)`<br/>`assistant_content(str)` | 注入上下文 | `JSON对象` |
| `POST` | `/userdata/context/rewrite/{user_id:str}` | 表单 | `index(int)`<br/>`content(str)`<br/>*`reasoning_content(str)`* | 重写上下文 | `JSON列表` |
| `GET` | `/userdata/context/branchs/{user_id:str}` | | | 获取用户分支ID列表 | `JSON列表` |
| `GET` | `/userdata/context/now_branch/{user_id:str}` | | | 获取用户当前分支ID | `纯文本` |
| `PUT` | `/userdata/context/change/{user_id:str}` | 表单 | `new_branch_id(str)` | 切换上下文 | `纯文本` |
| `DELETE` | `/userdata/context/delete/{user_id:str}` | | | 删除上下文 | `纯文本` |
| `GET` | `/userdata/prompt/get/{user_id:str}` | | | 获取提示词 | `纯文本` |
| `PUT` | `/userdata/prompt/set/{user_id:str}` | 表单 | `prompt(str)` | 设置提示词 | `纯文本` |
| `GET` | `/userdata/prompt/userlist` | | | 获取用户列表 | `JSON列表` |
| `GET` | `/userdata/prompt/branchs/{user_id:str}` | | | 获取用户分支ID列表 | `JSON列表` |
| `GET` | `/userdata/prompt/now_branch/{user_id:str}` | | | 获取用户当前分支ID | `纯文本` |
| `PUT` | `/userdata/prompt/change/{user_id:str}` | 表单 | `new_branch_id(str)` | 切换提示词 | `纯文本` |
| `DELETE` | `/userdata/prompt/delete/{user_id:str}` | | | 删除提示词 | `纯文本` |
| `GET` | `/userdata/config/get/{user_id:str}` | | | 获取配置 | `JSON对象` |
| `PUT` | `/userdata/config/set/{user_id:str}/{value_type:str}` | 表单 | `key(str)`<br/>`value(Any)` | 设置配置 | `JSON对象` |
| `PUT` | `/userdata/config/delkey/{user_id:str}` | 表单 | `key(str)` | 删除配置 | `JSON对象` |
| `GET` | `/userdata/config/userlist` | | | 获取用户列表 | `JSON列表` |
| `GET` | `/userdata/config/branchs/{user_id:str}` | | | 获取用户分支ID列表 | `JSON列表` |
| `GET` | `/userdata/config/now_branch/{user_id:str}` | | | 获取用户当前分支ID | `纯文本` |
| `PUT` | `/userdata/config/change/{user_id:str}` | 表单 | `new_branch_id(str)` | 切换分支数据 | `纯文本` |
| `DELETE` | `/userdata/config/delete/{user_id:str}` | | | 删除用户配置文件 | `纯文本` |
| `GET` | `/userdata/file/{user_id:str}.zip` | | | 获取用户数据 | `ZIP文件` |
| `GET` | `/request_log` | | | 获取调用日志(不推荐) | `JSON列表` |
| `GET` | `/request_log/list` | | | 获取调用日志(同上) | `JSON列表` |
| `GET` | `/request_log/stream` | | | 流式获取调用日志(推荐) | `JSONL流` |
| `GET` | `/file/render/{file_uuid:str}.png` | | | 获取图片渲染输出文件 | `PNG图片` |
| `POST` | `/admin/reload/apiinfo` | 请求头 | `X-Admin-API-Key(str)` | 刷新API信息 | `JSON对象` |
| `POST` | `/admin/regenerate/admin_key` | 请求头 | `X-Admin-API-Key(str)` | 重新生成管理密钥 | `JSON对象` |
| `POST` | `/admin/configs/reload` | 请求头 | `X-Admin-API-Key(str)` | 重新加载配置 (警告：某些模块会缓存配置结果，这可能导致模块之间的配置差异！) | `JSON对象` |
| `POST` | `/admin/configs/{name:str}/seek/{index:int}` | 请求头 | `X-Admin-API-Key(str)` | 移动指针在指定配置栈中的位置 | `JSON对象` |
| `POST` | `/admin/regenerate/admin_key` | 请求头 | `X-Admin-API-Key(str)` | 重新生成管理密钥 | `JSON对象` |

---

## 用户配置表

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `parset_prompt_name` | `str` | 项目配置中`PROMPT.PARSET_NAME`的值 | 在启动时如果没有检查到自定义提示词，默认选择的预设提示词文件名(此处没有文件后缀，如`default`，实际文件名中会与`PROMPT.DEFAULT_SUFFIX`拼接) |
| `model_uid` | `str` | 项目配置中`MODEL.DEFAULT_MODEL_UID`的值 | 模型UID |
| `temperature` | `float` | 项目配置中`MODEL.DEFAULT_TEMPERATURE`的值 | 模型温度 |
| `top_p` | `float` | 项目配置中`MODEL.DEFAULT_TOP_P`的值 | 模型top_p |
| `max_tokens` | `int` | 项目配置中`MODEL.DEFAULT_MAX_TOKENS`的值 | 模型最大生成长度(OpenAI计划丢弃此参数，但为了兼容性，此处仍然保留) |
| `max_completion_tokens` | `int` | 项目配置中`MODEL.DEFAULT_MAX_COMPLETION_TOKENS`的值 | 模型最大补全长度 |
| `stop` | `list[str]` | 项目配置中`MODEL.DEFAULT_STOP`的值 | 模型停止词 |
| `frequency_penalty` | `float` | 项目配置中`MODEL.DEFAULT_FREQUENCY_PENALTY`的值 | 模型频率惩罚 |
| `presence_penalty` | `float` | 项目配置中`MODEL.DEFAULT_PRESENCE_PENALTY`的值 | 模型存在性惩罚 |
| `auto_shrink_length` | `int` | 项目配置中`MODEL.AUTO_SHRINK_LENGTH`的值 | 自动上下文长度限制的最大值(为0时不自动限制长度) |

---

## 命令表：

\*已被移动至[Repeater NoneBot插件仓库](https://github.com/qeggs-dev/repeater-qq-ai-chatbot-nonebot-plugins)