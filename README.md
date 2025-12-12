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
 - MD图片渲染：可以将回复以图片的形式渲染发送，降低其妨碍用户正常聊天的程度
 - 命令别名触发：不管是缩写还是全文，都可以触发命令操作
 - 用户自治设计：用户可以自己管理自己的所有用户数据
 - 多预设人设：复读机支持多预设人设，用户可以自由选择自己喜欢的人设进行对话
> 注：拟人化并非复读机的赛道，复读机不对拟人化需求做过多保证，如有需要请自行引导或编写提示词。

## 注意事项:
 - 本服务由一位 `16岁自学开发者`(现在17了) 使用AI辅助开发，公益项目，如果你愿意捐赠，可以在机器人的**QQ空间**中找到赞赏码以支持项目运营(或是支持开发者)。
 - 使用者需确认生成内容的合法性，并自行承担使用本服务可能产生的风险。
 - 如果你觉得这个Bot非常好用，请去看一下[`Deepseek`](https://www.deepseek.com/)的官网吧，这个Bot最初就是基于他们的模型API文档开发的。

---

## License
这个项目基于[MIT License](LICENSE)发布。

---

### 依赖项:
| Name              | Version  | License                              | License Link                                                                        | Where it is used                    | Reasons                               |
|-------------------|----------|--------------------------------------|-------------------------------------------------------------------------------------|-------------------------------------|---------------------------------------|
| Markdown          | 3.8.2    | BSD 3-Clause License                 | [BSD-3-Clause](https://github.com/Python-Markdown/markdown/blob/master/LICENSE.md)  | `Markdown`                          | Parses Markdown text into HTML        |
| pyyaml            | 6.0.2    | MIT License                          | [MIT](https://github.com/yaml/pyyaml/blob/main/LICENSE)                             | `API` & `ConfigManager`             | Read configuration file               |
| aiofiles          | 24.1.0   | Apache Software License              | [Apache-2.0](https://github.com/Tinche/aiofiles/blob/main/LICENSE)                  | `core.DataManager`                  | Asynchronous file support             |
| environs          | 14.2.0   | MIT License                          | [MIT](https://github.com/sloria/environs/blob/main/LICENSE)                         | `run_repeater.py` & `ConfigManager` | Support for environment variables     |
| fastapi           | 0.115.13 | MIT License                          | [MIT](https://github.com/fastapi/fastapi/blob/master/LICENSE)                       | `API`                               | Build API                             |
| httpx             | 0.28.1   | BSD License                          | [BSD-3-Clause](https://github.com/encode/httpx/blob/master/LICENSE.md)              | `core.FuncerClient`                 | Asynchronous HTTP client              |
| playwright        | 1.56.0   | Apache-2.0                           | [Apache-2.0](https://github.com/Microsoft/playwright-python)                        | `Markdown_Render`                   | Render HTML as an image               |
| loguru            | 0.7.3    | MIT License                          | [MIT](https://github.com/Delgan/loguru/blob/master/LICENSE)                         | *Entire Project*                    | Logging                               |
| openai            | 1.90.0   | Apache Software License              | [Apache-2.0](https://github.com/openai/openai-python/blob/main/LICENSE)             | `core.CallAPI`                      | Call the OpenAI API                   |
| orjson            | 3.10.18  | Apache Software License; MIT License | [Apache-2.0](https://github.com/ijl/orjson/blob/master/LICENSE-APACHE) / [MIT](https://github.com/ijl/orjson/blob/master/LICENSE-MIT) | `core.DataManager` | High-performance JSON  resolution |
| pydantic          | 2.11.7   | MIT License                          | [MIT](https://github.com/pydantic/pydantic/blob/main/LICENSE)                       | `core.ConfigManager` & `API`        | Simple and convenient data validation |
| python-multipart  | 0.0.20   | Apache Software License              | [Apache-2.0](https://github.com/Kludex/python-multipart/blob/master/LICENSE.txt)    | `core.DataManager` & `API`          | Support for form data                 |
| uvicorn           | 0.34.3   | BSD License                          | [BSD-3-Clause](https://github.com/Kludex/uvicorn/blob/main/LICENSE.md)              | `run_repeater.py`                   | Run FastAPI                           |
| numpy             | 2.3.4    | BSD License                          | [BSD-3-Clause](https://github.com/numpy/numpy/blob/main/LICENSE.txt)                | *Entire Project*                    | Speed up batch computing of data      |
| python-box        | 7.3.2    | MIT License                          | [MIT](https://github.com/cdgriffith/Box/blob/master/LICENSE)                        | `core.Global_Config_Manager`        | Mixed configuration files             |
| tzdata            | 2025.2   | Apache Software License              | [Apache-2.0](https://github.com/python/tzdata/blob/master/LICENSE)                  | `core.Text_Template_Processer`      | Get timezone information              |

---

## 安装部署

**推荐Python3.11以上版本安装**
> PS: 复读机可能会兼容Python3.11以前的版本
> 但我们并未对其进行过测试
> 此处3.11为开发环境版本

### 自动安装

1. 将项目克隆到本地
2. 进入项目目录
5. 运行`run.py`启动器 (详情请查看[Sloves_Starter](https://github.com/qeggs-dev/Sloves_Starter))

### 手动安装

1. 将项目克隆到本地
2. 进入项目目录
3. 执行`python3 -m venv .venv`创建虚拟环境
4. 执行`.venv/bin/activate`激活虚拟环境(Windows下则是`.venv\Scripts\activate`)
5. 执行`pip install -r requirements.txt`安装依赖
6. 执行`python3 run_repeater.py`启动服务

PS: `run.py`启动器会在完成所有操作后启动主程序，而这只需要你保证你的配置正确
并且每一次你都可以通过启动器来启动程序

---

## 环境变量表

| 环境变量 | 描述 | 是否必填 | 默认值(*示例值*) |
| :---: | :---: | :---: | :---: |
| `*API_KEY` | API_Key (具体变量名由`API_INFO.API_FILE_PATH`指向 文件中`ApiKeyEnv`字段的名称) | **必填** | *\*可从[Deepseek开放平台/API Keys](https://platform.deepseek.com/api_keys)页面获取* |
| `ADMIN_API_KEY` | 管理员API_Key (用于Repeater的管理员操作身份验证) | **选填但生产环境建议填写</br>如果填写的不够随机，程序会报错</br>建议先执行一次取生成的API_Key** | *\*自动生成随机 API Key* |
| `CONFIG_DIR` | 配置文件夹路径 | **选填** | `./config/project_config` |
| `CONFIG_FORCE_LOAD_LIST` | 配置文件强制加载列表(元素为配置文件路径) | **选填** | *`["./config/project_config/configs.json", "./config/project_config/configs2.json"]`* |
| `HOST` | 服务监听的IP | **选填** | `0.0.0.0` |
| `PORT` | 服务监听的端口 | **选填** | `8080` |
| `WORKERS` | 服务监听的进程数 | **选填** | `1` |
| `RELOAD` | 是否自动重启 | **选填** | `false` |

## 配置文件

**默认值：**
```json
{
    "api_info": {
        // API INFO 配置

        // API INFO 文件路径
        "api_file_path": "./config/api_info.json",
        // 默认使用的模型uid
        // 这里需要填写你在api_info.json中配置的模型uid
        // 如果用户没有指定模型，则使用这个模型进行响应
        // uid匹配默认是不分大小写的
        // 不建议使用默认UID，因为chat指定的太过宽泛
        // 建议在部署时，自己定一个或是根据厂商和模型的名字来定一个
        // 比如deepseek-chat之类的
        "default_model_uid": "chat",
        // 在匹配UID时是否启用大小写敏感
        "case_sensitive": false
    },
    "blacklist": {
        // 黑名单配置

        // 黑名单文件路径
        // 嗯这个文件只需要在开头写一个`[REGEX PARALLEL FILE]`
        // 然后下面每一行一个正则表达式就行了
        // 如果没有你也可以不写
        // 但是文件头必须有
        "file_path": "./config/blacklist.regex",

        // 黑名单匹配超时时间，单位为秒
        "match_timeout": 10.0 // 匹配超时时间，单位为秒
    },
    "callapi": {
        // CallAPI 配置

        // 协程池最大并发数
        "max_concurrency": 1000
    },
    "context": {
        // Context 配置

        // 自动上下文长度裁剪
        // 当你聊天过长时，可能会超过模型上下文窗口限制
        // 这个设置可以让Repeater为你自动裁剪最久的消息
        // 让你可以继续聊天
        // 默认值：null，表示不启用
        // 你可以在这里填写一个整数，表示自动裁剪的长度，单位为字符数量
        "context_shrink_limit": null
    },
    "logger": {
        // Logger 配置

        // Log 文件输出路径
        "file_path": "./logs/repeater-log-{time:YYYY-MM-DD_HH-mm-ss.SSS}.log",
        // Log 级别
        "level": "INFO",
        // Log 轮换设置
        "rotation": "10 MB",
        // Log 保留设置
        "retention": "7 days",
        // Log 过期后执行的操作
        "compression": "zip"
    },
    "model": {
        // 你可以微调默认的用户model参数
        // 如果用户没有定义模型参数，则你这里定义的参数取请求API

        // 默认模型温度，更高的温度意味着下一个词更高的不确定性
        "default_temperature": 1.0,
        // 默认模型Top_P，指越大在采样时考虑的词汇越多
        "default_top_p": 1.0,
        // 默认模型最大生成长度(兼容)
        "default_max_tokens": 4096,
        // 默认模型最大生成长度
        "default_max_completion_tokens": 4096,
        // 默认模型频率惩罚，值越高模型越不容易出现重复内容
        // 惩罚程度按照频率增加，如果该值为负则是奖励模型输出重复内容
        "default_frequency_penalty": 0.0,
        // 默认模型存在惩罚，值越高模型越不容易出现重复内容
        // 惩罚程度只要存在就一直不变，如果该值为负则是奖励模型输出重复内容
        "default_presence_penalty": 0.0,
        // 默认模型停止符
        // 当模型输出到停止符内容时，停止生成
        "default_stop": [],
        // 默认模型是否流式输出
        // 注意：这里只是在告诉Repeater应该使用什么方式调用模型接口
        // 如果模型不支持流式生成，调用可能会报错
        // 且该参数不能决定/chat/completion接口是否流式输出
        // 如果这里为false
        // 那么/chat/completion接口调用时stream参数能且只能为false
        // 此时如果客户端请求流式响应，会返回503错误
        // 请求控制台和日志不会显示生成过程，也不会有chunk统计数据
        // 如果这里为true
        // 那么/chat/completion接口调用时stream参数可以为true或false
        // 且控制台和日志会打印当前chunk，并生成chunk统计数据
        "stream": true
    },
    "prompt_template": {
        // template 提示词文本模板展开器配置
        // 注：此选项不会改变实际的其他系统内容，而只会改变模板展开器中的变量

        // 模板展开器中显示的程序版本
        "version": "",
        // 模板展开器中显示的 Bot 名称
        "name": "Repeater",
        // Bot 的生日
        "birthday": {
            "day": 28,
            "month": 6,
            "year": 2024
        },
        "time": {
            // 时间偏移量，单位为小时
            // 如果为0，则是UTC时间
            // 此参数仅影响文本展开器的部分变量
            "time_offset": 0.0
        }
    },
    "prompt": {
        // Prompt 配置

        // 告诉Prompt加载器预设提示词目录的路径
        "dir": "./config/prompt/presets",
        // 预设提示词文件的后缀名
        "suffix": ".md",
        // 预设提示词文件应该用什么编码打开
        "encoding": "utf-8",
        // 如果用户没设置路由到其他提示词，应该使用哪一个提示词
        "preset_name": "default"
    },
    "render": {
        // Markdown 图片渲染器配置

        // 图片等待多少时间后被删除（URL有效时间）
        "default_image_timeout": 60.0,
        // Markdown 到 HTML 渲染配置
        "markdown": {
            // 默认样式
            "default_style": "light",
            // 样式文件目录
            "styles_dir": "./configs/styles",
            // 样式文件应该用什么编码打开
            "style_file_encoding": "utf-8",
            // HTML 模板文件目录
            "html_template_dir": "./configs/html_templates",
            // HTML 模板文件应该用什么编码打开
            "html_template_file_encoding": "utf-8",
            // 默认使用的 HTML 模板文件
            "default_html_template": "default.html",
            // Markdown 预处理器配置
            "preprocess_map": {
                // Before 预处理器
                // 处理 Markdown 数据
                "before": {},
                // After 预处理器
                // 处理 HTML 数据
                "after": {}
            },
            // 在 HTML 中添加的标题
            "title": "Repeater Image Generator"
        },
        "to_image": {
            // 最多允许在一个浏览器中打开多少个页面
            "max_pages_per_browser": 5,
            // 最多允许同时打开的浏览器数量
            "max_browsers": 2,
            // 浏览器类型
            "browser_type": "msedge",
            // 浏览器是否为无头模式
            "headless": true,
            // 输出图片的目录
            "output_dir": "./workspace/temp/render",
            // 输出图片的格式
            "output_suffix": ".png",
            // 浏览器的可执行文件路径
            "executable_path": "",

            // 浏览器窗口大小
            "width": 1200,
            "height": 600
        }
    },
    "request_log": {
        // /chat/completion 端口的请求日志

        // 请求日志的保存目录
        "dir": "./workspace/request_log",
        // 是否自动保存请求日志
        "auto_save": true,
        // 缓存请求日志的等待时间
        "debonce_save_wait_time": 1200.0,
        // 请求日志缓存的队列最大长度
        "max_cache_size": 1000
    },
    "server": {
        // 服务器配置
        // 这里的几个字段为null或不填则会使用环境变量中定义的配置
        // 如果这里填写了内容，那么这里的内容会覆盖环境变量中的值

        // 监听的IP
        "host": null,
        // 监听的端口
        "port": null,
        // 工作进程数量
        "workers": null,
        // 是否在文件发生变动时自动重启
        "reload": null
    },
    "static": {
        // 静态文件配置

        // README.md 文件的路径
        "readme_file_path": "./README.md",
        // 静态文件目录
        "static_dir": "./static"
    },
    "user_config_cache": {
        // 用户配置缓存配置

        // 读取配置后等待多少秒后从缓存删除
        "downgrade_wait_time": 600.0,
        // 保存配置到缓存后等待多少秒后从关闭缓存并写入
        "debounce_save_wait_time": 1000.0
    },
    "user_data": {
        // 用户数据配置

        // 用户数据的保存目录
        "dir": "./workspace/data/user_data",
        // 分支数据使用的目录名称
        "branches_dir_name": "branches",
        // 元数据文件名称
        "metadata_file_name": "metadata.json",

        // 是否缓存
        // 这里的两个字段同时支持bool和cache_data结构
        // 如果为bool，则该值对所有数据类型生效
        // 如果为cache_data结构，则该值对指定的数据类型生效
        // 警告：缓存系统仍未进行可行性与稳定性验证，请谨慎使用

        // 是否缓存元数据
        "cache_medadata": false,
        // 是否缓存用户数据
        "cache_data": {
            "context": false,
            "prompt": false,
            "config": false
        }
    },
    "user_nickname_mapping": {
        // 用户昵称映射配置

        // 昵称映射文件路径
        // 有些用户的昵称可能会让模型陷入循环
        // 可以用这个文件来映射它们到一个安全的昵称
        "file_path": "./config/user_nickname_mapping.json"
    },
    "web": {
        // Web配置

        // Index Web 文件路径
        // 如果不填写这个项目，那么默认会使用内置的索引页面
        "index_web_file": "./static/index.html"
    }
}
```

PS: 配置读取时键名不区分大小写，但建议使用小写格式
配置管理器会递归扫描环境变量`CONFIG_DIR`下的所有json/yaml文件
并按照路径的字符串顺序排列，后加载配置中的字段会覆盖之前的配置
你也可以使用环境变量`CONFIG_FORCE_LOAD_LIST`来强制按照指定的顺序加载配置

当你不知道如何配置时，直接运行程序
它可以给你自动生成一份默认配置文件

配置文件全部都有默认值，你只需要填写你需要的部分即可
比如：
``` json
{
    "api_info": {
        // 必须要定义模型，否则Repeater可能会不知道你要给谁发请求
        "api_file_path": "./config/api_info.json",
        // 这里非常建议你填写，因为默认的`chat`真的很容易冲突
        "default_model_uid": "deepseek-chat"
    },
    "logger": {
        // 建议填写，默认的是DEBUG，它的输出有点多
        "level": "INFO"
    },
    "render": {
        "to_image": {
            // 也建议填写，除非你对 playwright 安装了独立的浏览器
            "executable_path" : "" // 这里填写你安装的任意浏览器可执行文件的路径
        }
    }
}
```

---

## 各种配置文件的数据格式

1. 配置文件格式：
参考[配置文件](#配置文件)

2. api_info文件格式：
```json
[
    {
        "name": "Deepseek", // 显示在日志上的模型组名称
        "api_key_env": "DEEPSEEK_API_KEY", // 这里填写API_KEY的环境变量名称
        "url": "https://api.deepseek.com", // 这里填写API的URL
        "models": [
            {
                "name": "Deepseek Think Model", // 显示在日志上的模型名称
                "id": "deepseek-reasoner", // 面向API厂商的模型ID
                "uid": "deepseek-reasoner", // 面向Repeater和用户的模型ID
                "type": "chat" // 模型类型，用于告诉Repeater这个模型可以干什么
            },
            {
                "name": "Deepseek Chat Model",
                "id": "deepseek-chat",
                "uid": "deepseek-chat",
                "url": "https://api.deepseek.com/chat", // 如果模型有单独的URL，可以单独填写
                "type": "chat"
            }
        ]
    },
    {
        "name": "Open AI",
        "api_key_env": "OPENAI_API_KEY",
        "url": "https://api.openai.com/v1",
        "models": [
            {
                "name": "GPT-3.5 Turbo",
                "id": "gpt-3.5-turbo",
                "uid": "gpt-3.5-turbo",
                "type": "chat"
            },
            {
                "name": "GPT-4",
                "id": "gpt-4",
                "uid": "gpt-4",
                "timeout": 240.0, // 模型单独设置的超时时间可以覆盖模型组提供的全局设置
                "type": "chat"
            }
        ],
        "timeout": 120.0 // 请求的超时设置，单位为秒
    }
]
```
YAML同理
PS: 目前仅支持LLM Chat的任务类型(系统不会检查该字段，但APIINFO模块会收集相关组)
models中定义该模型的url时会覆盖上层的url
目前type=chat的表示该模型为兼容OpenAI接口的Chat.Completion模型
暂不支持其他类型的模型

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
这可以避开异常的昵称导致模型出错

---

## Markdown图片渲染样式

| 风格 | 译名 |
| --- | :---: |
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
| `legacy` | 旧版亮色 |
| `legacy-dark` | 旧版暗色 |
| `legacy-red` | 旧版红色 |
| `legacy-pink` | 旧版粉色 |
| `legacy-blue` | 旧版蓝色 |
| `legacy-green` | 旧版绿色 |
| `legacy-purple` | 旧版紫色 |
| `legacy-yellow` | 旧版黄色 |
| `legacy-orange` | 旧版橙色 |
| `legacy-dark-red` | 旧版暗红色 |
| `legacy-dark-pink` | 旧版暗粉色 |
| `legacy-dark-blue` | 旧版暗蓝色 |
| `legacy-dark-green` | 旧版暗绿色 |
| `legacy-dark-purple` | 旧版暗紫色 |
| `legacy-dark-yellow` | 旧版暗黄色 |
| `legacy-dark-orange` | 旧版暗橙色 |

PS: `light`为默认风格，无需指定
颜色风格默认在 `./configs/style` 文件夹下

---

## 模板展开系统

模板展开系统用于将模板中的变量替换为实际值
这里用单大括号括起来的内容叫变量
例如 `{user_name}` 表示用户名
模板展开系统会自动将变量替换为实际值，例如 `{user_name}` 可能会被替换为 `张三`
而在Repeater内，模板展开器是允许注册函数变量的
所以你可以给变量传参，按照Shell的风格进行
例如 `{randchoice 1 2 3}` 表示随机选择1、2、3中的一个
`{copytext "hello" 5 " "}` 表示将`hello`复制5次，并用空格连接

### 变量表

| 变量 | 描述 | 参数 |
| :---: | :---: | :---: |
| `age` | Bot年龄 | 无 |
| `nickname` | 昵称 | 无 |
| `birthday` | 生日 | 无 |
| `user_id` | 用户ID | 无 |
| `zodiac` | Bot星座 | 无 |
| `botname` | Bot名称 | 无 |
| `user_name` | 用户名 | 无 |
| `user_age` | 用户年龄 | 无 |
| `model_uid` | 模型类型 | 无 |
| `user_info` | 用户信息 | 无 |
| `user_gender` | 用户性别 | 无 |
| `generate_uuid` | 生成UUID | 无 |
| `time` | 当前时间 | 格式字符串(str) |
| `randchoice` | 随机选择 | 抽取内容(*str) |
| `reprs` | 显示对象的字符串表示 | 任何内容(*Any) |
| `random` | 随机数 | 随机数下限(int)，随机数上下限(int) |
| `birthday_countdown` | 生日倒计时 | 启用详细信息(bool) |
| `random_matrix` | 0~1随机矩阵 | 矩阵行数(int)，矩阵列数(int) |
| `randfloat` | 随机浮点数 | 随机数下限(float)，随机数上下限(float) |
| `copytext` | 重复文本 | 重复文本(str)， 重复次数(int), 间隔符(str) |
| `text_matrix` | 文本矩阵 | 重复文本(int)，列数(int)，行数(int)，间隔符(str)，换行符(str) |

### 变量传参方式

优先使用shell格式分割，失败时再按空格分割
```Plaintext
{random 1 10}
{randchoice a b c d e}
{copytext a 5 " "}
{text_matrix a 5 5 " " "<esc:"\n">"}
```

### 转义序列

```Plaintext
转义处理器：<esc:"">
<esc:"\0">空字符
<esc:"\n">换行符
<esc:"\r">回车符
<esc:"\t">制表符
<esc:"\a">响铃符
<esc:"\b">退格符
<esc:"\f">换页符
<esc:"\v">垂直制表符
<esc:"\e">转义符
<esc:"\xhh">二位16进制字符
<esc:"\uHHHH">四位16进制字符
<esc:"\UHHHHHHHH">八位16进制字符
<esc:"\oOOO">8进制字符
<esc:"\dDDD">10进制字符
```
PS: 转义必须保证转义处理器一字不漏，否则会以普通文本输出
引号必须存在，它和其他部分共同组成转义序列的边界

---

## 接口表

| 请求 | URL | 参数类型 | 参数(*可选*) | 描述 | 响应类型 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| `GET` | `/` | 无 | 无 | 获取Index Web | `Web页面` |
| `GET` | `/index.html` | 无 | 无 | (同上) 获取Index Web | `Web页面` |
| `GET` | `/docs` | 无 | 无 | 获取接口文档 | `Web页面` |
| `POST` | `/chat/completion/{user_id:str}` | JSON请求体 | *`message(str)`*<br/>*`user_name(str)`*<br/>*`role(str) = "user"`*<br/>*`role_name(str)`*<br/>*`model_uid(str)`*<br/>*`load_prompt(bool) = true`*<br/>*`save_context(bool) = true`*<br/>*`reference_context_id(str)`*<br/>*`continue_completion(bool)`*  | AI聊天 | `JSON响应对象` 或 `流式Delta对象` |
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
| `PUT` | `/userdata/config/set/{user_id:str}/{key:str}` | 表单 | `type(str)`<br/>`value(Any)` | 设置配置 | `JSON对象` |
| `PUT` | `/userdata/config/set/{user_id:str}` | 表单 | `config(JSON对象)` | 批量配置设置 | `JSON对象` |
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
| `GET` | `/version` | | | 获取版本信息 | `JSON对象` |
| `GET` | `/version/api` | | | 获取API版本信息 | `纯文本` |
| `GET` | `/version/core` | | | 获取核心版本信息 | `纯文本` |

---

## 用户配置

```json
{
    // (str) 时区设置，用于控制模板展开器中的{time}变量
    "timezone": null,
    // (str) 预设提示词，用于快速路由定义好的提示词文件
    "parset_prompt_name": null,
    // (str) 模型UID，用于指定消息处理模型
    "model_uid": null,
    // (float) 模型温度参数，温度越高模型输出的随机性就越高
    "temperature": null,
    // (float) 模型Top-p参数，Top-p参数越低，模型在采样的时候就更倾向于使用更高概率的词
    "top_p": null,
    // (int) 最大生成长度，模型新生成的文本长度不能超过这个值
    "max_tokens": null,
    // (int) 模型最大生成长度，模型生成文本长度不能超过这个值
    "max_completion_tokens": null,
    // (list[str]) 模型停止生成文本的标志词，当生成的文本中包含这些词时，模型会停止生成
    "stop": null,
    // (float) 模型频率惩罚参数，频率惩罚参数越高，模型在生成文本时越倾向于使用新的词
    "frequency_penalty": null,
    // (float) 模型存在性惩罚参数，存在性惩罚参数越高，模型越倾向于讨论新话题
    "presence_penalty": null,
    // (int) 定义上下文问的极限字数，Repeater会以一对消息为单位去删除过多的部分。
    "context_shrink_limit": null,
    // (str) 渲染风格，用于指定文本转图片时的CSS样式文件
    "render_style": null,
    // (str) 渲染HTML模板，用于指定文本转图片时的HTML模板文件
    "render_html_template": null,
    // (str) 渲染HTML标题，用于指定文本转图片时的图片标题
    "render_title": null,
    // (bool) 是否加载提示词，此选项会被API接口中传入的load_prompt参数覆盖
    "load_prompt": true,
    // (bool) 是否保存上下文，此选项会被API接口中传入的save_context参数覆盖
    "save_context": true
}
```
PS: 这里用户配置为null的表示使用主配置里写的默认值

---

## 命令表：

\*已被移动至[Repeater NoneBot插件仓库](https://github.com/qeggs-dev/repeater-qq-ai-chatbot-nonebot-plugins)

---

## 相关仓库

[Sloves_Starter](https://github.com/qeggs-dev/Sloves_Starter)