import pyodbc

# 定义连接参数
SERVER = '沈雨博'   # 服务器名称
DATABASE = 'student_management_system'  # 数据库名称
USERNAME = 'sa'   # 用户名
PASSWORD = '030612'   # 密码

# 构建连接字符串
connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
print(connectionString)

    # 使用 connect() 方法建立连接
conn = pyodbc.connect(connectionString)

    # 创建游标
cursor = conn.cursor()

    # 关闭游标和连接
cursor.close()
conn.close()
