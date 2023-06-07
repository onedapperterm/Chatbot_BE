from transformers import pipeline

model_checkpoint = "onedapperterm/LF6_Token_Classifier"

token_classifier = pipeline("token-classification", model=model_checkpoint, aggregation_strategy="simple")


def classify(user_input):
    result = token_classifier(user_input)
    return result


