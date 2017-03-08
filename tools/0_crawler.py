import requests
import re

url = 'http://www.zggdwx.com/honglou/{}.html'


def sub_text(matched):
    _c = matched.group('c')
    return _c


for i in range(1, 121):
    res = requests.get(url.format(i)).text
    with open('{}.html'.format(i), 'w') as f:
        f.write(res.encode('utf-8'))
    print '{}.html saved...'.format(i)

    print 'reading {}.html...'.format(i)
    with open('{}.html'.format(i)) as f:
        text = f.read()

    # get title
    title_start = text.index('<h1>')
    title_end = text.index('</h1>')
    title = text[title_start+4:title_end]
    # extract content
    content = re.findall(r'<div class="content">(.+?)</div>', text, flags=re.S)[0]
    # remove href
    content = re.sub(r'<a.+?href=".*?">(?P<c>.+?)</a>', sub_text, content)

    print 'writing %03d.md...'%(i)
    with open('%03d.md'%(i), 'w') as f:
        md = """
### {}
----

{}

<br>
<hr>
<br>

        """
        f.write(md.strip().format(title, content))



