# PDF Merge Tool

一个本地 Windows PDF 合并工具，支持：

- 直接打开窗口，手动添加多个 PDF 并调整顺序后合并。
- 资源管理器里选中多个 PDF，右键直接打开合并工具。
- 右键多选时自动把多个启动进程汇总到同一个窗口里。

## 文件说明

- `pdf_merge_tool.pyw`: 主程序。
- `start_pdf_merge_tool.bat`: 双击启动工具。
- `install_context_menu.ps1`: 安装 PDF 右键菜单。
- `uninstall_context_menu.ps1`: 卸载 PDF 右键菜单。
- `requirements.txt`: 依赖列表。

## 使用方法

### 1. 直接启动

双击 `start_pdf_merge_tool.bat`。

首次真正执行合并时，如果本机没有 `pypdf`，Python 版会提示自动安装到当前目录下的 `vendor` 文件夹，不需要管理员权限。

### 2. 安装右键菜单

在当前目录打开 PowerShell，执行：

```powershell
PowerShell -ExecutionPolicy Bypass -File .\install_context_menu.ps1
```

安装完成后，在资源管理器中：

- 选中一个或多个 PDF。
- 右键点击。
- 选择 `Merge PDFs`。

程序会自动把选中的 PDF 收集到同一个窗口中，方便继续调整顺序并保存为一个新文件。

### 3. 卸载右键菜单

```powershell
PowerShell -ExecutionPolicy Bypass -File .\uninstall_context_menu.ps1
```

## 说明

- 当前实现依赖 `pypdf` 做 PDF 合并。
- 当前 `exe` 版本会优先使用已打包的 `pypdf`；如果没打进去，会尝试调用本机的 `py` 或 `python` 自动安装到 `vendor` 目录。
- 如果后续已经准备好 `vendor\pypdf`，打包脚本会自动把整个 `vendor` 目录一起带进 `exe`。
- 重新打包前，建议先执行 `python -m pip install -r requirements.txt`，这样 `.spec` 里的 `pypdf` 收集规则才能生效。
- 如果你的环境不能联网安装依赖，也可以手动执行：

```powershell
python -m pip install --target .\vendor pypdf
```

- 工具不会修改原始 PDF，只会生成新的合并文件。
