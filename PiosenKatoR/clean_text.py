import re

def clean_html(raw):
    cleaner = re.compile('<.*?>')
    cleantext = re.sub(cleaner, '', raw)
    return cleantext

def clean_proverbs (raw):
    cleaner = re.compile('\([^)]*\)')
    cleantext = re.sub(cleaner, '',raw)
    return cleantext

def clean_indent(raw):
    cleaner = re.compile('^\s+')
    cleantext = re.sub(cleaner, '',raw)
    return cleantext

def clean_rest(text):
    cleaner = re.compile('\\r\\n\s+')
    cleantext = re.sub(cleaner, '',text)
    return cleantext

def clean_rest2(text):
    cleaner = re.compile('(\\r\\n)')
    cleantext = re.sub(cleaner, ' ',text)
    return cleantext

def clean_carriage(text):
    cleaner = re.compile('(.*)\n')
    cleantext = re.sub(cleaner, '',text)
    return cleantext

def clean_psalmus(text):
    cleaner = re.compile('Aklamacja|REFREN\:\s|Bracia\:\s')
    cleantext = re.sub(cleaner, '',text)
    return cleantext

def clean_text(raw):
    text = clean_html(raw)
    text = clean_proverbs(text)
    text = clean_indent(text)
    text = clean_rest(text)
    text = clean_rest2(text)
    text = clean_carriage(text)
    text = clean_psalmus(text)
    return text