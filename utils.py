from htmlentitydefs import name2codepoint
from HTMLParser import HTMLParser
from markdown import markdown
from BeautifulSoup import BeautifulSoup, Tag
from pygments.lexers import LEXERS, get_lexer_by_name
from pygments import highlight
from pygments.formatters import HtmlFormatter

# code from http://barryp.org/blog/entries/markdown-and-pygments/

# a tuple of known lexer names
_lexer_names = reduce(lambda a,b: a + b[2], LEXERS.itervalues(), ())

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

def markdown_pygment(txt, linenos="table", stripimg=False):
    """
    Convert Markdown text to Pygmentized HTML

    """
    html = markdown(txt, safe_mode='replace')
    soup = BeautifulSoup(html)
    formatter = HtmlFormatter(cssclass='source', linenos=linenos)
    dirty = False

    for img in soup.findAll('img'):
        dirty = True
        if stripimg:
            img.replaceWith("[IMAGES NOT ALLOWED IN COMMENTS]")
        else:
            # learn BeautifulSoup and clean this up
            img['class'] = 'postimg'
            toWrap = img
            p = img.parent
            if p.name == 'a':
                # This is a link, wrap the div around the parent of the link
                toWrap = p
                p = p.parent

            imgDiv = Tag(soup, "div", [("class", "image-wrapper")])
            imgDiv.insert(0, toWrap)
            p.insert(0, imgDiv)

            # Remove surrounding <p></p> to make HTML valid
            # This is all rather horrible but works with my blog
            # posts - need to fix so that the code is correct in all cases
            # easiest way may be to modify markdown itself
            para = imgDiv.parent
            if para.name == 'p':
                para.replaceWith(imgDiv)

    for tag in soup.findAll('pre'):
        if tag.code:
            txt = tag.code.renderContents()
            if txt.startswith('pygments:'):
                lexer_name, txt = txt.split('\n', 1)
                lexer_name = lexer_name.split(':')[1]
                txt = _replace_html_entities(txt)
                if lexer_name in _lexer_names:
                    lexer = get_lexer_by_name(lexer_name, stripnl=True, encoding='UTF-8')
                    tag.replaceWith(highlight(txt, lexer, formatter))
                    dirty = True
    if dirty:
        html = unicode(soup)

    return html
