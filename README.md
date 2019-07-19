# 功能
* 发送钉钉过消息到webhook机器人。
* 支持所有钉钉消息类型。

# 安装
```bash
1. 安装requests
pip install requests

2. 安装该模块
pip install dingtalk-webhook
```

# 使用
```
import dingtalk
access_token = 'xxxxxxx...xxx' # 创建webhook机器人时的access_token
dt = dingtalk.DingTalk(access_token)
dt.send_text(text='测试消息', at_all=True)
```
