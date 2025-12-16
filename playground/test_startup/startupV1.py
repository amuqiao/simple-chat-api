import sys
import uuid
import os
import threading

# 导入项目配置
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from configs.model_config import MODEL_PATH

# 启动FastChat的Controller
from fastchat.serve.controller import app as controller_app, Controller
import uvicorn
"""
代码启动FastChat controller , ModelWorker和openai_api_server三个服务
测试本地开源大模型使用借助FastChat 托管 提供 OpenAI API 服务
"""


def start_controller():
    """启动Controller服务"""
    controller = Controller(dispatch_method="shortest_queue")
    sys.modules["fastchat.serve.controller"].controller = controller
    controller_app.title = "FastChat Controller"
    controller_app._controller = controller
    uvicorn.run(controller_app, host="0.0.0.0", port=20001)


def start_model_worker():
    """启动ModelWorker服务"""
    worker_id = str(uuid.uuid4())[:8]
    # 启动本地模型
    from fastchat.serve.model_worker import app as model_worker_app, ModelWorker
    
    # 添加调试信息
    model_path = MODEL_PATH["local_model"]["chatglm3-6b"]
    print(f"DEBUG: 模型路径为: {model_path}")
    print(f"DEBUG: 模型路径是否存在: {os.path.exists(model_path)}")
    if os.path.exists(model_path):
        files = os.listdir(model_path)
        print(f"DEBUG: 模型路径内容: {files}")
        # 检查是否有tokenizer.model文件
        tokenizer_model_path = os.path.join(model_path, "tokenizer.model")
        print(f"DEBUG: tokenizer.model路径: {tokenizer_model_path}")
        print(f"DEBUG: tokenizer.model是否存在: {os.path.exists(tokenizer_model_path)}")
        # 检查是否有其他tokenizer相关文件
        tokenizer_files = [f for f in files if "tokenizer" in f.lower()]
        print(f"DEBUG: 分词器相关文件: {tokenizer_files}")
    
    # 手动设置tokenizer.model路径
    from transformers import AutoTokenizer
    import sys
    
    # 添加调试信息
    print(f"DEBUG: 正在尝试加载分词器...")
    print(f"DEBUG: 模型路径: {model_path}")
    
    # 尝试手动加载分词器
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        print(f"DEBUG: 分词器加载成功!")
        
        # 检查tokenizer的vocab_file属性
        if hasattr(tokenizer, 'vocab_file'):
            print(f"DEBUG: 分词器的vocab_file: {tokenizer.vocab_file}")
        else:
            print(f"DEBUG: 分词器没有vocab_file属性")
            
            # 手动设置vocab_file路径
            tokenizer_path = os.path.join(model_path, "tokenizer.model")
            print(f"DEBUG: 手动设置的vocab_file路径: {tokenizer_path}")
            print(f"DEBUG: 手动设置的vocab_file是否存在: {os.path.exists(tokenizer_path)}")
    except Exception as e:
        print(f"DEBUG: 加载分词器时发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    # 继续创建ModelWorker
    worker = ModelWorker(
        controller_addr="http://127.0.0.1:20001",
        worker_addr="http://0.0.0.0:20002",
        worker_id=worker_id,
        limit_worker_concurrency=5,
        no_register=False,
        model_path=model_path,
        num_gpus=0,
        model_names="chatglm3-6b",
        device="cpu",
        max_gpu_memory=None,
    )

    model_worker_app.title = f"FastChat LLM Server ChaGLM3-6b"
    model_worker_app._worker = worker

    uvicorn.run(model_worker_app, host="0.0.0.0", port=20002)


def start_openai_api_server():
    """启动OpenAI API Server服务"""
    from fastchat.serve.openai_api_server import app as openai_api_app, app_settings, CORSMiddleware
    openai_api_app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app_settings.controller_address = "http://127.0.0.1:20001"
    app_settings.api_keys = []

    openai_api_app.title = "FastChat OpeanAI API Server"

    uvicorn.run(openai_api_app, host="0.0.0.0", port=8000)


def start_main_server():
    """启动所有服务"""
    # 创建并启动各个服务的线程
    controller_thread = threading.Thread(target=start_controller, daemon=True)
    model_worker_thread = threading.Thread(target=start_model_worker, daemon=True)
    openai_api_thread = threading.Thread(target=start_openai_api_server, daemon=True)

    # 启动线程
    controller_thread.start()
    print("Controller服务已启动")
    
    # 等待Controller服务启动完成
    import time
    time.sleep(2)
    
    model_worker_thread.start()
    print("ModelWorker服务已启动")
    
    time.sleep(2)
    
    openai_api_thread.start()
    print("OpenAI API Server服务已启动")

    # 主线程保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("服务已停止")


if __name__ == '__main__':
    start_main_server()