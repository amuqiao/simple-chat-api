# ModelScope snapshot_download 参数说明

## cache_dir
- **功能**: 指定ModelScope下载和缓存模型文件的默认目录
- **作用**: 作为模型文件的临时存储位置，ModelScope会将原始下载的文件保存在这里
- **特点**: 
  - 通常用于系统级的缓存管理
  - 如果不指定，会使用默认的缓存路径（通常在用户目录下的.cache/modelscope）
  - 可以通过此参数集中管理所有下载的模型缓存

## local_dir
- **功能**: 指定下载完成后模型文件的最终存储目录
- **作用**: 这是您希望最终使用模型的目录
- **特点**: 
  - 可以是任意您有权限访问的目录
  - 模型文件会从cache_dir复制或符号链接到这个目录
  - 这是您实际在代码中引用的模型路径

## local_dir_use_symlinks
- **功能**: 指定在从cache_dir到local_dir的过程中是否使用符号链接
- **取值**: 
  - `True`: 创建符号链接，节省磁盘空间
  - `False`: 复制实际文件，占用更多磁盘空间但更可靠
- **适用场景**: 
  - 在Windows系统上，建议设置为False，因为符号链接可能需要特殊权限
  - 在Linux/Mac系统上，可以设置为True以节省磁盘空间

## 示例
```python
model_dir = snapshot_download(
    "ZhipuAI/chatglm3-6b",
    revision="v1.0.0",
    cache_dir="E:\github_project\models\cache",  # 临时缓存目录
    local_dir="E:\github_project\models\chatglm3-6b",  # 最终使用的模型目录
    local_dir_use_symlinks=False  # 复制实际文件而不是创建符号链接
)
```

在这个示例中：
1. ModelScope会将模型文件下载到 `E:\github_project\models\cache`
2. 然后将文件复制到 `E:\github_project\models\chatglm3-6b`
3. 最终您的代码应该引用 `E:\github_project\models\chatglm3-6b` 作为模型路径