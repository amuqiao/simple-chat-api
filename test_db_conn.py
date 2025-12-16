import asyncmy
import asyncio

async def test_connection():
    try:
        conn = await asyncmy.connect(
            host='localhost',
            user='root',
            password='snowball950123',
            db='fufanapi'
        )
        print('数据库连接成功！')
        await conn.close()
    except Exception as e:
        print(f'数据库连接失败: {e}')

if __name__ == '__main__':
    asyncio.run(test_connection())