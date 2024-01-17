import ast

# Your model_result string
model_result_str = '''The correct IPC sections are '{
    304: 'Culpable homicide not amounting to murder, If act by which the death is caused is done with intention of causing death, etc.Dowry death,Causing death by rash or negligent act', 
    420: 'Cheating and there by dishonestly inducing delivery of property, or the making, alteration or destruction of a valuable security', 
    406: 'Criminal breach of trust', 
    427: 'Mischief, and thereby causing damage to the'}'
    '''

# Extract the dictionary part from the string
dictionary_part = model_result_str.split("'")[1]

# Safely evaluate the string as a dictionary
result_dict = ast.literal_eval(dictionary_part)

# Now result_dict contains the dictionary
print(result_dict)
