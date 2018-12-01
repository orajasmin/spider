# -*- coding: utf-8 -*-
# @Author: Marte
# @Date:   2018-11-26 14:32:06
# @Last Modified by:   Marte
# @Last Modified time: 2018-11-26 14:39:10
import json
import requests
import re


# 抓二进制资源
def get_resourse(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    return None


# 抓网页
def get_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


# 解析页面
def parse_one_page(html):
    # 获取电影演员表的正则表达式
    pattern = re.compile('<p class="star">(.*?)</p>',re.S)
    actor_items = re.findall(pattern, html)
    # 获取电影标题的正则表达式
    pattern = re.compile('<p class="name"><a href="/films/.*?" title="(.*?)" data-act="boarditem-click" data-val="{movieId:.*?</a></p>',re.S)
    movie_name_items = re.findall(pattern, html)
    # 获取电影排名的正则表达式
    pattern = re.compile('<i class="board-index board-index-.*?">(.*?)</i>',re.S)
    rate_items = re.findall(pattern, html)
    # 获取电影的上映时间
    pattern = re.compile('<p class="releasetime">(.*?)</p>',re.S)
    releasetime_items = re.findall(pattern, html)
    # 获取电影的评分
    pattern = re.compile('<p class="score"><i class="integer">(.*?)</i><i class="fraction">(.*?)</i></p>', re.S)
    score_items = re.findall(pattern, html)
    # 获取电影封面
    pattern = re.compile('movieId:.*?>.*?<img.*?<img.*?src="(.*?)"', re.S)
    cover_items = re.findall(pattern, html)
    result_list = []
    for i in range(len(actor_items)):
        result_dict = {}
        result_dict['actor']=actor_items[i].strip()[3:]
        result_dict['movie_name'] = movie_name_items[i].strip()
        result_dict['rate'] = rate_items[i]
        result_dict['releasetime'] = releasetime_items[i][0:15]
        result_dict['score'] = ''.join(score_items[i])
        result_dict['cover'] = cover_items[i]
        result_list.append(result_dict)
    return result_list


# 取所有页
def get_all_pages():
    result_list = []
    for i in range(10):
        page = i * 10
        url = 'http://maoyan.com/board/4?offset=' + str(page)
        html = get_page(url)
        result_list.extend(parse_one_page(html))
    print(len(result_list))
    return result_list


def write_image_files(result_list):
    for item in result_list:
        cover_url = item['cover']
        file_name = cover_url.split('/')[-1].split('@')[0]
        print(cover_url)
        content = get_resourse(cover_url)
        with open('./images/%s' % file_name, 'wb') as f:
            f.write(content)


def save_json(result_list):
    json_text = json.dumps(result_list, ensure_ascii=False)
    with open('./maoyan.json','w', encoding='utf-8') as f:
        f.write(json_text)


def main():
    # html = get_page('http://maoyan.com/board/4')
    # print(html)
    result_list = get_all_pages()
    print(result_list)
    # write_image_files(result_list)
    save_json(result_list)


if __name__ == '__main__':
    main()