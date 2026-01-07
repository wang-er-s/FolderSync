# 需求文档

## 简介

文件夹同步系统是一个带图形界面的桌面应用程序，用于管理多个文件夹同步任务。每个任务监控一个源文件夹的变化，并将这些变化实时同步到对应的目标文件夹。系统采用简单的文件覆盖策略，不进行差分比较，确保目标文件夹始终与源文件夹保持一致。应用程序支持打包为exe可执行文件，可设置开机自启动，并能最小化到系统托盘运行。

## 术语表

- **Source_Folder（源文件夹）**: 被监控的文件夹，所有文件变化的起点
- **Target_Folder（目标文件夹）**: 接收同步内容的文件夹
- **Sync_System（同步系统）**: 执行文件夹监控和同步操作的核心系统
- **Sync_Task（同步任务）**: 一个源文件夹到目标文件夹的同步配置
- **File_Event（文件事件）**: 文件系统中的变化事件，包括创建、修改、删除等
- **Sync_Operation（同步操作）**: 将源文件夹的变化应用到目标文件夹的操作
- **GUI（图形界面）**: 用户与系统交互的图形用户界面
- **System_Tray（系统托盘）**: Windows任务栏右下角的通知区域

## 需求

### 需求 1: 文件创建同步

**用户故事:** 作为用户，我希望在源文件夹中创建新文件时，该文件能自动同步到目标文件夹，以便两个文件夹保持一致。

#### 验收标准

1. WHEN 用户在 Source_Folder 中创建新文件 THEN THE Sync_System SHALL 在 Target_Folder 中创建相同的文件
2. WHEN 新文件被创建 THEN THE Sync_System SHALL 复制完整的文件内容到目标位置
3. WHEN 在 Source_Folder 的子目录中创建文件 THEN THE Sync_System SHALL 在 Target_Folder 中创建相应的子目录结构并复制文件

### 需求 2: 文件修改同步

**用户故事:** 作为用户，我希望修改源文件夹中的文件时，修改能自动同步到目标文件夹，以便目标文件夹始终包含最新内容。

#### 验收标准

1. WHEN 用户修改 Source_Folder 中的文件 THEN THE Sync_System SHALL 用新内容覆盖 Target_Folder 中的对应文件
2. WHEN 文件被修改 THEN THE Sync_System SHALL 完整复制文件内容而不进行差分比较
3. WHEN 文件修改事件被检测到 THEN THE Sync_System SHALL 在合理的时间内（5秒内）完成同步操作

### 需求 3: 文件删除同步

**用户故事:** 作为用户，我希望删除源文件夹中的文件时，目标文件夹中的对应文件也被删除，以保持两个文件夹的一致性。

#### 验收标准

1. WHEN 用户从 Source_Folder 中删除文件 THEN THE Sync_System SHALL 从 Target_Folder 中删除对应的文件
2. WHEN 用户删除 Source_Folder 中的目录 THEN THE Sync_System SHALL 删除 Target_Folder 中对应的目录及其所有内容
3. IF 目标文件不存在 THEN THE Sync_System SHALL 记录警告信息并继续运行

### 需求 4: 文件夹结构同步

**用户故事:** 作为用户，我希望源文件夹的目录结构变化能自动同步到目标文件夹，以便维护完整的文件夹层次结构。

#### 验收标准

1. WHEN 用户在 Source_Folder 中创建新目录 THEN THE Sync_System SHALL 在 Target_Folder 中创建相同的目录
2. WHEN 用户在 Source_Folder 中删除目录 THEN THE Sync_System SHALL 删除 Target_Folder 中对应的目录
3. WHEN 用户在 Source_Folder 中移动文件或目录 THEN THE Sync_System SHALL 在 Target_Folder 中执行相同的移动操作

### 需求 5: 实时监控

**用户故事:** 作为用户，我希望系统能实时监控源文件夹的变化，以便变化能够立即被检测和同步。

#### 验收标准

1. WHEN Sync_System 启动 THEN THE Sync_System SHALL 开始监控 Source_Folder 的所有文件系统事件
2. WHEN File_Event 发生 THEN THE Sync_System SHALL 在事件发生后立即检测到该事件
3. WHILE Sync_System 运行 THEN THE Sync_System SHALL 持续监控文件系统事件直到被停止
4. WHEN 监控过程中发生错误 THEN THE Sync_System SHALL 记录错误信息并继续监控

### 需求 6: 初始同步

**用户故事:** 作为用户，我希望系统启动时能执行一次完整的初始同步，以确保目标文件夹与源文件夹一致。

#### 验收标准

1. WHEN Sync_System 首次启动 THEN THE Sync_System SHALL 执行完整的初始同步操作
2. WHEN 执行初始同步 THEN THE Sync_System SHALL 复制 Source_Folder 中的所有文件和目录到 Target_Folder
3. WHEN 初始同步进行中 THEN THE Sync_System SHALL 覆盖 Target_Folder 中已存在的文件
4. WHEN 初始同步完成 THEN THE Sync_System SHALL 开始实时监控模式

### 需求 7: 错误处理

**用户故事:** 作为用户，我希望系统能妥善处理各种错误情况，以便同步过程稳定可靠。

#### 验收标准

