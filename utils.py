from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

from BeautifulSoup import BeautifulStoneSoup, SoupStrainer

from markdown import markdown

def markdown_with_pygments(content, safe=False, linenos="table"):
    """Render this content for display."""
    # Code based on http://www.djangosnippets.org/snippets/119

    # First, pull out all the <code></code> blocks, to keep them away
    # from Markdown (and preserve whitespace).
    LINES_STRAINER = SoupStrainer("code")
    soup = BeautifulStoneSoup(str(content), convertEntities=BeautifulStoneSoup.HTML_ENTITIES, parseOnlyThese=LINES_STRAINER)
    code_blocks = soup.findAll('code')
    for block in code_blocks:
        block.replaceWith('<code class="removed"></code>')

    # Run the post through markdown.
    markeddown = markdown(str(soup), safe_mode=safe)

    LINES_STRAINER = SoupStrainer("code")

    # Replace the pulled code blocks with syntax-highlighted versions.
    soup = BeautifulStoneSoup(markeddown, convertEntities=BeautifulStoneSoup.HTML_ENTITIES, parseOnlyThese=LINES_STRAINER)
    empty_code_blocks, index = soup.findAll('code', 'removed'), 0
    formatter = HtmlFormatter(cssclass='source', linenos=linenos)
    for block in code_blocks:
        if block.has_key('class'):
            # <code class='python'>python code</code>
            language = block['class']
        else:
            # <code>plain text, whitespace-preserved</code>
            language = 'text'
        try:
            lexer = get_lexer_by_name(language, stripnl=True, encoding='UTF-8')
        except ValueError, e:
            try:
                # Guess a lexer by the contents of the block.
                lexer = guess_lexer(block.renderContents())
            except ValueError, e:
                # Just make it plain text.
                lexer = get_lexer_by_name('text', stripnl=True, encoding='UTF-8')
        empty_code_blocks[index].replaceWith(
                highlight(block.renderContents(), lexer, formatter))
        index = index + 1

    return str(soup)
