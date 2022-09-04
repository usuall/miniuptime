from mini.config import get_Config
import pymysql
from loguru import logger

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
            logger.error('MYSQL Error : ' + str(code) + ' '+ msg, 1)
            
        
    return wrapper


@with_cursor
def get_url_list(c):
    c.execute("SELECT * FROM tb_url where url_fg = 1")
    return c.fetchall()

@with_cursor
def get_grp_list(c):
    c.execute("SELECT * FROM tb_group where grp_fg = 1 order by grp_title")
    return c.fetchall()

@with_cursor
def get_grp_url_list(c, keyword):
    
    sql = f"select b.* from tb_group as a right outer join tb_url as b on a.grp_no = b.grp_no"
    if(keyword.get('DISABLED') == True):
        sql += f" where 1=1"
    else:
        sql += f" where b.url_fg=1"

    if(keyword.get('GRP_LIST') != '전 체' and len(keyword.get('GRP_LIST')) > 0):
        sql += f" and a.grp_title='{keyword.get('GRP_LIST')}'"
    if(keyword.get('SITE_TITLE')):
        sql += f" and b.url_title like '%{keyword.get('SITE_TITLE')}%'"
    if(keyword.get('SITE_URL')):
        sql += f" and b.url_addr like '%{keyword.get('SITE_URL')}%'"
    if(keyword.get('URL_NO')):
        sql += f" and b.url_no = '{keyword.get('URL_NO')}'"
    
    if(keyword.get('RANDOM') == True):
        sql += f" order by rand()"
        #sql += f" order by b.url_lastest_check_dt desc"
    elif(keyword.get('OLDEST') == True):
        sql += f" order by url_lastest_check_dt limit 1"
        # 가장 체크 오래된 것 5개(반복)        
    else:    
        sql += f" order by b.url_no"
            
    
    logger.info('SQL : ' + sql )
    c.execute(sql)
    
    return c.fetchall()

@with_cursor
def add_monitoring(c, tb_monitor):
    sql_data = ("INSERT INTO tb_monitor (url_no, mon_response_time, status_code, html_file, mon_image, mon_img_match1, mon_html_match1, mon_html_diff_output, mon_html_diff_time ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s) ")
    sql_val = (tb_monitor['url_no'], tb_monitor['mon_response_time'], tb_monitor['status_code'], tb_monitor['html_file'], tb_monitor['mon_image'], tb_monitor['mon_img_match1'], tb_monitor['mon_html_match1'], tb_monitor['mon_html_diff_output'], tb_monitor['mon_html_diff_time'])
    c.execute(sql_data, sql_val)
    
@with_cursor
def update_url_monitoring(c, tb_url):
    sql_data = ("UPDATE tb_url SET url_redirected = %s, url_response_time = %s, url_status = %s, url_lastest_check_dt = now(), url_img_match1 = %s, url_html_match1 = %s, url_html_diff_output = %s  WHERE url_no = %s ")
    sql_val = (tb_url['url_redirected'], tb_url['url_response_time'], tb_url['url_status'], tb_url['url_img_match1'], tb_url['url_html_match1'], tb_url['url_html_diff_output'], tb_url['url_no'])
    c.execute(sql_data, sql_val)
    
    
        
'''
# 오류 리스트 출력
SELECT *, round(100-(mon_img_match1*100), 2) as diff_rate
FROM `tb_monitor` 
WHERE 1=1 
and mon_img_match1 >= 0.4 
order by mon_dt desc;

'''