#!usr/bin/env python
#encoding: utf-8

from scrapy import Selector
import urllib2
import HTMLParser
import logging
from logging import handlers
import time

LOG_FILE = "mobile_num.log"
logger = logging.getLogger()
handler = logging.FileHandler(LOG_FILE)
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)

def setLog(log_message,log_filename='log'):
    """
    for log 
    """
    logger = logging.getLogger()
    handler = logging.FileHandler(log_filename)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)
    logger.debug(log_message)
    logger.removeHandler(handler)


import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def for_ominated_data(info_list, xpath_list):
    """
    for some ominated data
    """
    if len(xpath_list) == 0:
        xpath_list.append("")
        setLog(log_message="\001".join(info_list))
    else:
        pass
    try:
        assert len(xpath_list) >= 1, 'xpath_list must be one element'
        xpath_list = [el.strip() for el in xpath_list]
        info_list.extend(xpath_list)
    except Exception, e:
        setLog(log_message="for_ominated {info}".format(info=e))
    return info_list


def crawl_mobile_info():
    """
    base_url是两个网站没有手机号的url，
    web_cla是指不同网站的标识只有两种类型 分别是：'ip138','shouji'
    """
    
    f = open("norecord_mobile_code.txt")
    for mNum in f.readlines():
        try:
            detail_list = [mNum.strip()]
            #以下是抓取shouji上的数据
            base_url_shouji = 'http://shouji.supfree.net/fish.asp?cat=%s'
            url = base_url_shouji %str(mNum).rstrip()
            xtml = urllib2.urlopen(url)
            content = xtml.read()
            content = content.decode("gb2312").encode("utf-8")
            content = bytes(content)
            sel = Selector(text=content, type='html')
            classi = sel.xpath(u"//span[text()='卡类型：']/../text()").extract()
            detail_list = for_ominated_data(detail_list, classi)
            bus = sel.xpath(u"//span[text()='运营商：']/following-sibling::a[1]/text()").extract() #运营商
            detail_list = for_ominated_data(detail_list,bus)

            #以下是从ip138上抓取
            base_url_ip138 = 'http://www.ip138.com:8080/search.asp?mobile=%s&action=mobile'
            url = base_url_ip138 %str(mNum).rstrip()
            xtml = urllib2.urlopen(url)
            content = xtml.read()
            content = content.decode("gb2312").encode("utf-8")
            content = bytes(content)
            sel = Selector(text=content, type='html')
    #            html_parse = HTMLParser.HTMLParser()
    #            clue = '卡&nbsp;类&nbsp;型'
    #            newclue = html_parse.unescape(clue)  #解析html中的空格
    #            xpath_syn = u"//td[text()='%s']/following-sibling::td[1]/text()"%newclue
    #            classi = sel.xpath(xpath_syn).extract()  #电话卡类型
    #            detail_list = for_ominated_data(detail_list,classi)
            district_code = sel.xpath(u"//td[text()='区 号']/following-sibling::td[1]/text()").extract()
            detail_list = for_ominated_data(detail_list,district_code)   #区号
            fox_code = sel.xpath(u"//td[text()='邮 编']/following-sibling::td[1]/text()").extract()
            detail_list = for_ominated_data(detail_list,fox_code)   #邮编
            local = sel.xpath(u"//td[text()='卡号归属地']/following-sibling::td[1]/text()").extract()
            html_parse = HTMLParser.HTMLParser()
            #local = html_parse.unescape(local)  #解析html中的空格
            try:
                local = local[0].strip()
                local = local.split(html_parse.unescape("&nbsp;")) #应老马要求将归属地拆开
            except Exception,e:
                setLog("归属地_errror %"%"|".join(detail_list),) 
            detail_list = for_ominated_data(detail_list, local)#卡号归属地
            in_f = open("detail_info_norecord_mobile_num.txt","a")
            in_f.write("|".join(detail_list)+"\n")
            time.sleep(1)
        except Exception,e:
            setLog("error mobile_num=%s" %mNum) 
            


crawl_mobile_info()









