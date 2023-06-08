from .default_answers import get_pattern
from pipelines import text_classifier, token_classifier
from scenario_handler.handler import get_answer

def process_input(text, state, threshold=.7):
    intent = text_classifier.classify(text)
    if intent.get('score') < threshold:  #type:ignore
        return {"answer": get_pattern('UNKNOWN'), "state": "transfer_to_human"}
    else:
        label = intent.get('label')  #type:ignore
        answer = _process_intent(label, text, threshold)
        return answer

def _process_intent(label, input, threshold):
    if label in ('GREETING', 'APRECIATION', 'GOODBYE'):
        return { "answer": get_pattern(label), "label": label}
    else:
        classification = token_classifier.classify(input) 
        print(classification)
        entities = _get_entities(classification, threshold)
        print(entities)
        answer = get_answer(label, entities)
        return answer

def _get_entities(classification, threshold):
    entities =[ entity for entity in classification ] #type:ignore 
    processed_entities = {}

    for entity in entities:
        if entity['score'] > threshold:
            group = entity['entity_group']
            if group not in processed_entities: 
                processed_entities[group] = []
            processed_entities[group].append(entity['word'])
        else: 
            pass
    return processed_entities


