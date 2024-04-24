from .db import Database

class AllDAO:
    def __init__(self):
        self.db = Database()
    def getAllTables(self):
        cur = self.db.conexion.cursor()
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name != 'pg_stat_statements_info'
        AND table_name != 'pg_stat_statements';
        """
        cur.execute(query=query)
        tables = cur.fetchall()
        self.db.close()
        cur.close()

        return tables
    def getColumnNames(self, table):
        cur = self.db.conexion.cursor()
        query="""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'  -- replace with your schema, often 'public'
        AND table_name   = %s;  -- replace with your table name
        """
        cur.execute(query=query,vars=(table,))
        columns = cur.fetchall()
        self.db.close()
        cur.close()

        return columns
    def getPrimaryKey(self, table):
        cur = self.db.conexion.cursor()
        query="""
        SELECT a.attname
        FROM pg_index i
        JOIN pg_attribute a ON a.attrelid = i.indrelid
                            AND a.attnum = ANY(i.indkey)
        WHERE i.indrelid = %s ::regclass
        AND i.indisprimary;

        """
        cur.execute(query=query,vars=(table,))
        key = cur.fetchall()
        self.db.close()
        cur.close()
        return key


        