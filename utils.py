import re

class Utils:
  """Common utilities and constants for input and output."""
  @staticmethod
  def read_lines(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
      return f.readlines()

  @staticmethod
  def capitalize_single(w):
    """Capitalizes a single word w."""
    return w[0].upper() + w[1:]

  @staticmethod
  def capitalize_apa(s, spliter=' '):
    """Capitalizes a single word w."""
    LOWER_CASES = {
        'a', 'an', 'the', 'to', 'on', 'in', 'of', 'at', 'by', 'for', 'or',
        'and', 'vs.', 'iOS'
    }

    s = s.strip(',.- ')

    # Reverses wrong order for IEEE proceedings.
    # if comma is found and last word is 'on'.
    if s.rfind(',') > 0 and s[-3:].lower() == ' on':
      p = s.rfind(',')
      s = s[p + 2:] + s[:p]

    # Split the words and capitalize with filters.
    words = s.split(spliter)
    capitalized_words = []
    start = True
    for word in words:
      if len(word) == 0:
        continue
      if not start and word.lower() in LOWER_CASES:
        capitalized_words.append(word.lower())
      else:
        capitalized_words.append(Utils.capitalize_single(word))
      start = word[-1] in '.:'

    s = spliter.join(capitalized_words)

    return s if spliter == '-' else Utils.capitalize_apa(s, '-')

  @staticmethod
  def capitalize_all(s):
    """Capitalizes a title (string)."""
    return ' '.join(list(map(Utils.capitalize_single, s.split(' '))))

  @staticmethod
  def file_nameable(s):
    """Makes a string available for file names.

    Removes all punctuations.
    Converts : to -.
    Removes UTF-8 characters such as °.
    """
    return ''.join(
        re.split(' |\.|\,|\!|\?',
                 s.replace(':', '-').replace('°', '')))
