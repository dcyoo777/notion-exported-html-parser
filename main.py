from bs4 import BeautifulSoup
import os

SKIP_HTML_TAGS = ['html', 'body', 'span']
DELETE_HTML_TAGS = ['head', 'svg']

def skipTags(html):
  if html.name == '[document]':
    return ''.join([skipTags(content) for content in html.contents])
  if html.name == None:
    return html.strip()
  if html.name in DELETE_HTML_TAGS:
    return ''
  if html.name in SKIP_HTML_TAGS:
    return ''.join([skipTags(content) for content in html.contents])
  result = ['<' + html.name + '>']
  for content in html.contents:
    result.append(skipTags(content))
  result.append('</' + html.name + '>')
  return ''.join(result)



for fileName in os.listdir('input'):
  if fileName[-5:] == '.html':
    f = open("input/" + fileName, 'r')
    inputFile = ''.join(f.readlines())
    f.close()

    soup = BeautifulSoup(inputFile, 'html.parser')
    for tag in soup.recursiveChildGenerator():
      try:
        tag.attrs = {}
      except AttributeError:
        pass

    fixSoup = BeautifulSoup(skipTags(soup), 'html.parser')

    html = fixSoup.prettify()
    print(html)
    lines = [line.strip() for line in html.split('\n')]

    wf = open("output/" + fileName[:-5] + "_output.html", 'w')
    for line in lines:
      wf.write(line + '\n')
    wf.close()