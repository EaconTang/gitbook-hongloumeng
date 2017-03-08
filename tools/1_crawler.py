#coding=utf-8
import requests
import re
import sys


reload(sys)
sys.setdefaultencoding('utf-8')

# get url list (chapters)
domain = 'http://www.sbkk8.cn'
url_index = domain + '/mingzhu/gudaicn/zhiyanzhaizhongpingshitouji'
ret = requests.get(url_index)
ret.encoding = ret.apparent_encoding
index_html = ret.text
with open('index.html', 'w') as f:
    f.write(index_html.encode('utf-8'))
print 'index.html saved...'

chapter_list = re.findall(r'<ul class="leftList">(.+?)</ul>', index_html, flags=re.S)[0]
url_list = re.findall(r'<li> <a href="(.+?)".+?</li>', chapter_list)
url_list = [domain + url for url in url_list][2:]


def sub_text(matched):
    tag = matched.group('tag')
    if tag == 'p':
        return '&nbsp;'*8
    elif tag == '/p':
        return '  \n'
    else:
        return ''

print 'start to traverse url...'
for n, url in enumerate(url_list, start=1):
    # save each html
    ret = requests.get(url)
    ret.encoding = ret.apparent_encoding
    with open('%03d.html'%(n), 'w') as f:
        print >> f, ret.text
    print '%03d.html saved...'%(n)

    with open('%03d.html'%(n)) as f:
        _text = f.read()

    # get title
    title = re.findall(r'<h1>(.+?)</h1>', _text)[0]
    ch, t1, t2 = title.split(' ')
    title = ' '.join(['【{}】'.format(ch), t1, t2])

    # get content
    _content = re.findall(r'<script src="http://www\.sbkk8\.cn/cn/b_content_float\.js" type="text/javascript"></script>(.+?)<div class="mingzhuPage">', _text, flags=re.S)[0]
    # __content =  _content.replace('<span class="xs_jj">', '').replace('</span>', '')
    __content = re.sub(r'<(?P<tag>.+?)>', sub_text, _content)
    md_text =__content.replace('[', ' ```(').replace(']', ')```')

    # write to md file
    md = """
### {}
----

{}

<br>
<hr>
<br>
    """
    with open('%03d.md'%(n), 'w') as f:
        f.write(md.strip().format(title, md_text))

    print '%03d.md saved...'%(n)