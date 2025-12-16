import asyncio
import os
import sys
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 添加项目根到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from server.knowledge_base.kb_service.faiss_kb_service import FaissKBService

async def simple_test_query():
    """简化的测试查询函数，用于定位问题"""
    try:
        logger.info("开始创建FaissKBService实例")
        faissService = FaissKBService("private")
        logger.info("FaissKBService实例创建成功")
        
        logger.info("开始搜索文档: '解释一下langchain'")
        search_ans = await faissService.search_docs(query="解释一下langchain")
        logger.info(f"搜索结果: {search_ans}")
        
        return search_ans
    except Exception as e:
        logger.error(f"测试查询失败: {type(e).__name__}: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    logger.info("启动FAISS向量数据库初始化测试")
    try:
        # 只运行简化的测试查询
        result = asyncio.run(simple_test_query())
        logger.info("测试完成，结果: %s", result)
    except Exception as e:
        logger.error(f"程序执行失败: {type(e).__name__}: {e}", exc_info=True)
        sys.exit(1)