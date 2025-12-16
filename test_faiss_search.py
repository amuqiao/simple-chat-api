import asyncio
import logging
from server.knowledge_base.kb_service.faiss_kb_service import FaissKBService

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_simple_search():
    """简化的测试，直接创建 FaissKBService 实例并调用 search_docs"""
    try:
        logger.info("开始测试 FaissKBService.search_docs")
        
        # 创建 FaissKBService 实例
        faiss_service = FaissKBService("private")
        logger.info("FaissKBService 实例创建成功")
        
        # 测试 search_docs 方法
        search_ans = await faiss_service.search_docs(query="解释一下langchain")
        logger.info(f"搜索结果: {search_ans}")
        return search_ans
    except Exception as e:
        logger.error(f"测试失败: {type(e).__name__}: {e}", exc_info=True)
        raise

async def main():
    logger.info("开始所有测试")
    
    logger.info("\n=== 测试: FaissKBService.search_docs ===")
    try:
        await test_simple_search()
        logger.info("测试通过")
    except Exception as e:
        logger.error("测试失败")

if __name__ == "__main__":
    asyncio.run(main())