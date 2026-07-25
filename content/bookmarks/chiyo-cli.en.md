---
title: Chiyo CLI
date: 2026-07-25
description: A collection of small, focused, search-oriented command-line tools
---

> Reach files, projects, applications, bookmarks, and other known objects faster from the terminal.

Chiyo CLI is a personal command-line toolbox for macOS. It brings common workflows together through one simple pattern:

```text
Search → Pick → Action
```

Each tool solves one focused problem while remaining small, readable, customizable, and composable with other command-line programs.

## Why Chiyo CLI?

Modern applications often bundle many features, settings pages, background services, and interface layers. They can be powerful, but they may also feel unnecessarily heavy when all you need is one simple action.

Chiyo CLI takes a different approach:

- One tool solves one problem
- Workflows share a consistent terminal interface
- Code stays small, transparent, and auditable
- Tools can be installed and configured independently
- Commands compose naturally with the rest of the terminal

The goal is not to replace graphical applications. The terminal instead acts as a lightweight, unified layer connecting different workflows.

## Features

### Core tools

| Command | Description |
| --- | --- |
| `chiyo` | Show the dashboard, manage tools, and diagnose the local setup |
| `gop` | Search for files or directories, then enter or open them |
| `proj` | Search Git projects and change to the selected project directory |
| `s` | Build and open web search URLs |
| `ws` | Enter, create, or manage tmux workspaces |
| `def` | Look up definitions and translations |
| `app` | Search installed macOS applications and launch one |
| `bm` | Search Safari bookmarks and open URLs |

### Optional integrations

| Command | Description |
| --- | --- |
| `agd` | Search Org Agenda items and open their source locations |
| `zo` | Search Zotero items and open entries or PDFs |

## Quick start

### 1. Install

After cloning the repository, run this command from the project root:

```sh
./install.sh
```

The installer links the `chiyo` bootstrap command to `~/.local/bin/chiyo`. Make sure that directory is included in `PATH`:

```sh
export PATH="$HOME/.local/bin:$PATH"
```

### 2. Enable zsh integration

Add the following line to `~/.zshrc`:

```zsh
eval "$(chiyo init zsh)"
```

Reload the configuration:

```sh
source ~/.zshrc
```

### 3. Initialize configuration and install tools

```sh
chiyo config init --all --append
chiyo install s ws gop proj
```

### 4. Check the local setup

```sh
chiyo doctor
```

## Examples

```sh
# Search with a configured search engine
chiyo run s gh chiyo-cli

# Enter a tmux workspace
chiyo run ws cli-tools

# Find and launch an application
chiyo run app safari

# Search Safari bookmarks
chiyo run bm github

# Look up a definition
chiyo run def epistemic

# Find and enter a Git project
chiyo shell proj cli-tools

# Find and open a file or directory
chiyo shell gop docs

# Open the Chiyo dashboard
chiyo
```

Once a tool has been installed, its command can also be used directly:

```sh
s gh chiyo-cli
ws cli-tools
app safari
proj cli-tools
```

## Requirements

- macOS
- Python 3.9 or later
- [fd](https://github.com/sharkdp/fd)
- [ripgrep](https://github.com/BurntSushi/ripgrep)
- [fzf](https://github.com/junegunn/fzf)
- zsh for shell integration and commands that change the current directory
- tmux when using `ws`
- Zotero when using `zo`

Some tools read Safari bookmarks, application metadata, or configured filesystem roots. If necessary, grant Full Disk Access to your terminal application in macOS Privacy & Security settings.

## Configuration

Chiyo CLI uses two configuration files:

```text
~/.config/chiyo-cli/config.toml
~/.config/chiyo-cli/tools.toml
```

- `config.toml` contains Chiyo infrastructure settings, such as enabled tools.
- `tools.toml` contains tool-specific settings.

Generate explicit default configuration with:

```sh
# Initialize Chiyo and all currently enabled tools
chiyo config init --all --write

# Add missing settings without replacing existing values
chiyo config init --all --append

# Replace the configuration for one tool
chiyo config init s --force
```

The generated files are intended to be edited. You can customize search roots, command aliases, and individual tool behavior.

## Custom tools

User-defined tools live in:

```text
~/.config/chiyo-cli/tools/
```

A small tool can be a single Python file:

```text
~/.config/chiyo-cli/tools/paper.py
```

Larger tools can use a directory:

```text
~/.config/chiyo-cli/tools/zotero/
├── tool.py
├── local_api.py
├── sqlite_source.py
└── item.py
```

Custom tools share the same configuration, `fzf` selection interface, shell completion, installation, documentation, and diagnostics infrastructure as built-in tools.

User tools are executable Python code. Only install and run tools from sources you trust.

## Management commands

```sh
# List available tools
chiyo tool list

# Enable or disable a tool
chiyo tool enable TOOL
chiyo tool disable TOOL

# Install or uninstall a tool command
chiyo install TOOL
chiyo uninstall TOOL

# Read a tool's documentation
chiyo doc TOOL

# Diagnose dependencies and configuration
chiyo doctor
```

## Development

Run the complete test suite:

```sh
make test
```

GitHub Actions runs the same tests on macOS.

Focused bug fixes, documentation improvements, tests, and small new tools are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Project status

Chiyo CLI is currently in the `v0.x` alpha stage and uses a development installation model. The core commands are intended to remain small and understandable, but configuration and installation details may change before a stable release.

Because installation uses symbolic links, moving the repository requires running the installer again:

```sh
./install.sh
```

## Security

Chiyo CLI runs locally, but some tools may read configured filesystem roots, Safari bookmarks, macOS application metadata, Zotero data, and local Chiyo configuration.

The project includes AI-assisted implementation and refactoring and should not yet be considered fully manually audited. See [SECURITY.md](SECURITY.md) for details.

## Design principle

> Build the smallest tool that solves the problem well enough.

Chiyo CLI is not intended to become a large application or package manager. Each tool should remain small, focused, easy to understand, easy to customize, and easy to compose.

## License

This project is available under the [MIT License](LICENSE).
