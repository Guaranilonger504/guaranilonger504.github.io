---
title: Chiyo CLI
description: 一组小巧、专注、以搜索为核心的命令行工具
---

# Chiyo CLI

> 更快地从终端找到文件、项目、应用、书签和其他已知对象。

Chiyo CLI 是一个面向 macOS 的个人命令行工具箱。它将常用工作流统一为一个简单的模式：

```text
搜索 → 选择 → 执行动作
```

每个工具只解决一个明确的问题，并尽量保持小巧、易读、可定制，也可以与其他命令行程序组合使用。

## 为什么做这个项目

现代应用通常包含大量功能、设置页面、后台服务和复杂界面。它们很强大，但完成一个简单任务时，有时也显得过于沉重。

Chiyo CLI 采用另一种思路：

- 一个工具只处理一个问题
- 使用统一的终端交互方式
- 保持代码简单、透明、可审查
- 支持按需安装和个性化配置
- 让不同工具能够自然组合

它并不试图取代图形界面，而是把终端作为连接不同工作流的统一入口。

## 功能概览

### 核心工具

| 命令 | 功能 |
| --- | --- |
| `chiyo` | 查看工具面板、管理安装并检查环境 |
| `gop` | 搜索文件或目录，然后进入或打开 |
| `proj` | 搜索 Git 项目并进入项目目录 |
| `s` | 构建并打开网页搜索 |
| `ws` | 创建、进入或管理 tmux 工作区 |
| `def` | 查询单词释义或翻译 |
| `app` | 搜索并启动 macOS 应用 |
| `bm` | 搜索并打开 Safari 书签 |

### 可选集成

| 命令 | 功能 |
| --- | --- |
| `agd` | 搜索 Org Agenda 项目并打开源文件位置 |
| `zo` | 搜索 Zotero 条目并打开记录或 PDF |

## 快速开始

### 1. 安装

克隆仓库后，在项目根目录运行：

```sh
./install.sh
```

安装脚本会把 `chiyo` 引导命令链接到 `~/.local/bin/chiyo`。请确保该目录已经加入 `PATH`：

```sh
export PATH="$HOME/.local/bin:$PATH"
```

### 2. 配置 zsh 集成

将下面这行加入 `~/.zshrc`：

```zsh
eval "$(chiyo init zsh)"
```

然后重新加载配置：

```sh
source ~/.zshrc
```

### 3. 初始化配置并安装工具

```sh
chiyo config init --all --append
chiyo install s ws gop proj
```

### 4. 检查本地环境

```sh
chiyo doctor
```

## 使用示例

```sh
# 使用指定搜索引擎搜索
chiyo run s gh chiyo-cli

# 进入 tmux 工作区
chiyo run ws cli-tools

# 搜索并启动应用
chiyo run app safari

# 搜索 Safari 书签
chiyo run bm github

# 查询释义
chiyo run def epistemic

# 搜索并进入 Git 项目
chiyo shell proj cli-tools

# 搜索并打开文件或目录
chiyo shell gop docs

# 打开 Chiyo 面板
chiyo
```

安装工具后，也可以直接使用对应命令：

```sh
s gh chiyo-cli
ws cli-tools
app safari
proj cli-tools
```

## 系统要求

- macOS
- Python 3.9 或更高版本
- [fd](https://github.com/sharkdp/fd)
- [ripgrep](https://github.com/BurntSushi/ripgrep)
- [fzf](https://github.com/junegunn/fzf)
- zsh，用于 shell 集成和需要改变当前目录的命令
- tmux，仅在使用 `ws` 时需要
- Zotero，仅在使用 `zo` 时需要

某些功能需要读取 Safari 书签、应用元数据或指定的文件系统目录。必要时，请在 macOS 的“隐私与安全性”设置中，为终端应用授予“完全磁盘访问权限”。

## 配置

Chiyo CLI 使用两个配置文件：

```text
~/.config/chiyo-cli/config.toml
~/.config/chiyo-cli/tools.toml
```

- `config.toml` 保存 Chiyo 本身的基础设置，例如已启用的工具。
- `tools.toml` 保存各个工具的独立设置。

生成默认配置：

```sh
# 初始化 Chiyo 和当前启用工具的配置
chiyo config init --all --write

# 补充缺少的配置，不覆盖已有值
chiyo config init --all --append

# 重置指定工具的配置
chiyo config init s --force
```

配置文件是为用户编辑而设计的，你可以修改搜索目录、命令别名和工具行为。

## 自定义工具

用户工具存放在：

```text
~/.config/chiyo-cli/tools/
```

小型工具可以只使用一个 Python 文件：

```text
~/.config/chiyo-cli/tools/paper.py
```

复杂工具也可以采用目录结构：

```text
~/.config/chiyo-cli/tools/zotero/
├── tool.py
├── local_api.py
├── sqlite_source.py
└── item.py
```

自定义工具与内置工具共享配置加载、`fzf` 选择界面、命令补全、安装、文档和诊断能力。

需要注意：用户工具是可执行的 Python 代码，只应安装和运行你信任的工具。

## 常用管理命令

```sh
# 查看可用工具
chiyo tool list

# 启用或禁用工具
chiyo tool enable TOOL
chiyo tool disable TOOL

# 安装或卸载工具命令
chiyo install TOOL
chiyo uninstall TOOL

# 查看工具文档
chiyo doc TOOL

# 检查环境和配置
chiyo doctor
```

## 开发

运行完整测试：

```sh
make test
```

项目使用 GitHub Actions 在 macOS 环境中运行相同的测试。

欢迎提交聚焦的错误修复、文档改进、测试以及符合“小而专注”理念的新工具。更多信息请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 当前状态

Chiyo CLI 目前处于 `v0.x` Alpha 阶段，采用开发式安装。工具的核心行为会尽量保持简单、清晰，但配置格式和安装机制在稳定版本发布前仍可能变化。

由于安装使用符号链接，移动仓库后需要重新运行：

```sh
./install.sh
```

## 安全说明

Chiyo CLI 在本地运行，但部分工具可能读取配置的文件系统目录、Safari 书签、macOS 应用元数据、Zotero 数据和 Chiyo 本地配置。

项目包含 AI 辅助生成和重构的代码，目前仍应视为尚未完成全面人工审计。详细说明请参阅 [SECURITY.md](SECURITY.md)。

## 设计原则

> 构建一个足够解决问题的最小工具。

Chiyo CLI 不追求成为庞大的应用或包管理器。它希望让每个工具都保持小巧、专注、易于理解、易于修改和易于组合。

## 许可证

本项目采用 [MIT License](LICENSE)。
