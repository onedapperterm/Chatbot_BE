from transformers import  AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer 
from sklearn.model_selection import train_test_split
import json
import torch

model_checkpoint = "dbmdz/bert-base-german-cased"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

with open('./dataset.json') as f:
    raw_dataset = json.load(f)

label_names = raw_dataset["scenarios"]
intents = raw_dataset["intents"]

texts = [intent["words"] for intent in intents]
labels = [intent["intent_label"] for intent in intents]

train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=.2)

print(train_texts[0])

train_encodings = tokenizer(train_texts, truncation=True, padding=True, is_split_into_words=True)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, is_split_into_words=True)

class TextDataset(torch.utils.data.Dataset): #type:ignore
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = TextDataset(train_encodings, train_labels)
val_dataset = TextDataset(val_encodings, val_labels)


model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint, num_labels=8)

args = TrainingArguments(
    "LF6_Serice_Classifier",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    num_train_epochs=3,
    weight_decay=0.01,
    push_to_hub=True,
)


print(train_dataset[0])

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
)

trainer.train()
trainer.push_to_hub(commit_message="Training complete")

