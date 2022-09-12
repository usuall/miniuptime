from mini.ssl_checker import SSLChecker
import mini.library as mini
import mini.model as model
from loguru import logger
from datetime import datetime
from urllib.parse import urlparse
import json
import whois



SSLChecker = SSLChecker()

def main():
    
    result = model.get_ssl_url_list()
    # print('resutl ',type(result), len(result))
    total_cnt = len(result) # 조회 건수
    now_dt = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    for row in result:
        

        url_addr = get_url(row['url_addr'])

        # ssl 인증서 정보 취득
        ssl_info = get_SSL_info(url_addr)
        #print(ssl_info)
        #print (type(ssl_info))   # str
        
        # str -> dict 형식으로 변경
        ssl_info = json.loads(ssl_info)
        #print (type(ssl_info))
        
        print ('===================')
        print (row['url_no'], url_addr)
        
        # print(ssl_info.get(url_addr))
        # break
        
        # SSL 조회 안될경우 
        if(ssl_info.get(url_addr) != None):
            
            tb_domain = {}
            tb_domain['check_date'] = now_dt
            tb_domain['url_no'] = row['url_no']
            
            for key, value in ssl_info[url_addr].items():
                # print(key, value)
                tb_domain[key] = value
                
            # print(tb_domain)
            
            # SSL 인증서 정보 갱신
            model.insert_ssl_info(tb_domain)
            
        
        # 도메인 정보 취득
        get_whois(url_addr, row['url_no'])
            

def get_whois(url_addr, url_no):
    # print ('whois')
    domain = whois.whois(url_addr)
    
    # print (domain.creation_date, domain.updated_date, domain.expiration_date )
    
    tb_domain = {}
    tb_domain['url_no'] = url_no

    # 값이 2개 이상인 경우(list로 리턴)
    if (type(domain.domain_name) is list):
        domain.domain_name = domain.domain_name[0]
        
    # 값이 2개 이상인 경우(list로 리턴)
    if (type(domain.updated_date) is list):
        domain.updated_date = domain.updated_date[0]
        
    # print (domain.domain_name)                   
    tb_domain['host'] = url_addr
    tb_domain['domain_name'] = domain.domain_name    
    tb_domain['creation_date'] = domain.creation_date
    tb_domain['updated_date'] = domain.updated_date
    tb_domain['expiration_date'] = domain.expiration_date
    tb_domain['name_servers'] = domain.name_servers
    
    model.insert_domain_info(tb_domain)
    
def get_url(url_addr):
    
    # url_addr = url_addr.replace('http://', '')
    # url_addr = url_addr.replace('https://', '')
    # url_addr = url_addr.split('/')
    # url_addr = url_addr[2]
    
    

    # netloc : url 부분만 취득
    url_addr = urlparse(url_addr).hostname
    
    return url_addr    
    

def get_SSL_info(url_addr):
    # global SSLChecker
    # SSLChecker = SSLChecker()

    args = {
        'hosts': [url_addr],
    }


    try:
        ssl_info = SSLChecker.show_result(SSLChecker.get_args(json_args=args))
        ssl_info
        
    except Exception as error:
        
        print ('----- exception --------')
        pass
    
    return ssl_info
    
    
    


if __name__ == '__main__':
    
    main()
    
    # url_str = "http://www.163.com:8080/mail/index.htm"
    # url = urlparse(url_str)
    # print ('protocol:',url.scheme)
    # print ('hostname:',url.hostname)
    # print ('port:',url.port)
    # print ('path:',url.path)
    # print ('query:', url.query) #    ，  a=1
    # i = len(url.path) - 1
    # while i > 0:
    # if url.path[i] == '/':
    #     break
    # i = i - 1
    # print 'filename:',url.path[i+1:len(url.path)]