# Git LFS 安装位置说明

## `git lfs install` 命令特性
`git lfs install` 是一个**全局命令**，它会将 Git LFS 配置到你的全局 Git 设置中，因此：

1. ✅ **可以在任何目录下执行**，包括你的项目目录 `e:\github_project\fufan-chat-api`
2. ✅ 执行一次后，所有 Git 仓库都会自动启用 LFS 支持
3. ✅ 不需要在每个仓库中重复执行

## 建议的操作流程

1. **先安装 Git LFS**（可以在任何目录）：
   ```bash
   git lfs install
   ```

2. **然后在合适的位置克隆模型**：
   - 建议在项目的 `models` 目录下执行：
     ```bash
     cd e:\github_project\fufan-chat-api\models
     git clone https://www.modelscope.cn/ZhipuAI/chatglm3-6b.git
     ```
   - 或者直接在项目根目录克隆，然后移动到 models 目录

## 注意事项
- 确保已经安装了 Git LFS 客户端（可以通过 `git lfs --version` 检查）
- 克隆模型时会自动使用 LFS 下载大文件
- 如果遇到问题，可以尝试在模型目录内再次执行 `git lfs install`（局部启用）