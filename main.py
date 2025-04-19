import os
from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
from pkg.platform.types import *
import json
import time
import aiohttp
from plugins.KawaiiDashboard.tool.drawer import  draw

# 注册插件
@register(name="Kawaii-Dashboard", description="更可爱的服务器基本信息展示面板，使用!sys展示", version="0.1", author="Hanschase")
class MyPlugin(BasePlugin):
    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.ap = host.ap
        self.start_time = time.time()
        if not os.path.exists("plugins/KawaiiDashboard/config"):
            os.makedirs("plugins/KawaiiDashboard/config")
        if not os.path.exists("plugins/KawaiiDashboard/config/bot_qq.json"):
            with open("plugins/KawaiiDashboard/config/bot_qq.json", "w",encoding='utf-8') as f:
                self.data = {
                    "QQ" : "Please enter your bots QQ",
                    "name" : "BOT"
                }
                json.dump(self.data, f, indent=4)
        else:
            try:
                with open("plugins/KawaiiDashboard/config/bot_qq.json", "r",encoding='utf-8') as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                self.ap.logger.error("bot_qq.json decoding failed,please check the plugins/KawaiiDashboard/config/bot_qq.json or delete it")

    # 异步初始化
    async def initialize(self):
        await self.get_qlogo()

    @handler(PersonCommandSent)
    @handler(GroupCommandSent)
    async def get_cmd(self,ctx: EventContext):
        if ctx.event.command == "sys":
            ctx.prevent_default()
            ctx.prevent_postorder()
            runtime = self.get_runtime()
            img64 = draw(self.ap, self.data['name'], runtime)
            await ctx.reply(MessageChain([Image(base64 = img64)]))

    async def get_qlogo(self):
        bot_qq = self.data["QQ"]
        url = f'http://q1.qlogo.cn/g?b=qq&nk={bot_qq}&s=100'
        save_path = 'plugins/KawaiiDashboard/tool/resources/images/qlogo.jpg'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    # 创建保存图片的目录（如果不存在）
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    # 以二进制写入模式打开文件
                    with open(save_path, 'wb') as file:
                        # 异步地将响应内容写入文件
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            file.write(chunk)
        except Exception as e:
            self.ap.logger.error(e)

    def get_runtime(self):
        # 模拟函数执行的耗时操作
        time.sleep(5)
        # 获取当前时间
        current_time = time.time()
        # 计算时间差（秒）
        elapsed_seconds = current_time - self.start_time
        # 将时间差转换为小时
        runtime = round(elapsed_seconds / 3600, 0)
        return runtime

    # 插件卸载时触发
    def __del__(self):
        pass
