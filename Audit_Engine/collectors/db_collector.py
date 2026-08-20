class DBCollector:
    def __init__(self, config):
        self.config = config

    def collect(self, db_type, host, user, password, dbname):
        result = {"tables": [], "users": [], "error": None}
        try:
            if db_type == "postgres":
                import psycopg2
                conn = psycopg2.connect(host=host, user=user, password=password, dbname=dbname)
                cur = conn.cursor()
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
                result["tables"] = [row[0] for row in cur.fetchall()]
                cur.execute("SELECT usename FROM pg_user")
                result["users"] = [row[0] for row in cur.fetchall()]
                conn.close()
            elif db_type == "mysql":
                import pymysql
                conn = pymysql.connect(host=host, user=user, password=password, database=dbname)
                cur = conn.cursor()
                cur.execute("SHOW TABLES")
                result["tables"] = [row[0] for row in cur.fetchall()]
                cur.execute("SELECT user FROM mysql.user")
                result["users"] = [row[0] for row in cur.fetchall()]
                conn.close()
        except Exception as e:
            result["error"] = str(e)
        return result