import os 
import json
import re
from tqdm import tqdm

SAVE_DIR='./data/processed_wiki/'
ORIGINAL_WIKI_DATA='./data/wiki-pages'
os.makedirs(SAVE_DIR, exist_ok=True)

def process_lines(lines):
    sentences = []
    lines = lines.split('\n')
    for line in lines:
        line = line.split('\t')
        line = line[1] if len(line) > 1 else ''
        sentence = re.sub(r'[\t\n\r]', '', line)
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        sentences.append(sentence)

    return sentences


def process_wiki_file(dir_entry):
    docs = []
    with open(dir_entry.path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            if data['id'] != '':
                docs.append({
                    'id': data['id'],
                    'contents': data['text'],
                    'sentences': process_lines(data['lines'])
                })
    return docs

def save_processed_file(file_name, docs):
    with open(os.path.join(SAVE_DIR, file_name), 'w', encoding='utf-8') as file:
        for doc in docs:
            file.write(json.dumps(doc) + '\n')
    
def main():
    for entry in tqdm(os.scandir(ORIGINAL_WIKI_DATA)):
        if entry.is_file() and entry.name.endswith('jsonl'):
            docs = process_wiki_file(entry)
            save_processed_file(entry.name, docs)
    
if __name__ == '__main__':
    main()
