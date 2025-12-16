# 使用基础镜像（可尝试国内镜像加速，如阿里云的nvidia镜像）
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04
# 备选国内镜像（若官方镜像拉取慢可替换）：
# FROM registry.cn-hangzhou.aliyuncs.com/nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# 设定维护者标签
LABEL maintainer=MuyuChery

# 设置工作目录和环境变量
ENV HOME=/fufan-chat-api \
    PATH=/opt/conda/bin:$PATH

# 设置工作目录
WORKDIR /fufan-chat-api

# 替换Ubuntu apt源为阿里云镜像（加速系统依赖安装）
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends curl libgl1 libglib2.0-0 jq && \
    # 使用清华镜像源下载Miniconda（替代官方源）
    curl -sLo /miniconda.sh https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash /miniconda.sh -b -p /opt/conda && \
    rm /miniconda.sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 配置时区
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

# 配置Conda国内镜像源（清华）加速环境创建
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/ && \
    conda config --set show_channel_urls yes && \
    # 接受Anaconda服务条款
    conda tos accept

# 使用conda创建虚拟环境
RUN conda create -n fufan_chat_api python=3.10 --yes --override-channels \
    -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main \
    -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free \
    -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge \
    -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch && \
    echo "source activate fufan_chat_api" > ~/.bashrc

# 复制并安装Python依赖（利用Docker缓存，仅当requirements.txt变化时重新安装）
COPY requirements.txt .
RUN /opt/conda/envs/fufan_chat_api/bin/pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制其他所有文件（最后复制，避免代码变化导致依赖重新安装）
COPY . .

# 暴露端口
EXPOSE 8000

# 容器启动时执行的命令
ENTRYPOINT ["/opt/conda/envs/fufan_chat_api/bin/python", "startup.py"]