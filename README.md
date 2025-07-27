# 一键获取 google_lens 有效 cookie 的脚本

---

## 使用方式
- 根据具体需求选择本地引擎还是远程引擎
- 运行 `main.py` 脚本一键获取

---

## 注意事项

### 1. 桌面端
- 确认已安装 **chrome 浏览器**

### 2. docker
- 确认已安装 **selenium 官方镜像** `selenium/standalone-chrome`
- 配置 `remote_addr` 默认值 `http://localhost:4444/wd/hub`
- 如果 `remote_addr` 为公网地址，请将 `localhost` 改为具体域名
- 服务器配置越差，`timeout` 值应该越高
