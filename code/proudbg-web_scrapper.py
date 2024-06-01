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
    for sentence in sentences:
        filtered.append(sentence)
    return filtered

def simple_sentence_splitter(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [sentence.strip() for sentence in sentences if sentence]

def fetch_article_sentences(url, max_sentences=1000):
    sentences = []
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}, stopping...")
        return sentences

    tree = html.fromstring(response.content)
    post_bodies = tree.xpath('//div[contains(@class, "entry-content")]/p')

    for post in post_bodies:
        text = post.text_content().strip()
        text = clean_text(text)
        post_sentences = simple_sentence_splitter(text)
        post_sentences = filter_sentences(post_sentences)
        sentences.extend(post_sentences)
        if len(sentences) >= max_sentences:
            break
    return sentences[:max_sentences]

urls = [
    'https://proud.bg/kak-da-pravim-seks-s-trans-partnyori-saveti-ot-trans-momiche/',
    'https://proud.bg/translation-yanuarsko-razstrelvane-na-biologichnia-pol/',
    'https://proud.bg/doklad-trima-ot-chetirima-sa-bili-tormozeni-v-uchilishte-zaradi-polova-identichnost/',
    'https://proud.bg/sofia-prayd-otbelyaza-mezhdunarodnia-den-sreshtu-homofobiata-bifobiata-i-transfobiata/',
    'https://proud.bg/evropa-ne-e-podgotvena-sreshtu-atakite-na-kraynata-desnitsa/',
    'https://proud.bg/my-voice-my-choice-initsiativa-za-pravoto-na-bezopasen-i-dostapen-abort/',
    'https://proud.bg/baydan-finalizira-mashtabni-promeni-v-zakona-za-zashtita-ot-diskriminatsia/',
    'https://proud.bg/konkurs-za-poezia-v-rusia-vavede-zabrana-za-uchastie-na-trans-hora/',
    'https://proud.bg/irak-otlaga-glasuvaneto-na-zakonoproekt-predvizhdasht-smartno-nakazanie-za-ednopolovi-otnoshenia/',
    'https://proud.bg/tayland-se-doblizhava-do-legaliziraneto-na-ednopolovite-sayuzi/',
    'https://proud.bg/gana-e-blizo-do-priemaneto-na-strog-anti-lgbti-zakon/',
    'https://proud.bg/gartsia-legalizira-ednopolovite-brakove/',
    'https://proud.bg/kak-da-badesh-po-dobar-pasiven-v-legloto/',
    'https://proud.bg/seks-saveti-za-neopitnite-gey-mazhe/',
    'https://proud.bg/zhenite-koito-pravyat-seks-s-zheni-svarshv/',
    'https://proud.bg/dopitvane-razkri-che-chetvart-ot-porno-d/',
    'https://proud.bg/kolko-riskov-e-oralniat-seks/',
    'https://proud.bg/kak-da-badesh-po-dobar-aktiven-v-legloto/',
    'https://proud.bg/nasheto-semeystvo-se-radva-na-prava-koito-ne-bihme-imali-v-balgaria/',
    'https://proud.bg/izraelski-lekari-i-zdravni-rabotnitsi-se-protivopostavyat-na-anti-lgbti-prizivite-na-pravitelstvoto/'

]

all_sentences = []

for url in urls:
    collected_sentences = fetch_article_sentences(url)
    all_sentences.extend(collected_sentences)
    print(f"Total sentences collected from {url}: {len(collected_sentences)}")

print(f"Total sentences collected from all URLs: {len(all_sentences)}")
print(all_sentences)

df = pd.DataFrame({
    'text': all_sentences,
    'Toxic': 0,
    'MedicalTerminology': 0,
    'NonToxic': 0,
    'MinorityGroup': 0,
    'sentence_length': [len(sentence) for sentence in all_sentences]
})

df.to_csv('../data/proud_bg_sentences.csv', index=False)
print("CSV file has been created with the collected sentences.")