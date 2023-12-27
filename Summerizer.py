import csv
from transformers import T5Tokenizer, TFT5ForConditionalGeneration
from summarizer import Summarizer

def summarize_text(input_text, model_name='bert-base-uncased'):
    summarizer = Summarizer(model_name)
    summary = summarizer(input_text)
    return summary

# Load CSV data
csv_file_path = r'D:\RJPOLICE_HACK_765_NeuralNinjas_4\Dataset\TranslateData.csv'
output_file_path = r'D:\RJPOLICE_HACK_765_NeuralNinjas_4\Dataset\newData.csv'

with open(csv_file_path, 'r', encoding='utf-8', errors='ignore') as csv_file:
    reader = csv.DictReader(csv_file)
    rows = list(reader)

# Summarize each text and add a new 'Summary' column
for row in rows:
    text = row['Content']  # Replace 'Content' with the actual column name in your CSV file
    summary = summarize_text(text)
    row['Summary'] = summary

# Write the summarized data back to a new CSV file
header = reader.fieldnames + ['Summary']
with open(output_file_path, 'w', encoding='utf-8', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)

print(f"Summaries have been written to {output_file_path}")
