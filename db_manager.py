import mysql.connector
from mysql.connector import Error
import logging

class DatabaseManager:
    def __init__(self, host="localhost", database="quant_trade_db", user="root", password=""):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                charset="utf8mb4"
            )
            if self.conn.is_connected():
                self.cursor = self.conn.cursor(dictionary=True)
                logging.info("MySQL 数据库连接成功")
                self.init_tables()
                return True
        except Error as e:
            logging.error(f"MySQL 连接失败: {e}")
            return False

    def init_tables(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS stock_pool (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    code VARCHAR(10) NOT NULL,
                    name VARCHAR(50) NOT NULL,
                    price DECIMAL(10,2),
                    change_pct VARCHAR(20),
                    score DECIMAL(5,2),
                    signal VARCHAR(20),
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS positions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    code VARCHAR(10) NOT NULL,
                    name VARCHAR(50) NOT NULL,
                    volume INT NOT NULL,
                    cost_price DECIMAL(10,2),
                    current_price DECIMAL(10,2),
                    pnl DECIMAL(12,2),
                    pnl_pct VARCHAR(20),
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS trade_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    log_time VARCHAR(50),
                    content TEXT,
                    level VARCHAR(20)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            self.conn.commit()
            logging.info("MySQL 数据库表结构初始化成功")
        except Error as e:
            logging.error(f"初始化数据库表失败: {e}")

    def save_stock_pool(self, stocks):
        if not self.conn or not self.conn.is_connected():
            return
        try:
            self.cursor.execute("TRUNCATE TABLE stock_pool;")
            for s in stocks:
                self.cursor.execute(
                    "INSERT INTO stock_pool (code, name, price, change_pct, score, signal) VALUES (%s, %s, %s, %s, %s, %s)",
                    (s[0], s[1], float(s[2]), s[3], float(s[4]), s[5])
                )
            self.conn.commit()
        except Error as e:
            logging.error(f"保存选股池异常: {e}")

    def log_trade(self, content, level="INFO"):
        if not self.conn or not self.conn.is_connected():
            return
        try:
            import datetime
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(
                "INSERT INTO trade_logs (log_time, content, level) VALUES (%s, %s, %s)",
                (t, content, level)
            )
            self.conn.commit()
        except Error as e:
            logging.error(f"记录交易日志异常: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
            logging.info("MySQL 数据库连接已关闭")

