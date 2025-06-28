try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    print("Warning: PyMySQL not found. Please install it with: pip install pymysql")