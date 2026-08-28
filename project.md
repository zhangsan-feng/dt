# 当前项目功能

_platform/douyin/
    douyin_detail.py 当前已回退到 Git HEAD 版本，负责原有抖音视频/图文详情接口请求和数据处理。
    douyin_adapter.py 对外只保留 douyin_adapter_api 和 douyin_adapter_browser；视频、笔记、图集走浏览器监听，直接把浏览器真实请求头交给数据处理器，不自定义 Cookie；用户页和直播等走 API 适配器。
    __init__.py 重新导出 data_handler 中的数据处理函数，兼容原有 API 模块导入。
    sign/__init__.py 保留旧接口签名逻辑，并为详情页提供独立的新版签名入口和 Cookie 参数整理。
    sign/a_bogus.py 调用 Spider_Dy_comment2 的纯 JavaScript 签名器生成当前版本 a_bogus。
    browser/douyin_detail_browser.py 由 douyin_adapter_browser 调用，负责 detail 参数和业务处理；通用浏览器调用由 browser_request_capture.py 提供。
    sign/ms_token.py 请求 msToken 服务并从响应头或 Set-Cookie 提取 token，同时记录脱敏状态日志。
    当前详情入口恢复原有请求流程；纯 HTTP、纯 a_bogus 和浏览器桥接代码仍保留在工作区供后续选择。
    详情数据处理只下载 MP3、MP4 和 PNG；默认关闭 only_audio/only_video/only_image 过滤，因此三类媒体都会下载。
config/
    Configuration 提供项目路径、下载目录、平台 Cookie、代理和媒体下载选项；已替代旧 application.entity.config_entity。
    旧 application/ 目录及其 API、service、实体和 XHR Hook 已按一次性重构要求移除；下载记录不再由旧 application 持久化。
Spider_Dy_comment2/reverse_a_bogus/
    pure_a_bogus.js 及 core/ 提供 1.0.1.19 版本纯 a_bogus 算法实现。
_platform/douyin/browser/
    browser_request_capture.py 提供通用浏览器请求捕获，负责 Browser 实例、桥接脚本调用和参数校验。
    douyin_detail_browser.py 负责 detail 的 aweme_id 替换、响应解析、签名日志和数据处理器调用。
    douyin_post_browser.py 负责用户主页 URL 解析、作品列表接口捕获、aweme_list 校验和作品数据处理，支持通过 max_cursor 指定请求游标。
    browser_detail_capture.mjs 提供完整详情浏览器抓取：先通过 page.goto 初始化源页面，再在 BDM 签名前改写 detail 请求参数，由页面默认流程生成签名、发送请求并读取响应。
    `DOUYIN_HTTP_ONLY` 不再影响已回退的 douyin_detail.py 入口。

utils/
    browser.py 提供 BrowserObject；browser_call_js 在浏览器页面上下文执行 JS 函数，browser_request_listener 打开页面并监听指定响应接口，browser_request 获取页面主请求和主响应；三者均使用临时隔离浏览器环境。
    browser.py 的 run_bridge_json() 是通用桥接脚本执行入口，抖音专用逻辑不放在 utils 中。
    browser_call_js.mjs 负责启动临时隔离浏览器并通过 page.evaluate 执行页面 JS 函数文件。
    browser_request_listener.mjs 负责启动临时隔离浏览器、注册 response 监听器并返回匹配接口的请求和响应对象。
    browser_request.mjs 使用 Node.js Patchright 访问指定 URL，返回主请求和主响应的 URL、方法、请求头、请求体、状态码、响应头和响应体。

静态分析结论
    Spider_Dy_comment/bdm.js:6428-6444 的 `var m = n.apply(d, e)` 是字节码解释器的通用函数调用分发点。
    在 `e[0] == "a_bogus" && e.length == 2` 条件下，实测 n 是 URLSearchParams.prototype.append，d 是 URLSearchParams，e 是 `["a_bogus", 已生成的最终字符串]`。
    因此该断点只能观察 a_bogus 的最终写入，不能代表算法入口；Spider_Dy_comment2 的生成链是 query canonicalization -> dhzx/SM3 -> UA/屏幕指纹 -> payload96 -> mask/RC4-like finalize。
    历史验证：只带 aid 和 aweme_id 的最小纯 HTTP 请求曾返回 200 JSON 且含 aweme_detail；带不匹配的纯 a_bogus 会得到 200 空 text/plain。

