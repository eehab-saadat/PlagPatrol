# Imports
from re import split, compile, escape
from docxpy import process
from PyPDF2 import PdfReader

# File Parser (Reads File Contents To String)
def parse(filename: str):
    # Determines File Extension
    ext = filename.rsplit('.', 1)[1].lower()

    text = ""
    # DOCX
    if ext == 'docx':
        text += process(filename)
    # TXT
    elif ext == 'txt':
        with open(filename, 'r') as file:
            text += file.read()
    # PDF
    elif ext == 'pdf':
        with open(filename, 'rb') as file:
            pdf = PdfReader(file)
            for page in pdf.pages:
                text += page.extract_text()
            text = text.replace(' ', '')
    # For Invalid Ext, Even Tho Impossible
    else:
        print("Invalid File Type.")

    # Returns String With Newline, Format Specifiers Removed
    return text.replace('\n', ' ')

# Tokenizer (Tokenizes String To A List Of Phrases)
#def tokenize(text):
#    # Filters Null Strings And Strings With Word Lenghts <= 2
#    filter = lambda x : x and len(x.split(' ')) > 2
#    # Splits The String On Different Punctuation And Strips Off Leading Whitespace While Filtering
#    return [s.strip() for s in split('[,.;"-:?]', text) if filter(s.strip())]

# Tokenizer (Tokenizes String To A List Of Phrases)
#def tokenize(text: str):
    # Filters Null Strings And Strings With Word Lenghts <= 2
#    filter = lambda x : x and len(x.split(' ')) > 0
    # Splits The String On Different Punctuation And Strips Off Leading Whitespace While Filtering
#    pattern = compile(r'([,.;"-:?!])\s*')
#    phrases = pattern.split(text)
#    return [phrases[i] + phrases[i+1] for i in range(0, len(phrases)-1, 2) if filter(phrases[i] + phrases[i+1]) ]

def tokenize(text):
    delimiters = ".", ";", "\"", "-", ":", "?", "!"
    regex_pattern = '|'.join('(?<={})'.format(escape(delim)) for delim in delimiters)
    return [s.strip() for s in split(regex_pattern, text) if s.strip()]

# Test Data
#docx = tokenize(parse('Lipsum.docx'))
#txt = tokenize(parse('Lipsum.txt'))
#pdf = tokenize(parse('Lipsum.pdf'))

def filter(phrases):
    return [phrase for phrase in phrases if len(phrase.split(' ', 2)) > 2]

def get_meta(text: str):
    return (len(text.split()), len(text))

# Display
#x = "Hello this a string, an output string. Whereas, this is also another phrase! Can't believe it? Here's how to: Do not."
#x = "Hello, do you know who I am? I am Eehab, Eehab Saadat."
#print(f"Original: {x}")
#print(f"Output: {tokenize(x)}")
#getMeta = lambda x: (len(x.split()), len(x))
#w,c = getMeta(x)
#print(f"Word Count: {w} \tChar Count: {c}")
#print('\n')
#print(filter(tokenize(x)))

