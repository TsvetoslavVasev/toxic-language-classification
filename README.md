
  # Ontology for toxic language and filters for automatic toxic language detection in bulgarian text 📝  
  ## This repository contains content that includes toxic, offensive, or otherwise inappropriate language. The materials within this repository are intended for research and educational purposes only  

  Toxic content detection in online communication remains a significant challenge, with current solutions often inadvertently blocking valuable information, including medical terms and text related to minority groups. This thesis presents a more nuanced approach to identifying toxicity in Bulgarian text while preserving access to essential information.
  
  The research explores two distinct methodologies for filtering toxic content. The first leverages a custom-built ontology that models concepts such as toxic language, medical terminology, non-toxic language, and terms related to minority communities. The second employs transfer learning techniques on a BERT-based model, trained on a specially curated and annotated corpus of Bulgarian texts.

  To train the model, an existing data corpus was expanded with web scraped content from Bulgarian online forums. The resulting dataset comprises 4,384 manually annotated sentences across four categories: toxic language, medical terminology, non-toxic language, and terms related to minority communities. The training process utilized transfer learning on a pre-trained Bulgarian BERT-based model.

  Results from the research demonstrate that the model-based filter outperforms the ontology-based approach in overall effectiveness. However, the ontological method exhibits high precision in identifying specific toxic words and phrases and offers greater flexibility in modeling various contexts.

The developed methodologies have potential applications across diverse online platforms and content moderation systems. The ontology serves as a valuable tool for media and linguistic researchers, as well as developers of filtering systems. The trained model is directly applicable in a real environment and can be seamlessly integrated as a component of toxic content detection systems.
  
  ## Get Started 🚀  
  Below are listed instruction how to setup and play around with the filters using the main.py file. 
  
  * make sure you have `git lfs`, `python` and `pip` installed
  * clone the repository
  * run `git lfs pull` from the root of the repository
  * install the requirements using `pip install -r requirements.txt`
  * run `python main.py`
  * from a browser of your choice you can acess the classification system from `localhost:5678`