浏览器签名调用点
    `XMLHttpRequest` 是通用入口，不是 XML DOM。`Spider_Dy_comment/bdm.js:6358-6368` 的 `D -> n -> X` 启动 BDM VM，随后进入 `d()` 解释器；`Spider_Dy_comment/bdm.js:6442` 的 `n.apply(d, e)` 仅负责分发 VM 中的 native 调用。
    当前 1.0.1.19 handler 的 VM 字节码长度为 238：`a === 150` 对应使用 query 序列化结果和请求上下文生成签名并准备写入 `s[9]`，`a === 168` 对应 `searchParams.append("a_bogus", s[9])`。detail、comment、social/count 等 XHR 共用这条 BDM 处理链。

浏览器请求捕获验证
    `fetch_detail_with_browser` 已验证可直接在浏览器内读取 detail 响应：状态 `200`、类型 `application/json`、包含 `aweme_detail`；因此详情链路当前使用浏览器请求，不依赖 Python 重放。
    2026-08-28 批量短链验证：6 个视频/图文短链均成功解析并返回 detail；`AxBinfaYolc` 虽标注为 live，实际重定向到 `iesdouyin.com/share/slides/7637410157160769251/`，详情返回 3 张图片，当前判定为图集。

当前项目计划：page.goto 初始化后改写参数并继续浏览器默认 detail 流程
    1. `douyin_detail_browser.py` 通过通用捕获模块和 `page.goto` 打开源 `browser_aweme_id` 页面，初始化抖音前端和 BDM 环境。
    2. 在页面初始化阶段包裹 `XMLHttpRequest.open` 的后续 BDM wrapper 赋值。
    3. 对 detail 请求只替换调用方指定的目标 `aweme_id`，保持其余原始 query 和编码不变。
    4. 调用页面原有 XHR/BDM 流程生成 `a_bogus`、发送请求；Python 不创建 XHR、不拼签名、不重放请求。
    5. 在浏览器内按可选 response_field 校验响应后交给 Python；不再保留浏览器单独提取 `a_bogus` 的备用入口。

    执行结果
    计划已完成。详情入口使用源页面 `page.goto` + BDM 签名前目标 `aweme_id` 替换；普通 detail 和源/目标 ID 不同的 detail 均返回 `200 application/json`，响应含目标 `aweme_detail`，`a_bogus` 长度为 180。Python 只接收浏览器结果，不重放请求。
    最新职责拆分：`douyin_detail_browser.py` 的 `handle_detail_with_browser()` 统一负责浏览器详情抓取、`aweme_detail` 校验、请求头提取和现有数据处理器调用；`douyin_adapter.py` 只负责链接分流和提取 `aweme_id`，不再内嵌 `_browser_detail`。
    最新模块拆分：`browser_request_capture.py` 负责 Browser/桥接脚本调用、通用请求参数校验和响应捕获；`douyin_detail_browser.py` 仅保留 detail 参数替换、响应业务解析和数据处理入口；`browser/__init__.py` 继续提供统一公共导出。

    2026-08-28 清理：当前业务流程均使用浏览器完整请求捕获或纯算法签名，已删除浏览器单独提取 a_bogus 的备用桥接脚本及其 Python 导出入口。
    2026-08-28 浏览器环境调整：`browser_detail_capture.mjs` 已移除持久化 Profile，始终使用临时隔离 Context；如需携带登录态，仍可通过 `DOUYIN_COOKIE` 注入。
    2026-08-28 运行目录清理：已删除整个 `.runtime` 目录，包括旧 Profile 和 `js-reverse-mcp-cdp*` 运行目录。
    2026-08-28 运行环境调整：通用浏览器桥接工具已统一改用临时隔离 Context，项目不再依赖 `.runtime` 目录。
