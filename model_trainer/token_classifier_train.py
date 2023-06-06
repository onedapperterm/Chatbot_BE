from transformers import AutoTokenizer, DataCollatorForTokenClassification, AutoModelForTokenClassification, TrainingArguments, Trainer
from datasets.arrow_dataset import Dataset
import json
import evaluate
import numpy as np

model_checkpoint = "dbmdz/bert-base-german-cased"

tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

with open('./dataset.json') as f:
    raw_dataset = json.load(f)

label_names = raw_dataset["labels"]

def align_labels_with_tokens(labels, word_ids):
    new_labels = []
    current_word = None
    for word_id in word_ids:
        if word_id != current_word:
            # Start of a new word!
            current_word = word_id
            label = -100 if word_id is None else labels[word_id]
            new_labels.append(label)
        elif word_id is None:
            # Special token
            new_labels.append(-100)
        else:
            # Same word as previous token
            label = labels[word_id]
            # If the label is B-XXX we change it to I-XXX
            if label % 2 == 1:
                label += 1
            new_labels.append(label)

    return new_labels

def tokenize_and_align_labels(sentence):
    tokenized_inputs = tokenizer(
        sentence["words"], truncation=True, is_split_into_words=True
    )
    labels = align_labels_with_tokens(sentence["ner_tags"], tokenized_inputs.word_ids())
    
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

tokenized_datasets = { "train": [], "validation": [], "test": [] }

raw_dataset_size = raw_dataset["size"]
data_splitted_limits = [ int(raw_dataset_size * 0.8), int(raw_dataset_size * 0.2) ]

for i, sentence in enumerate(raw_dataset['intents']):
    if i <= data_splitted_limits[0]:
        tokenized_datasets["train"].append(tokenize_and_align_labels(sentence))
    else:
        tokenized_datasets["validation"].append(tokenize_and_align_labels(sentence))


data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

# batch = data_collator([tokenized_datasets["test"][i] for i in range(10)])
# print(batch["labels"])


metric = evaluate.load("seqeval")

def compute_metrics(eval_preds):
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)

    # Remove ignored index (special tokens) and convert to labels
    true_labels = [[label_names[l] for l in label if l != -100] for label in labels]
    true_predictions = [
        [label_names[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    all_metrics = metric.compute(predictions=true_predictions, references=true_labels)
    
    return {
        "precision": all_metrics["overall_precision"], #type: ignore
        "recall": all_metrics["overall_recall"], #type: ignore
        "f1": all_metrics["overall_f1"], #type: ignore
        "accuracy": all_metrics["overall_accuracy"], #type: ignore
    }

id2label = {i: label for i, label in enumerate(label_names)}
label2id = {v: k for k, v in id2label.items()}

model = AutoModelForTokenClassification.from_pretrained(
        model_checkpoint,
        id2label=id2label,
        label2id=label2id
        )

args = TrainingArguments(
    "LF6_Token_Classifier",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    num_train_epochs=3,
    weight_decay=0.01,
    push_to_hub=True,
)

data_train = Dataset.from_list(tokenized_datasets["train"])
data_val = Dataset.from_list(tokenized_datasets["validation"])


print(data_train[0])
print(id2label)
print(label2id)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=data_train, #type:ignore
    eval_dataset=data_val, #type:ignore
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    tokenizer=tokenizer,
)
trainer.train()
trainer.push_to_hub(commit_message="Training complete")

