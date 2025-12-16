import asyncio
import logging
from server.db.repository.knowledge_base_repository import get_kb_detail
from server.db.session import async_session_scope
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from server.db.base import AsyncSessionLocal
from server.db.models.knowledge_base_model import KnowledgeBaseModel

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_get_kb_detail_direct():
    """直接使用 async_session_scope 测试 get_kb_detail 逻辑"""
    try:
        logger.info("开始直接测试 get_kb_detail 逻辑")
        async with async_session_scope() as session:
            stmt = select(KnowledgeBaseModel).where(KnowledgeBaseModel.kb_name.ilike('private'))
            result = await session.execute(stmt)
            kb = result.scalars().first()
            logger.info(f"查询结果: {kb}")
            if kb:
                return {
                    "kb_name": kb.kb_name,
                    "kb_info": kb.kb_info,
                    "vs_type": kb.vs_type,
                    "embed_model": kb.embed_model,
                    "file_count": kb.file_count,
                    "create_time": kb.create_time,
                }
            else:
                return {}
    except Exception as e:
        logger.error(f"直接测试失败: {type(e).__name__}: {e}", exc_info=True)
        raise

async def test_get_kb_detail_function():
    """测试 get_kb_detail 函数"""
    try:
        logger.info("开始测试 get_kb_detail 函数")
        result = await get_kb_detail(kb_name='private')
        logger.info(f"函数调用结果: {result}")
        return result
    except Exception as e:
        logger.error(f"函数测试失败: {type(e).__name__}: {e}", exc_info=True)
        raise

async def test_async_session_local():
    """测试 AsyncSessionLocal 直接使用"""
    try:
        logger.info("开始测试 AsyncSessionLocal 直接使用")
        async with AsyncSessionLocal() as session:
            stmt = select(KnowledgeBaseModel).where(KnowledgeBaseModel.kb_name.ilike('private'))
            result = await session.execute(stmt)
            kb = result.scalars().first()
            logger.info(f"直接使用 AsyncSessionLocal 查询结果: {kb}")
            return kb
    except Exception as e:
        logger.error(f"AsyncSessionLocal 测试失败: {type(e).__name__}: {e}", exc_info=True)
        raise

async def main():
    logger.info("开始所有测试")
    
    logger.info("\n=== 测试1: AsyncSessionLocal 直接使用 ===")
    try:
        await test_async_session_local()
        logger.info("测试1通过")
    except Exception as e:
        logger.error("测试1失败")
    
    logger.info("\n=== 测试2: 直接使用 async_session_scope ===")
    try:
        await test_get_kb_detail_direct()
        logger.info("测试2通过")
    except Exception as e:
        logger.error("测试2失败")
    
    logger.info("\n=== 测试3: get_kb_detail 函数 ===")
    try:
        await test_get_kb_detail_function()
        logger.info("测试3通过")
    except Exception as e:
        logger.error("测试3失败")

if __name__ == "__main__":
    asyncio.run(main())