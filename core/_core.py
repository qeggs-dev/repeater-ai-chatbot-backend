# ==== 标准库 ==== #
import atexit
import asyncio
import traceback
from pathlib import Path
from typing import (
    AsyncIterator,
    Any,
)

# ==== 第三方库 ==== #
import orjson
import aiofiles
from loguru import logger

# ==== 自定义库 ==== #
from .CallAPI import (
    CompletionsAPI
)
from . import Data_Manager
from . import Context_Manager
from . User_Config_Manager import (
    ConfigManager as UserConfigManager,
    UserConfigs
)
from .Core_Response import Response
from .Lock_Pool import AsyncLockPool
from RegexChecker import RegexChecker
from .Global_Config_Manager import ConfigManager
from .Request_User_Info import Request_User_Info
from .ApiInfo import (
    ApiInfo,
)
from . import Request_Log
from .Logger_Init import (
    logger_init
)
from TextProcessors import (
    PromptVP
)
from .Text_Template_Processer import (
    PromptVP_Loader
)
from ._info import (
    __version__,
)

# ==== 本模块代码 ==== #

class Core:
    # region > init
    def __init__(self, max_concurrency: int | None = None):
        # 初始化日志
        logger_init(
            ConfigManager.get_configs().logger,
        )

        # 全局锁(用于获取会话锁)
        self.lock = asyncio.Lock()

        # 初始化用户数据管理器
        self.context_manager = Data_Manager.ContextManager()
        self.prompt_manager = Data_Manager.PromptManager()
        self.user_config_manager = UserConfigManager()

        # 初始化变量加载器
        self.prompt_pv_loader = PromptVP_Loader(
            version = __version__
        )
        # 初始化Client并设置并发大小
        self.api_client = CompletionsAPI.ClientNoStream(
            ConfigManager.get_configs().callapi.max_concurrency
            if max_concurrency is None else max_concurrency
        )
        self.stream_api_client = CompletionsAPI.ClientStream(
            ConfigManager.get_configs().callapi.max_concurrency
            if max_concurrency is None else max_concurrency
        )

        # 初始化API INFO
        self.apiinfo = ApiInfo(
            ConfigManager.get_configs().api_info.case_sensitive
        )
        # 从指定文件加载API数据
        self.apiinfo.load(
            ConfigManager.get_configs().api_info.api_file_path
        )

        # 初始化锁池
        self.namespace_locks = AsyncLockPool()

        # 初始化调用日志管理器
        self.request_log = Request_Log.RequestLogManager(
            ConfigManager.get_configs().request_log.dir,
            auto_save = ConfigManager.get_configs().request_log.auto_save,
        )

        # 黑名单
        self.blacklist: RegexChecker = RegexChecker()
        blacklist_file_path = Path(ConfigManager.get_configs().blacklist.file_path)
        try:
            with open(blacklist_file_path, "r", encoding="utf-8") as f:
                self.blacklist.load_strstream(f)
        except ValueError:
            logger.error("Invalid blacklist file")
        except FileNotFoundError:
            logger.error(f"Blacklist file not found: {blacklist_file_path}")
        self.blacklist_match_timeout: int | None = ConfigManager.get_configs().blacklist.match_timeout

        # 添加退出函数
        def _exit():
            """
            退出时执行的任务
            """
            # 保存调用日志
            if ConfigManager.get_configs().request_log.auto_save:
                self.request_log.save_request_log()
            logger.info("Exiting...")
        
        # 注册退出函数
        atexit.register(_exit)
    # endregion

    # region > get namespace lock
    async def _get_namespace_lock(self, user_id: str) -> asyncio.Lock:
        """
        获取指定用户的命名空间锁

        :param user_id: 用户ID
        :return:该命名空间的锁
        """
        
        return await self.namespace_locks.get_lock(user_id)
    # endregion
    
    # region > nickname mapping
    async def nickname_mapping(self, user_id: str, user_info: Request_User_Info) -> Request_User_Info:
        """
        用户昵称映射

        :param user_id: 用户ID
        :param user_info: 用户信息
        :return: 昵称
        """
        user_nickname_mapping_file_path = Path(ConfigManager.get_configs().user_nickname_mapping.file_path)
        if not user_nickname_mapping_file_path.exists():
            return user_info
        async with aiofiles.open(user_nickname_mapping_file_path, "rb") as f:
            fdata = await f.read()
            try:
                nickname_mapping = orjson.loads(fdata)
            except orjson.JSONDecodeError:
                logger.warning(f"Failed to decode nickname mapping file [{user_nickname_mapping_file_path}]", user_id=user_id)
                nickname_mapping = {}
        
        output = user_info
        if user_info.nickname in nickname_mapping:
            logger.info("User Name [{user_name}] -> [{to_nickname}]", user_id=user_id, user_name = user_info.nickname, to_nickname = nickname_mapping[user_info.nickname])
            output.nickname = nickname_mapping[user_info.nickname]
        elif user_info.username in nickname_mapping:
            logger.info("User Name [{user_name}] -> [{to_nickname}]", user_id=user_id, user_name = user_info.username, to_nickname = nickname_mapping[user_info.username])
            output.username  = nickname_mapping[user_info.username]
        elif user_id in nickname_mapping:
            logger.info("User Name [{user_id}](ID) -> [{to_nickname}]", user_id=user_id, to_nickname = nickname_mapping[user_id])
            output.username = nickname_mapping[user_id]
        
        return output
    # endregion

    # region > get config
    async def get_config(self, user_id: str) -> UserConfigs:
        """
        加载用户配置

        :param user_id: 用户ID
        :return: 用户配置
        """
        config = await self.user_config_manager.load(user_id=user_id)
        return config
    # endregion

    # region > get context
    async def get_context_loader(self) -> Context_Manager.ContextLoader:
        """
        加载上下文
        :return: 上下文加载器
        """
        context_loader = Context_Manager.ContextLoader(
            config=self.user_config_manager,
            prompt=self.prompt_manager,
            context=self.context_manager,
        )
        return context_loader
    
    async def get_context(
            self,
            context_loader: Context_Manager.ContextLoader,
            user_id: str,
            message: str,
            user_name: str,
            role: str = "user",
            role_name: str | None = None,
            load_prompt: bool = True,
            continue_completion: bool = False,
            reference_context_id: str | None = None,
            prompt_vp: PromptVP = PromptVP()
        ) -> Context_Manager.ContextObject:
        """
        获取上下文

        :param context_loader: 上下文加载器
        :param user_id: 用户ID
        :param message: 消息
        :param user_name: 用户名
        :param role: 角色
        :param role_name: 角色名
        :param load_prompt: 是否加载提示
        :param continue_completion: 是否继续完成
        :param reference_context_id: 引用上下文ID
        :param prompt_vp: PromptVP模板解析器
        :return: 上下文对象
        """
        if reference_context_id:
            logger.info(
                "Reference Context ID: {reference_context_id}",
                user_id = user_id,
                reference_context_id = reference_context_id
            )
            context = await context_loader.load(
                user_id = reference_context_id,
                message = message,
                role = role,
                role_name = role_name if role_name else user_name,
                load_prompt = load_prompt,
                continue_completion = continue_completion,
                prompt_vp = prompt_vp
            )
        else:
            logger.info(
                "Current Context ID: {user_id}",
                user_id = user_id,
            )
            context = await context_loader.load(
                user_id = user_id,
                message = message,
                role = role,
                role_name = role_name,
                load_prompt = load_prompt,
                continue_completion = continue_completion,
                prompt_vp = prompt_vp
            )
        return context
    # endregion

    # region > load blacklist
    async def load_blacklist(self, path: str | Path | None = None) -> None:
        """
        加载黑名单

        :param path: 黑名单文件路径
        """
        if not path:
            blacklist_file_path = Path(ConfigManager.get_configs().blacklist.file_path)
        else:
            blacklist_file_path = Path(path)
        
        if blacklist_file_path.exists():
            self.blacklist.clear()
            try:
                async with aiofiles.open(blacklist_file_path, "r") as f:
                    self.blacklist.load(await f.read())
            except ValueError as e:
                logger.warning(f"load blacklist failed: {e}")
    # endregion

    # region > in blacklist
    async def in_blacklist(self, user_id: str) -> bool:
        """
        判断用户是否在黑名单中

        :param user_id: 用户ID
        :return: 是否在黑名单中
        """
        async def _match_blacklist(user_id: str, timeout: int | None) -> bool:
            if timeout is not None:
                return bool(await asyncio.wait_for(asyncio.to_thread(self.blacklist.check, user_id), timeout = timeout))
            else:
                return bool(await asyncio.to_thread(self.blacklist.check, user_id))
        
        try:
            if await _match_blacklist(user_id, self.blacklist_match_timeout):
                logger.info("User in blacklist", user_id = user_id)
                return True
        except asyncio.exceptions.TimeoutError:
            logger.warning("Blacklist match timeout", user_id = user_id)
            return False
        return False
    # endregion

    # region > Chat
    async def chat(
            self,
            message: str,
            user_id: str,
            user_info: Request_User_Info = Request_User_Info(),
            role: str = "user",
            role_name:  str = "",
            print_chunk: bool = True,
            model_uid: str | None = None,
            load_prompt: bool | None = None,
            save_context: bool | None = None,
            reference_context_id: str | None = None,
            continue_completion: bool = False,
            stream: bool = False,
        ) -> Response | AsyncIterator[dict[str, Any]]:
        """
        与模型对话

        :param message: 用户输入的消息
        :param user_id: 用户ID
        :param user_name: 用户名
        :param role: 角色
        :param role_name: 角色名
        :param model_uid: 模型UID
        :param load_prompt: 是否加载提示
        :param print_chunk: 是否打印片段
        :param save_context: 是否保存上下文
        :param reference_context_id: 引用上下文ID
        :param continue_completion: 是否继续完成
        :return: 返回对话结果
        """
        try:
            # 记录开始时间
            task_start_time = Request_Log.TimeStamp()

            # 获取用户锁对象
            lock = await self._get_namespace_lock(user_id)
            
            # 加锁执行
            async with lock:
                logger.info("====================================", user_id = user_id)
                logger.info("Start Task", user_id = user_id)

                # 判断用户是否在黑名单中
                if await self.in_blacklist(user_id):
                    return Response(
                        content = "Error: Sorry, you are in blacklist.",
                        finish_reason_cause = "User in blacklist",
                        status = 403
                    )
                
                if not ConfigManager.get_configs().model.stream and stream:
                    return Response(
                        content = "Error: The streaming response feature is turned off in the server configuration.",
                        finish_reason_cause = "Streaming response feature is turned off",
                        status = 503
                    )

                # 获取配置
                config = await self.get_config(user_id)
                
                # 获取默认模型uid
                if model_uid is None:
                    model_uid: str = config.model_uid or ConfigManager.get_configs().api_info.default_model_uid
                
                # 获取API信息
                apilist = self.apiinfo.find(model_uid = model_uid)
                # 取第一个API
                if len(apilist) == 0:
                    logger.error(
                        "API not found: {model_uid}",
                        user_id = user_id,
                        model_uid = model_uid
                    )
                    output = Response(
                        content = f"API not found: {model_uid}",
                        status = 404
                    )
                    return output
                elif len(apilist) > 1:
                    logger.warning(
                        "Multiple API found: {length}, using the first one",
                        user_id = user_id,
                        length = len(apilist)
                    )
                api = apilist[0]

                # 进行用户名映射
                user_info = await self.nickname_mapping(user_id, user_info)

                # 获取Prompt_vp以展开变量内容
                prompt_vp = self.prompt_pv_loader.get_prompt_vp_ex(
                    user_id = user_id,
                    user_info = user_info,
                    model_uid = model_uid,
                    global_config = ConfigManager.get_configs(),
                    config = config
                )

                # 获取上下文加载器
                context_loader = await self.get_context_loader()

                # 获取上下文
                context = await self.get_context(
                    context_loader = context_loader,
                    user_id = user_id,
                    message = message,
                    user_name = user_info.nickname or user_info.username,
                    role = role,
                    role_name = role_name,
                    load_prompt = load_prompt if load_prompt is not None else config.load_prompt,
                    continue_completion = continue_completion,
                    reference_context_id = reference_context_id,
                    prompt_vp = prompt_vp
                )

                # 如果上下文需要收缩，则进行收缩(为零或类型不对则不进行操作)
                max_context_length = config.context_shrink_limit or ConfigManager.get_configs().context.context_shrink_limit
                if isinstance(max_context_length, int) and max_context_length > 0:
                    if len(context) > max_context_length:
                        logger.info(f"Context length exceeds {max_context_length}, auto shrink", user_id = user_id)
                        try:
                            context.shrink(max_context_length)
                        except Exception as e:
                            logger.error(f"Failed to shrink context: {e}", user_id = user_id)
                            return Response(
                                content = (
                                    "Sorry, I failed to shrink the context.\n"
                                    "This can be caused by an incorrect parameter input.\n"
                                    "Please check that the context field is working properly in your configuration.\n"
                                    "Or whether the Context data does not contain the specified header Role."
                                ),
                                status_code = 400,
                                finish_reason_cause = "shrink_context_failed",
                            )

                user_input = context.last_content
                
                # 创建请求对象
                request = CompletionsAPI.Request()
                # 设置上下文
                request.context = context
                
                # 设置请求对象的API信息
                request.url = api.url
                request.model = api.id
                request.key = api.api_key
                request.timeout = api.timeout
                logger.info(
                    "API URL: {url}",
                    user_id = user_id,
                    url = api.url
                )
                logger.info(
                    "API Model: {parent}/{model_name}",
                    user_id = user_id,
                    parent = api.parent,
                    model_name = api.name
                )

                # 打印上下文信息
                if user_input.content:
                    logger.info(
                        "Message:\n{message}",
                        message = user_input.content,
                        user_id = user_id
                    )
                else:
                    logger.warning(
                        "No message to send",
                        user_id = user_id
                    )

                # 如果有设置用户信息，则打印日志
                if user_info.username:
                    logger.info(
                        "User Name: {username}",
                        user_id = user_id,
                        username = user_info.username
                    )
                if user_info.nickname:
                    logger.info(
                        "User Nickname: {nickname}",
                        user_id = user_id,
                        nickname = user_info.nickname
                    )
                if user_info.gender:
                    logger.info(
                        "User Gender: {gender}",
                        user_id = user_id,
                        gender = user_info.gender
                    )
                if user_info.age:
                    logger.info(
                        "User Age: {age}",
                        user_id = user_id,
                        age = user_info.age
                    )
                if role_name:
                    logger.info(
                        "Role Name: {role_name}",
                        user_id = user_id,
                        role_name = role_name
                    )

                # 设置请求对象的参数信息
                request.user_name = user_info.nickname
                request.temperature = config.temperature or ConfigManager.get_configs().model.default_temperature
                request.top_p = config.top_p or ConfigManager.get_configs().model.default_top_p
                request.frequency_penalty = config.frequency_penalty or ConfigManager.get_configs().model.default_frequency_penalty
                request.presence_penalty = config.presence_penalty or ConfigManager.get_configs().model.default_presence_penalty
                request.max_tokens = config.max_tokens or ConfigManager.get_configs().model.default_max_tokens
                request.max_completion_tokens = config.max_completion_tokens or ConfigManager.get_configs().model.default_max_completion_tokens
                request.stop = config.stop or ConfigManager.get_configs().model.default_stop
                request.stream = ConfigManager.get_configs().model.stream
                request.print_chunk = print_chunk

                # 记录预处理结束时间
                call_prepare_end_time = Request_Log.TimeStamp()

                # 输出 (为了自动填充输出内容)
                output = Response()
                output.model_group = api.parent
                output.model_name = api.name
                output.model_type = api.type.value
                output.model_uid = api.uid
                output.user_raw_input = message
                output.user_input = user_input.content

                # region >> 提交请求
                try:
                    response: CompletionsAPI.Response = CompletionsAPI.Response()
                    if stream:
                        async def generator_wrapper(generator: CompletionsAPI.StreamingResponseGenerationLayer) -> AsyncIterator[CompletionsAPI.Delta]:
                            async for chunk in generator:
                                yield chunk
                        async def post_treatment(response: CompletionsAPI.Response):
                            """
                            包装后处理函数，以传递更多数据
                            """
                            nonlocal output
                            output = await self._post_treatment(
                                output = output,
                                user_id = user_id,
                                response = response,
                                prompt_vp = prompt_vp,
                                user_input = user_input,
                                context_loader = context_loader,
                                task_start_time = task_start_time,
                                reference_context_id = reference_context_id,
                                call_prepare_end_time = call_prepare_end_time,
                                save_context = save_context if save_context is not None else config.save_context,
                            )
                        response_iterator = await self.stream_api_client.submit_Request(
                            user_id = user_id,
                            request = request,
                            response_callback = post_treatment
                        )

                        return generator_wrapper(response_iterator)
                    else:
                        response = await self.api_client.submit_Request(
                            user_id = user_id,
                            request = request
                        )
                        
                        output = await self._post_treatment(
                            output = output,
                            user_id = user_id,
                            response = response,
                            prompt_vp = prompt_vp,
                            user_input = user_input,
                            context_loader = context_loader,
                            task_start_time = task_start_time,
                            reference_context_id = reference_context_id,
                            call_prepare_end_time = call_prepare_end_time,
                            save_context = save_context if save_context is not None else config.save_context,
                        )
                        return output
                
                except CompletionsAPI.Exceptions.APIServerError as e:
                    logger.error(f"API Server Error: {e}")
                    output.content = f"Error:{e}"
                    output.status = 500
                    return output
                
                except CompletionsAPI.Exceptions.BadRequestError as e:
                    logger.error(f"Bad Request Error: {e}")
                    output.content = f"Error:{e}"
                    output.status = 400
                    return output

                except CompletionsAPI.Exceptions.CallApiException as e:
                    logger.error(f"CallAPI Error: {e}")
                    output.content = f"Error:{e}"
                    output.status = 500
                    return output
                # endregion

        except Exception as e:
            traceback_info = traceback.format_exc()
            logger.error("API call failed: \n{traceback}", user_id = user_id, traceback = traceback_info)
            raise
    # endregion
    
    # region > 处理结果
    async def _post_treatment(
        self,
        user_id: str,
        prompt_vp: PromptVP,
        response: CompletionsAPI.Response,
        task_start_time: Request_Log.TimeStamp,
        user_input: Context_Manager.ContentUnit,
        context_loader:Context_Manager.ContextLoader,
        call_prepare_end_time: Request_Log.TimeStamp,
        output: Response = Response(),
        save_context: bool | None = None,
        reference_context_id: str | None = None
    ) -> Response:
        # 补充调用日志的时间信息
        response.calling_log.task_start_time = task_start_time
        response.calling_log.call_prepare_start_time = task_start_time
        response.calling_log.call_prepare_end_time = call_prepare_end_time
        response.calling_log.created_time = response.created

        # 展开模型输出内容中的变量
        response.context.last_content.content = prompt_vp.process(response.context.last_content.content)
        # 记录Prompt_vp的命中情况
        logger.info(f"Prompt Hits Variable: {prompt_vp.hit_var()}/{prompt_vp.discover_var()}({prompt_vp.hit_var() / prompt_vp.discover_var() if prompt_vp.discover_var() != 0 else 0:.2%})", user_id = user_id)

        # 保存上下文
        if save_context:
            context = response.context
            if reference_context_id:
                historical_context = await context_loader.get_context_object(user_id)
                historical_context.append(user_input)
                historical_context.append(response.context.last_content)
                context = historical_context
            await context_loader.save(
                user_id = user_id,
                context = context
            )
        else:
            logger.warning("Context not saved", user_id = user_id)

        # 记录任务结束时间
        response.calling_log.task_end_time = Request_Log.TimeStamp()

        # 记录调用日志
        await self.request_log.add_request_log(response.calling_log)

        # 记录API调用成功
        logger.success(f"API call successful", user_id = user_id)

        # 返回模型输出内容
        output.reasoning_content = response.context.last_content.reasoning_content
        output.content = response.context.last_content.content
        output.create_time = response.created
        output.id = response.id

        output.finish_reason_cause = response.finish_reason_cause
        output.finish_reason_code = response.finish_reason

        return output
    # endregion
    # region > 重新加载API信息
    async def reload_apiinfo(self):
        await self.apiinfo.load_async(Path(ConfigManager.get_configs().api_info.api_file_path))
    # endregion

    # region > 加载指定API INFO文件
    async def load_apiinfo(self, api_info_file_path: Path):
        if not api_info_file_path.exists():
            logger.error(f"API INFO File not found: {api_info_file_path}")
            raise FileNotFoundError(f"File not found: {api_info_file_path}")
        await self.apiinfo.load_async(api_info_file_path)
    # endregion