# import argparse
from owlready2 import get_ontology
from rdflib import Graph, Namespace
import string
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='ui/templates', static_folder='ui/static')

translator = str.maketrans('', '', string.punctuation)

ontology_path = "./ontology/toxic-language-ontology-with-individuals.owl"
onto = get_ontology(ontology_path).load()

g = Graph()
g.parse(ontology_path, format="xml")
namespace = Namespace("http://www.semanticweb.org/cvasev/ontologies/2024/4/modified-toxic-ontology#")
g.bind("onto", namespace)

save_path = './saved_model_5epochs/'
model = AutoModelForSequenceClassification.from_pretrained(save_path)
tokenizer = AutoTokenizer.from_pretrained(save_path)

labels_map = {0: 'Toxic', 1: 'MedicalTerminology', 2: 'NonToxic', 3: 'MinorityGroup'}

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

def predict(sentence):
    inputs = tokenizer(sentence, return_tensors='pt', padding=True, truncation=True, max_length=512)
    inputs = {key: value.to(model.device) for key, value in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_label = torch.argmax(logits, dim=1).item()
    return labels_map[predicted_label]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    text = request.form['text']
    ontology_classification = classify_ontology(text, onto)
    model_classification = predict(text)
    
    filtered_ontology_classification = {key: value for key, value in ontology_classification.items() if value == 1}
    
    return render_template('result.html', text=text, ontology_classification=filtered_ontology_classification, model_classification=model_classification)

if __name__ == '__main__':
    app.run(port = 5678, debug=True)
