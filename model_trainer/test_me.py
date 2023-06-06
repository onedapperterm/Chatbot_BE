from transformers import pipeline
import sys

model_checkpoint = "./LF6_Serice_Classifier"

text_classifier = pipeline("text-classification", model=model_checkpoint)

def _answer(user_input):
    result = text_classifier(user_input)
    if result[0]['label'] == 'GOODBYE':
        print(f"CLASSIFIER: The user intent class is: {result[0]['label']}" )
        print(f"CLASSIFIER: See ya ;)" )
        sys.exit(1)
    else:
        print(f"CLASSIFIER: The user intent class is: {result[0]['label']}" )


while True:
  message = input("USER: ")
  _answer(message)

