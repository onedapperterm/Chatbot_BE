from transformers import pipeline

model_checkpoint = "onedapperterm/LF6_Serice_Classifier"

text_classifier = pipeline("text-classification", model=model_checkpoint)

def classify(user_input):
    model_result = text_classifier(user_input)
    result = model_result[0] #type:ignore
    return result



