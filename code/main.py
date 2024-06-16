import argparse
from owlready2 import get_ontology
from rdflib import Graph, Namespace
import string
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

translator = str.maketrans('', '', string.punctuation)

ontology_path = "../ontology/toxic-language-ontology-with-individuals.owl"
onto = get_ontology(ontology_path).load()

g = Graph()
g.parse(ontology_path, format="xml")
namespace = Namespace("http://www.semanticweb.org/cvasev/ontologies/2024/4/modified-toxic-ontology#")
g.bind("onto", namespace)

def classify_ontology(text, ontology):
    words = text.split()
    classifications = {'Toxic': 0, 'MedicalTerminology': 0, 'NonToxic': 0, 'MinorityGroup': 0}

    matched = False
    for word in words:
        for individual in ontology.Content.instances():
            cleaned_word = word.translate(translator).lower()
            if cleaned_word == individual.name.lower():
                matched = True
                for content_class in individual.is_a:
                    if content_class.name == 'ToxicLanguage' and classifications['Toxic'] == 0:
                        classifications['Toxic'] = 1
                    if content_class.name == 'MedicalTerminology' and classifications['MedicalTerminology'] == 0:
                        classifications['MedicalTerminology'] = 1
                    if content_class.name == 'MinorityGroup' and classifications['MinorityGroup'] == 0:
                        classifications['MinorityGroup'] = 1
                    if content_class.name == 'NonToxicLanguage' and classifications['NonToxic'] == 0:
                        classifications['NonToxic'] = 1
    if not matched:
        classifications['NonToxic'] = 1
    return classifications

save_path = '../saved_model_5epochs/'
model = AutoModelForSequenceClassification.from_pretrained(save_path)
tokenizer = AutoTokenizer.from_pretrained(save_path)

label_map = {0: 'Toxic', 1: 'MedicalTerminology', 2: 'NonToxic', 3: 'MinorityGroup'}

def predict(sentence):
    inputs = tokenizer(sentence, return_tensors='pt', padding=True, truncation=True, max_length=512)
    inputs = {key: val.to(model.device) for key, val in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_label = torch.argmax(logits, dim=1).item()
    return label_map[predicted_label]


def main():
    parser = argparse.ArgumentParser(description="Classify sentences using ontology and ML model.")
    parser.add_argument("sentence", type=str, help="Sentence to classify")
    args = parser.parse_args()

    sentence = args.sentence
    ontology_classification = classify_ontology(sentence, onto)
    model_classification = predict(sentence)
    
    print(f"Sentence: \"{sentence}\"")
    print(f"Ontology Classification: {ontology_classification}")
    print(f"Model Classification: {model_classification}")

if __name__ == "__main__":
    main()