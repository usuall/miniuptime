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
            conn = pymysql.connect(host=host, port=int(port), user=username, password=password, db=database, use_unicode=True, charset='utf8')
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
def get_url_list_cnt(c):
    c.execute("SELECT count(*) as cnt FROM tb_url where url_fg = 1")
    
    # print(c.fetchone())
    
    return c.fetchone()
    
    # cnt값 반환
    # return number_of_rows

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
    # elif(keyword.get('OLDEST') == True):
    #     sql += f" order by url_lastest_check_dt limit 1"
    #     가장 체크 오래된 것 5개(반복)
    else:    
        sql += f" order by b.url_no"
    
    ##############################################################
    # ERROR 상태의 URL만 점검시 
    if(keyword.get('ERROR_URL') == True):
        sql = 'SELECT /* ERROR 상태의 URL만 점검시 */ b.* from tb_group as a right outer join tb_url as b on a.grp_no = b.grp_no '
        sql += ' WHERE url_fg = 1 and url_lastest_check_dt <= DATE_ADD(NOW(), INTERVAL -1 MINUTE) /* 체크한지 1분 이상된것만 다시 점검 */ '
        sql += f" and ( (b.url_status <> 200 or b.url_status is NULL) /* 상태코드 200 아닌것 */ OR "
        sql += f" (b.url_img_match1 <= 50 or b.url_html_match1 <= 50) /* 이미지, html 유사도 낮은 경우(50%) */ OR "
        sql += f" (b.url_img_match1 = -1 or b.url_html_match1 = -1) /* 원본이미지 또는 원본소스가 없는 경우 */ OR "
        sql += f" (b.url_response_time >= 12) /* 응답시간이 12초 이상 소요된 것 */ "
        sql += f" ) ORDER BY url_lastest_check_dt "
    
    ##############################################################
    # URL 범위 검색시
    if(keyword.get('URL_LIST').strip() == '----'):
        logger.info('URL 범위지정 하지 않음')
    else:
        logger.info('URL 범위지정')
        ranges = keyword.get('URL_LIST').strip().split(' ~ ')
        # print (ranges[0], 'TEST' , ranges[1])
        
        sql = f"select b.* from tb_group as a right outer join tb_url as b on a.grp_no = b.grp_no"
        if(keyword.get('DISABLED') == True):
            sql += f" where 1=1"
        else:
            sql += f" where b.url_fg=1"
            
        sql += f" and url_no between {ranges[0]} and {ranges[1]}"        


    ##############################################################
    # 최종 실행 SQL        
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
    
    
@with_cursor
def get_ssl_url_list(c):
    c.execute("SELECT * FROM tb_url where 1=1 /* and url_fg = 1 */ order by url_no")
    # c.execute("SELECT * FROM tb_url where url_no = 293 and url_fg = 1 order by url_no")
    return c.fetchall()



# 도메인 SSL 인증서 만료일 체크
@with_cursor
def insert_ssl_info(c, tb_domain):
    sql_data = ("INSERT INTO tb_domain SET url_no = %s /* primary/unique key */ , check_date = %s, host= %s, issued_to= %s, issued_o= %s, issuer_c= %s, issuer_o= %s, issuer_ou= %s, issuer_cn= %s, cert_sn= %s, cert_sha1= %s, cert_alg= %s, cert_ver= %s, cert_sans= %s, cert_exp= %s, cert_valid= %s, valid_from= %s, valid_till= %s, validity_days= %s, days_left= %s, valid_days_to_expire= %s, tcp_port= %s ON DUPLICATE KEY UPDATE check_date = %s, host= %s, issued_to= %s, issued_o= %s, issuer_c= %s, issuer_o= %s, issuer_ou= %s, issuer_cn= %s, cert_sn= %s, cert_sha1= %s, cert_alg= %s, cert_ver= %s, cert_sans= %s, cert_exp= %s, cert_valid= %s, valid_from= %s, valid_till= %s, validity_days= %s, days_left= %s, valid_days_to_expire= %s, tcp_port= %s ")
    sql_val = (tb_domain['url_no'], tb_domain['check_date'], tb_domain['host'], tb_domain['issued_to'], tb_domain['issued_o'], tb_domain['issuer_c'], tb_domain['issuer_o'], tb_domain['issuer_ou'], tb_domain['issuer_cn'], tb_domain['cert_sn'], tb_domain['cert_sha1'], tb_domain['cert_alg'], tb_domain['cert_ver'], tb_domain['cert_sans'], tb_domain['cert_exp'], tb_domain['cert_valid'], tb_domain['valid_from'], tb_domain['valid_till'], tb_domain['validity_days'], tb_domain['days_left'], tb_domain['valid_days_to_expire'], tb_domain['tcp_port'], tb_domain['check_date'], tb_domain['host'], tb_domain['issued_to'], tb_domain['issued_o'], tb_domain['issuer_c'], tb_domain['issuer_o'], tb_domain['issuer_ou'], tb_domain['issuer_cn'], tb_domain['cert_sn'], tb_domain['cert_sha1'], tb_domain['cert_alg'], tb_domain['cert_ver'], tb_domain['cert_sans'], tb_domain['cert_exp'], tb_domain['cert_valid'], tb_domain['valid_from'], tb_domain['valid_till'], tb_domain['validity_days'], tb_domain['days_left'], tb_domain['valid_days_to_expire'], tb_domain['tcp_port'])
    c.execute(sql_data, sql_val)
    