1. IF 源文件夹不存在 THEN THE Sync_System SHALL 报告错误并拒绝启动
2. IF 目标文件夹不存在 THEN THE Sync_System SHALL 创建目标文件夹
3. IF 文件复制失败（权限不足、磁盘空间不足等）THEN THE Sync_System SHALL 记录详细错误信息并继续处理其他事件
4. IF 文件被占用无法访问 THEN THE Sync_System SHALL 重试操作最多3次，每次间隔1秒
5. WHEN 发生错误 THEN THE Sync_System SHALL 输出清晰的错误消息，包含文件路径和错误原因

### 需求 8: 日志记录

**用户故事:** 作为用户，我希望系统能记录同步操作的日志，以便我了解同步状态和排查问题。

#### 验收标准

1. WHEN Sync_Operation 执行 THEN THE Sync_System SHALL 记录操作类型、文件路径和时间戳
2. WHEN 错误发生 THEN THE Sync_System SHALL 记录错误级别的日志信息
3. WHEN Sync_System 启动或停止 THEN THE Sync_System SHALL 记录系统状态变化
4. THE Sync_System SHALL 支持配置日志级别（DEBUG、INFO、WARNING、ERROR）

### 需求 9: 图形界面管理

**用户故事:** 作为用户，我希望通过简洁的图形界面管理同步任务，以便直观地配置和监控多个文件夹同步。

#### 验收标准

1. THE GUI SHALL 显示所有已配置的同步任务列表
2. WHEN 用户点击添加按钮 THEN THE GUI SHALL 显示对话框让用户选择源文件夹和目标文件夹
3. WHEN 用户选择文件夹路径 THEN THE GUI SHALL 使用文件夹选择对话框而不是手动输入
4. THE GUI SHALL 为每个任务显示源路径、目标路径和当前状态（运行中/已停止）
5. WHEN 用户选择一个任务 THEN THE GUI SHALL 提供启动、停止和删除操作按钮
6. THE GUI SHALL 使用简洁清晰的布局，避免复杂的设计

### 需求 10: 多任务管理

**用户故事:** 作为用户，我希望能同时运行多个同步任务（如A→B、C→D），以便一次性管理所有需要同步的文件夹对。

#### 验收标准

1. THE Sync_System SHALL 支持同时运行多个独立的同步任务
2. WHEN 用户添加新任务 THEN THE Sync_System SHALL 将任务配置保存到本地配置文件
3. WHEN 应用程序启动 THEN THE Sync_System SHALL 加载所有已保存的任务配置
4. THE Sync_System SHALL 为每个任务独立维护监控状态和日志
5. WHEN 一个任务发生错误 THEN THE Sync_System SHALL 继续运行其他任务

### 需求 11: 系统托盘功能

**用户故事:** 作为用户，我希望应用程序能最小化到系统托盘，以便在后台运行而不占用任务栏空间。

#### 验收标准

1. WHEN 用户点击窗口最小化按钮 THEN THE GUI SHALL 最小化到系统托盘而不是任务栏
2. WHEN 用户点击托盘图标 THEN THE GUI SHALL 显示或隐藏主窗口
3. WHEN 用户右键点击托盘图标 THEN THE GUI SHALL 显示上下文菜单，包含"显示窗口"和"退出"选项
4. THE System_Tray SHALL 显示应用程序图标
5. WHEN 同步任务发生重要事件或错误 THEN THE System_Tray SHALL 显示通知消息

### 需求 12: 开机自启动

**用户故事:** 作为用户，我希望应用程序能设置开机自启动，以便系统启动后自动开始同步工作。

#### 验收标准

1. THE GUI SHALL 提供"开机自启动"复选框选项
2. WHEN 用户启用开机自启动 THEN THE Sync_System SHALL 在Windows注册表中添加启动项
3. WHEN 用户禁用开机自启动 THEN THE Sync_System SHALL 从Windows注册表中移除启动项
4. WHEN 系统启动时应用程序自动运行 THEN THE GUI SHALL 直接最小化到系统托盘

### 需求 13: 可执行文件打包

**用户故事:** 作为用户，我希望应用程序能打包成单个exe文件，以便在没有Python环境的Windows系统上直接运行。

#### 验收标准

1. THE Sync_System SHALL 能够使用PyInstaller或类似工具打包成exe文件
2. WHEN 打包完成 THEN THE 可执行文件 SHALL 包含所有必要的依赖库
3. THE 可执行文件 SHALL 在没有安装Python的Windows系统上正常运行
4. THE 可执行文件 SHALL 包含应用程序图标

### 需求 14: 配置持久化

**用户故事:** 作为用户，我希望应用程序能保存我的配置，以便下次启动时自动加载所有同步任务。

#### 验收标准

1. WHEN 用户添加、修改或删除任务 THEN THE Sync_System SHALL 立即保存配置到本地文件
2. THE Sync_System SHALL 使用JSON格式存储配置文件
3. WHEN 应用程序启动 THEN THE Sync_System SHALL 从配置文件加载所有任务
4. IF 配置文件不存在或损坏 THEN THE Sync_System SHALL 创建新的空配置文件

### 需求 15: 优雅停止

**用户故事:** 作为用户，我希望能够安全地停止同步任务和退出应用程序，以便在需要时干净地关闭程序。

#### 验收标准

1. WHEN 用户从托盘菜单选择退出 THEN THE Sync_System SHALL 停止所有运行中的同步任务
2. WHEN 停止信号被接收 THEN THE Sync_System SHALL 完成当前正在进行的同步操作
3. WHEN 系统退出 THEN THE Sync_System SHALL 保存所有配置并记录退出日志
4. WHEN 用户停止单个任务 THEN THE Sync_System SHALL 只停止该任务而不影响其他任务
