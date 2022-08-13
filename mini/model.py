from mini.config import get_Config
import pymysql
import logging

# DB 환경에 맞게 입력할것

properties = get_Config()
config_db = properties['DATABASE']

host = config_db['HOST']
port = config_db['PORT']
database = config_db['DATABASE']
username = config_db['USERNAME']
password = config_db['PASSWORD']
charset = config_db['CHARSET']

def with_cursor(original_func):
    def wrapper(*args, **kwargs):
        # conn = sqlite3.connect('blog.db')
        # conn.row_factory = sqlite3.Row
        # c = conn.cursor()
        try:
            conn = pymysql.connect(host=host, user=username, password=password, db=database, use_unicode=True, charset='utf8')
            c = conn.cursor(pymysql.cursors.DictCursor)
            rv = original_func(c, *args, **kwargs)
            conn.commit()
            conn.close()
            return rv
        except Exception as e:
            code, msg = e.args
            logging.error('MYSQL Error : ' + str(code) + ' '+ msg, 1)
        
    return wrapper


@with_cursor
def get_url_list(c):
    c.execute("SELECT * FROM tb_url where url_fg = 1")
    return c.fetchall()

@with_cursor
def get_org_list(c):
    c.execute("SELECT * FROM tb_org order by org_title")
    return c.fetchall()

@with_cursor
def get_org_url_list(c, keyword):
    
    sql = f"select b.* from tb_org as a right outer join tb_url as b on a.org_no = b.org_no"
    if(keyword.get('DISABLED') == True):
        sql += f" where 1=1"
    else:
        sql += f" where b.url_fg=1"

    if(keyword.get('ORG_LIST') != '전 체' and len(keyword.get('ORG_LIST')) > 0):
        sql += f" and a.org_title='{keyword.get('ORG_LIST')}'"
    if(keyword.get('SITE_TITLE')):
        sql += f" and b.url_title like '%{keyword.get('SITE_TITLE')}%'"
    if(keyword.get('SITE_URL')):
        sql += f" and b.url_addr like '%{keyword.get('SITE_URL')}%'"
    
    print('- SQL : ' + sql )
    c.execute(sql)
    
    return c.fetchall()

@with_cursor
def add_monitoring(c, url_no, status_code, file_name):
    sql_data = ("INSERT INTO tb_monitor (url_no, status_code, file_name ) VALUES ( %s, %s, %s)")
    sql_val = (url_no, status_code, file_name)
    c.execute(sql_data, sql_val)