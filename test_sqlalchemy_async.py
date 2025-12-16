from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, select
from configs import SQLALCHEMY_DATABASE_URI
import asyncio

async def test_sqlalchemy_async():
    try:
        print(f"使用连接字符串: {SQLALCHEMY_DATABASE_URI}")
        
        # 创建异步引擎
        async_engine = create_async_engine(
            SQLALCHEMY_DATABASE_URI,
            echo=True,  # 启用SQL查询日志
        )
        
        # 创建异步会话
        AsyncSessionLocal = sessionmaker(
            async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # 测试1: 使用text()函数执行简单查询
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1 as test"))
            print(f"简单查询结果: {result.scalar()}")
            print("测试1通过: SQLAlchemy异步连接基本功能正常")
        
        # 测试2: 尝试执行应用中失败的查询
        async with AsyncSessionLocal() as session:
            # 模拟应用中的查询: SELECT * FROM knowledge_base WHERE lower(kb_name) LIKE lower(%s)
            kb_name = "private"
            query = text("SELECT id, kb_name, kb_info, vs_type, embed_model, file_count, create_time, user_id FROM knowledge_base WHERE lower(kb_name) LIKE lower(:kb_name)")
            result = await session.execute(query, {"kb_name": kb_name})
            rows = result.fetchall()
            print(f"知识库查询结果: {rows}")
            print("测试2通过: 应用查询执行正常")
            
    except Exception as e:
        print(f"测试失败: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭引擎
        if 'async_engine' in locals():
            await async_engine.dispose()
            print("引擎已关闭")

if __name__ == '__main__':
    asyncio.run(test_sqlalchemy_async())