# 功能

* 支持所有钉钉消息类型。
* 支持加签的安全设置。

# Python版本

`Python 3.6+`

# 安装

```bash
1. 安装requests
pip install requests

2. 安装该模块
pip install dingtalk-webhook
```

# 使用

```python
import dingtalk

access_token = 'xxxxxxx...xxx'  # 创建webhook机器人时产生的access_token
secret = 'SECxxxxxxx'  # 如果安全设置没有勾选加签，可不用设置该参数
dt = dingtalk.DingTalk(access_token=access_token, secret=secret)
dt.send_text(text='测试消息', at_all=True)
```