# 도메인 만료일 체크
@with_cursor
def insert_domain_info(c, tb_domain):
    
    # print (tb_domain['domain_name'],)
    
    sql_data = ("INSERT INTO tb_domain SET url_no = %s /* primary/unique key */ , host = %s, domain_name = %s, creation_date = %s, updated_date = %s, expiration_date = %s ON DUPLICATE KEY UPDATE host = %s, domain_name = %s, creation_date = %s, updated_date = %s, expiration_date = %s")
    sql_val = (tb_domain['url_no'], tb_domain['host'], tb_domain['domain_name'], tb_domain['creation_date'], tb_domain['updated_date'], tb_domain['expiration_date'], tb_domain['host'], tb_domain['domain_name'], tb_domain['creation_date'], tb_domain['updated_date'], tb_domain['expiration_date'])
    
    c.execute(sql_data, sql_val)
    
'''
# 오류 리스트 출력
SELECT *, round(100-(mon_img_match1*100), 2) as diff_rate
FROM `tb_monitor` 
WHERE 1=1 
and mon_img_match1 >= 0.4 
order by mon_dt desc;

'''

@with_cursor
def get_ssl_url_list_all(c):
    c.execute("SELECT * FROM tb_domain_list where 1=1 order by url_no")
    # c.execute("SELECT * FROM tb_url where url_no = 293 and url_fg = 1 order by url_no")
    return c.fetchall()

@with_cursor
def insert_ssl_info_all(c, tb_domain):
    sql_data = ("INSERT INTO tb_domain_list SET url_no = %s /* primary/unique key */ , check_date = %s, host= %s, issued_to= %s, issued_o= %s, issuer_c= %s, issuer_o= %s, issuer_ou= %s, issuer_cn= %s, cert_sn= %s, cert_sha1= %s, cert_alg= %s, cert_ver= %s, cert_sans= %s, cert_exp= %s, cert_valid= %s, valid_from= %s, valid_till= %s, validity_days= %s, days_left= %s, valid_days_to_expire= %s, tcp_port= %s ON DUPLICATE KEY UPDATE check_date = %s, host= %s, issued_to= %s, issued_o= %s, issuer_c= %s, issuer_o= %s, issuer_ou= %s, issuer_cn= %s, cert_sn= %s, cert_sha1= %s, cert_alg= %s, cert_ver= %s, cert_sans= %s, cert_exp= %s, cert_valid= %s, valid_from= %s, valid_till= %s, validity_days= %s, days_left= %s, valid_days_to_expire= %s, tcp_port= %s ")
    sql_val = (tb_domain['url_no'], tb_domain['check_date'], tb_domain['host'], tb_domain['issued_to'], tb_domain['issued_o'], tb_domain['issuer_c'], tb_domain['issuer_o'], tb_domain['issuer_ou'], tb_domain['issuer_cn'], tb_domain['cert_sn'], tb_domain['cert_sha1'], tb_domain['cert_alg'], tb_domain['cert_ver'], tb_domain['cert_sans'], tb_domain['cert_exp'], tb_domain['cert_valid'], tb_domain['valid_from'], tb_domain['valid_till'], tb_domain['validity_days'], tb_domain['days_left'], tb_domain['valid_days_to_expire'], tb_domain['tcp_port'], tb_domain['check_date'], tb_domain['host'], tb_domain['issued_to'], tb_domain['issued_o'], tb_domain['issuer_c'], tb_domain['issuer_o'], tb_domain['issuer_ou'], tb_domain['issuer_cn'], tb_domain['cert_sn'], tb_domain['cert_sha1'], tb_domain['cert_alg'], tb_domain['cert_ver'], tb_domain['cert_sans'], tb_domain['cert_exp'], tb_domain['cert_valid'], tb_domain['valid_from'], tb_domain['valid_till'], tb_domain['validity_days'], tb_domain['days_left'], tb_domain['valid_days_to_expire'], tb_domain['tcp_port'])
    c.execute(sql_data, sql_val)

# 도메인 만료일 체크
@with_cursor
def insert_domain_info_all(c, tb_domain):
    sql_data = ("INSERT INTO tb_domain_list SET url_no = %s /* primary/unique key */ , host = %s, domain_name = %s, creation_date = %s, updated_date = %s, expiration_date = %s ON DUPLICATE KEY UPDATE host = %s, domain_name = %s, creation_date = %s, updated_date = %s, expiration_date = %s")
    sql_val = (tb_domain['url_no'], tb_domain['host'], tb_domain['domain_name'], tb_domain['creation_date'], tb_domain['updated_date'], tb_domain['expiration_date'], tb_domain['host'], tb_domain['domain_name'], tb_domain['creation_date'], tb_domain['updated_date'], tb_domain['expiration_date'])
    c.execute(sql_data, sql_val)
    