import re
from lxml import html
import requests
import pandas as pd

def clean_text(text):
    text = re.sub(r'\n+|\t+', ' ', text)
    text = re.sub(r'Share on Facebook', '', text)
    text = text.strip()
    return text

def filter_sentences(sentences):
    filtered = []
    date_pattern = re.compile(r'\d{1,2} [А-Яа-я]{3} \d{4}, \d{2}:\d{2}')  # Pattern to match dates like '16 Яну 2019, 18:48'
    intro_phrase = "В тази тема на здравния форум може да откриете мнения и зададете вашите въпроси, свързани с"

    for sentence in sentences:
        if (sentence.startswith('Re:') or 
            'Специалистите на www.framar.bg предоставят консултация' in sentence or
            date_pattern.search(sentence) or 
            intro_phrase in sentence):
            continue
        filtered.append(sentence)
    return filtered

def simple_sentence_splitter(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [sentence.strip() for sentence in sentences if sentence]

def fetch_sentences(forum_tuples, start_page=0, step=10, max_sentences=1000):
    sentences = []

    for base_url, max_pages in forum_tuples:
        current_page = start_page

        while len(sentences) < max_sentences and current_page <= max_pages * step:
            if current_page == 0:
                url = f"{base_url}.html"
            else:
                url = f"{base_url}-{current_page}.html"

            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to retrieve data from {url}, stopping...")
                break

            tree = html.fromstring(response.content)
            post_bodies = tree.xpath('//div[contains(@class, "postbody")]')

            for post in post_bodies:
                text = post.text_content().strip()
                text = clean_text(text)
                post_sentences = simple_sentence_splitter(text)
                post_sentences = filter_sentences(post_sentences)
                sentences.extend(post_sentences)
                if len(sentences) >= max_sentences:
                    break
            print(f"Scraped page {current_page} of {base_url}... Total sentences collected: {len(sentences)}")
            current_page += step

        if len(sentences) >= max_sentences:
            break

    return sentences[:max_sentences]

forums = [
    ('https://forum.framar.bg/cervicit-vazpalenie-shiikata-matkata-mnenia-vaprosi-t17363', 4),
    ('https://forum.framar.bg/vaginalni-infekcii-karvene-mnenia-vaprosi-t17361', 3),
    ('https://forum.framar.bg/vazpalenie-penisa-testisite-mnenia-vaprosi-t17502', 0),
    ('https://forum.framar.bg/problemi-polovi-jlezi-menstruatsia-onlajn-konsultacia-endokrinolog-t10035', 2),
    ('https://forum.framar.bg/polovo-predavani-bolesti-onlain-konsultacia-venerolog-t9819', 4)
]

collected_sentences = fetch_sentences(forums)
print(f"Total sentences collected: {len(collected_sentences)}")
print(collected_sentences)


df = pd.DataFrame({
    'text': collected_sentences,
    'Toxic': 0,
    'MedicalTerminology': 0,
    'NonToxic': 0,
    'MinorityGroup': 0,
    'sentence_length': [len(sentence) for sentence in collected_sentences]
})

df.to_csv('../data/scraped_datasets/framar_forum_sentences.csv', index=False)
print("CSV file has been created with the collected sentences.")