
# 🚀 自动发版部署工具（Auto Deploy Platform）

一个为 **后端微服务项目** 提供“一键构建 + 一键上传 + 一键部署”的自动化发版工具。
支持 Windows 环境运行，提供 GUI，可对接远程服务器，自动完成构建、打包、上传、备份、部署、日志查看等全流程。

---

## ✨ 核心特性

* **一键构建 JAR 包 / Node 项目**
* **自动设置 JAVA_HOME（支持 JDK8 / JDK17 切换）**
* **自动执行 Maven 构建（可定制 settings.xml / 本地仓库）**
* **自动 SSH 登录服务器执行部署**
* **自动上传文件并备份旧版本**
* **自动查看实时日志（tail -F）**
* **GUI 可视化操作，全流程可视**
* **部署失败自动提示，错误日志可查看**
* **完整可配置 `.env` 文件**

---

## 🖼️ 工具界面预览（GUI）

> 支持一键点击开始发版，所有构建日志实时显示。

（可在此处加入你的截图）

---

## 📦 项目结构

```
auto-deploy/
│── main.py                # 程序入口
│── gui/                   # UI 部分
│── core/                  # 核心发版逻辑
│── config/                # 配置管理（含 .env 读取）
│── ssh/                   # SSH & SFTP 管理
│── utils/                 # 工具类
│── assets/                # 图标与资源文件
│── .env.example           # 配置示例
│── requirements.txt       # 依赖
│── README.md
```

---

## ⚙️ 配置说明（.env）

你需要在项目根目录创建 `.env`，参考如下：

```env
# ========================
# Maven / Java 配置
# ========================
JAVA_HOME=D:\Application\Java\jdk-17
MAVEN_CMD=D:\APP\Apache-maven-3.9.11-bin\bin\mvn
MAVEN_SETTINGS=D:\APP\Apache-maven-3.9.11-bin\conf\settings.xml
MAVEN_REPO=D:\APP\Apache-maven-3.9.11-bin\unicom_repo

# ========================
# 项目构建路径
# ========================
LOCAL_PROJECT_PATH=D:\workspace\project
LOCAL_JAR_OUTPUT=target\project.jar

# ========================
# 服务器信息
# ========================
SERVER_HOST=192.168.1.10
SERVER_PORT=22
SERVER_USER=root
SERVER_PASSWORD=123456
SERVER_DEPLOY_PATH=/data/project
SERVER_BACKUP_PATH=/data/backup

# ========================
# 日志路径
# ========================
REMOTE_LOG_FILE=/data/project/logs/app.log
```

---

## 🔧 使用方式

### 1️⃣ 启动程序

```bash
python main.py
```

### 2️⃣ 在 GUI 中配置：

* 本地项目路径
* Maven settings 路径
* JDK 版本
* SSH 信息
* 远程部署路径
* 日志路径

---

## 🚀 示例发版流程

1. **检测配置**

   * JAVA_HOME 是否正确
   * Maven settings 文件存在
   * VPN 是否已连接
   * 服务器可连通

2. **构建后端服务**
   自动执行：

   ```
   "mvn clean install -DskipTests -s xxx -Dmaven.repo.local=xxx"
   ```

   自动捕获构建错误，如：

   * JDK 版本不匹配
   * settings.xml 找不到
   * 仓库权限问题
   * 依赖下载失败

3. **上传构建产物至服务器**
   通过 SFTP 自动上传，并执行远程备份：

   ```
   mv project.jar project-20250101.jar.bak
   ```

4. **远程部署**
   自动执行 shell：

   ```
   stop.sh
   start.sh
   ```

5. **自动查看日志（tail -F）**

   * 不自动关闭
   * 用户点击右上角 X 才退出
   * 释放所有资源防止占用

该流程解决传统发版耗时长、重复步骤多、容易遗漏的痛点。

---

## 🧰 常见问题（FAQ）

### ❓ 构建时报“JAVA_HOME 不正确”

请确认 `.env` 内的 JDK 目录包含 `bin/java.exe`。

### ❓ settings.xml 找不到

确保填写了绝对路径，如：

```
D:\APP\Apache-maven-3.9.11-bin\conf\settings.xml
```

### ❓ 日志窗口关闭后，程序还会占用吗？

不会。
日志查看模块已加入 safe-exit，确保释放 SSH/SFTP 资源。

---

## 🛠️ 开发与贡献

欢迎提交 PR 或 Issue！

---

## 📄 开源协议

MIT License

---
