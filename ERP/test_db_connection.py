import psycopg2
from psycopg2 import OperationalError

def test_db_connection():
    try:
        # 尝试连接数据库
        conn = psycopg2.connect(
            dbname='erp_db',
            user='postgres',
            password='666666',
            host='localhost'
        )
        print("数据库连接成功")
        conn.close()
        return True
    except OperationalError as e:
        print(f"数据库连接失败: {e}")
        return False

if __name__ == '__main__':
    test_db_connection()