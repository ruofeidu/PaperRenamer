"""Renames the filenames of PDFs automatically by their author, title, and published conference."""
# Reference: https://blog.pythonlibrary.org/2018/06/07/an-intro-to-pypdf2
from PyPDF2 import PdfFileReader
import os
import re
from utils import Utils

CONFERENCES = ['CHI', 'UIST', 'SIGGRAPH', 'ECCV', 'CVPR', 'ICCV', 'I3D', 'Web3D', 'ISMAR', 'VR', 'WWW']

CONF_MATCH = re.compile(
    '(CHI|UIST|SIGGRAPH|ECCV|CVPR|ICCV|I3D|Web3D|ISMAR|VR|WWW)(19|20)\d{2}')
YEAR_MATCH = re.compile('(19|20)\d{2}')

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))
    # ...
    return value

def get_info_and_rename(path, original_name):
  """
  Gets info from a PDF and rename the file following:
  https://duruofei.com/papers/Du_Geollery-AMixedRealitySocialMediaPlatform_CHI2019.pdf
  """
  original_file_path = os.path.join(path, original_name)
  with open(original_file_path, 'rb') as f:
    pdf = PdfFileReader(f)
    info = pdf.getDocumentInfo()
    number_of_pages = pdf.getNumPages()
    # Gets the first page.
    page = pdf.getPage(1)
    text = page.extractText()

  # Gets meta data.
  author = info.author
  creator = info.creator
  producer = info.producer
  subject = info.subject
  title = info.title

  if author:
    comma_pos = author.find(',')
    if comma_pos > 0:
      author = author[:comma_pos]
    last_space = author.rfind(' ')
    if last_space < 0:
      last_space = -1
    last_name = author[last_space+1:]
  file_title = Utils.file_nameable(title)

  conf_year = ''
  ans = CONF_MATCH.search(text)
  if ans:
    conf_year = ans.group()
  else:
    ans = YEAR_MATCH.search(text)
    if ans:
      conf_year = ans.group()
  new_name = '%s_%s_%s.pdf' % (last_name, file_title, conf_year)
  print('%s: %s => %s' % (path, original_name, new_name))
  new_file_path = os.path.join(path, new_name)
  os.rename(original_file_path, new_file_path)

if __name__ == '__main__':
  cwd = os.getcwd()
  all_paths = os.walk(cwd)

  for path, dir_list, file_list in all_paths:
    for file_name in file_list:
      if file_name[-3:].lower() == "pdf":
        get_info_and_rename(path, file_name)
