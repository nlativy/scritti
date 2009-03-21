from htmlentitydefs import name2codepoint
from HTMLParser import HTMLParser
from markdown import markdown
from BeautifulSoup import BeautifulSoup
from pygments.lexers import LEXERS, get_lexer_by_name
from pygments import highlight
from pygments.formatters import HtmlFormatter

# code from http://barryp.org/blog/entries/markdown-and-pygments/

# a tuple of known lexer names
_lexer_names = reduce(lambda a,b: a + b[2], LEXERS.itervalues(), ())

# default formatter
_formatter = HtmlFormatter(cssclass='source')    

class _MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []
    def handle_data(self, data):
        self.text.append(data)
    def handle_entityref(self, name):
        self.text.append(unichr(name2codepoint[name]))

def _replace_html_entities(s):
    """
    Replace HTML entities in a string
    with their unicode equivalents.  For
    example, '&amp;' is replaced with just '&'

    """
    mp = _MyParser()
    mp.feed(s)
    mp.close()
    return u''.join(mp.text)  

def markdown_pygment(txt):
    """
    Convert Markdown text to Pygmentized HTML

    """
    html = markdown(txt)
    soup = BeautifulSoup(html)
    dirty = False
    for tag in soup.findAll('pre'):
        if tag.code:
            txt = tag.code.renderContents()
            if txt.startswith('pygments:'):
                lexer_name, txt = txt.split('\n', 1)
                lexer_name = lexer_name.split(':')[1]
                txt = _replace_html_entities(txt)
                if lexer_name in _lexer_names:
                    lexer = get_lexer_by_name(lexer_name, stripnl=True, encoding='UTF-8')
                    tag.replaceWith(highlight(txt, lexer, _formatter))
                    dirty = True
    if dirty:
        html = unicode(soup)

    return html
