import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

def count_tokens(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    tokens = word_tokenize(text)
    num_tokens = len(tokens)
    
    return num_tokens

file_path = 'transcript.txt'
num_tokens = count_tokens(file_path)
print(f'The number of tokens in the file is: {num_tokens}')