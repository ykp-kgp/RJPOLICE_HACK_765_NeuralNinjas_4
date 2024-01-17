# import json
# from sentence_transformers import SentenceTransformer, CrossEncoder, util
# import gzip
# import os
# import torch
# import pandas as pd  # Import pandas library

# if not torch.cuda.is_available():
#     print("Warning: No GPU found. Please add GPU to your notebook")

# #We use the Bi-Encoder to encode all passages, so that we can use it with semantic search
# bi_encoder = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
# bi_encoder.max_seq_length = 256     #Truncate long passages to 256 tokens
# top_k = 32                          #Number of passages we want to retrieve with the bi-encoder


# # Load the Excel file
# excel_filepath = 'updated_IPC.xlsx'
# df = pd.read_excel(excel_filepath)

# # Extract documents from a specific column in the Excel file, e.g., 'document_column'
# passages = df['Offense'].tolist()

# print("Passages:", len(passages))

# # Extract documents from a specific column in the Excel file, e.g., 'document_column'
# passages_and_ipc = [(offense, ipc) for offense, ipc in zip(df['Offense'].tolist(), df['IPC_Section'].tolist())]

# print("Passages:", len(passages_and_ipc))

# # We encode all passages into our vector space. This takes about 5 minutes (depends on your GPU speed)
# corpus_embeddings = bi_encoder.encode([passage for passage, ipc in passages_and_ipc], convert_to_tensor=True, show_progress_bar=True)


# import requests

# def search(query):
#     results = {}

#     print("\n-------------------------\n")
#     print("\nInput question:", query)

#     # Encode the query using the bi-encoder and find potentially relevant passages
#     question_embedding = bi_encoder.encode(query, convert_to_tensor=True)
#     # question_embedding = question_embedding.cuda()
#     hits = util.semantic_search(question_embedding, corpus_embeddings, top_k=top_k)
#     hits = hits[0]  # Get the hits for the first query

#     print("Top Bi-Encoder Retrieval hits")
#     hits = sorted(hits, key=lambda x: x['score'], reverse=True)

#     for hit in hits[0:10]:
#         ipc_section = passages_and_ipc[hit['corpus_id']][1]

#         if ipc_section not in results:
#             results[ipc_section] = ""

#         results[ipc_section] += passages[hit['corpus_id']].replace("\n", " ")

#     # Extract IPC information from the results
#     ipc_information = "\n".join([f"{ipc}: {text}" for ipc, text in results.items()])

#     return ipc_information

# s="Sevame Mr. Police Officer, Sir, Pulish police station dargah Ajmer, in connection with the request to Kanuni Karviya, I am requesting Lalaram Putar Ramlal 17 Jati Bhil resident Shahpura - Rupapura district Bhilwada and I was going to be a 2 -minute phone of Utaur Rahman, then Atikur Rahman Putar Athahur Rahman said to me in the talkroom, I wrote me, I refused, then he slapped me and grabbed my hair and hit the wall on the wall and abused me. Lalaram Shahpura- Rooppura District Bhilwara 8209072672 Hall in/No. 502/19 Hindu Mola Mohla Gasety Bazar Ajmer 95410505, 3/4/23 Action Police PS Dargah District Ajmer Date 04.04.2023 Time is certified that Tahiriri Hasta is certified. Written report Shri Lalaram son Shri Ram Lal caste Bhil age 17 years resident Rooppura Police Station Phoolia district Bhilwara (Raj) Hall Ataur Rahman's house 502/19 Hindi Mochi Mohalla Ghaseti Bazar Ajmer PS Dargah Ajmer, May Shri Ajizur Rahman son Mr. Ataur Rahman caste Chudghar Syed Musalman age 41 years resident M.N. 502/19 Hindu Mauchi Mauhla Ghaseti Bazaar Ajmer PS Dargah Ajmer District Ajmer was present via the police station present. On Mazid Dariyaft, the incident is from the ground floor in Ataur Rahman's house. It was read after reading. Listened to understand right. Majmoon Report 341,323,342,504,377/511 IPC, 7/8, 18 Poxo Act 2012 and Section 3 (2) (2) (2) (v) (A) SC/ST Act 1989 and filed an indictment on CCTNS portal after coming to Waku of SC/ST Act 1989. . Tafish Shri Gori Shankar was held by Deputy Superintendent of Police, Sur Dargah District Ajmer. M.N. CCTNS will be inscribed separately when received from the portal. Capital FIR was issued as per rules. A copy of FIR is free. Will be given to SR will be released separately. SD Ugma Ram Uni I/C Police Station Police Station Dargah District Ajmer"
# search(query=s)



import json
from sentence_transformers import SentenceTransformer, CrossEncoder, util
import gzip
import os
import torch
import pandas as pd  # Import pandas library

if not torch.cuda.is_available():
    print("Warning: No GPU found. Please add GPU to your notebook")

#We use the Bi-Encoder to encode all passages, so that we can use it with semantic search
bi_encoder = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
bi_encoder.max_seq_length = 256     #Truncate long passages to 256 tokens
top_k = 32                          #Number of passages we want to retrieve with the bi-encoder


# Load the Excel file
excel_filepath = 'D:/rajasApp/updated_IPC.xlsx'
df = pd.read_excel(excel_filepath)

# Extract documents from a specific column in the Excel file, e.g., 'document_column'
passages = df['Offense'].tolist()

print("Passages:", len(passages))

# Extract documents from a specific column in the Excel file, e.g., 'document_column'
passages_and_ipc = [(offense, ipc) for offense, ipc in zip(df['Offense'].tolist(), df['IPC_Section'].tolist())]

print("Passages:", len(passages_and_ipc))

# We encode all passages into our vector space. This takes about 5 minutes (depends on your GPU speed)
corpus_embeddings = bi_encoder.encode([passage for passage, ipc in passages_and_ipc], convert_to_tensor=True, show_progress_bar=True)







def search(query,k):
    results = {}

    # Encode the query using the bi-encoder and find potentially relevant passages
    question_embedding = bi_encoder.encode(query, convert_to_tensor=True)
    # question_embedding = question_embedding.cuda()
    hits = util.semantic_search(question_embedding, corpus_embeddings, top_k=top_k)
    hits = hits[0]  # Get the hits for the first query
    hits = sorted(hits, key=lambda x: x['score'], reverse=True)

    for hit in hits[0:k]:
        ipc_section = passages_and_ipc[hit['corpus_id']][1]

        if ipc_section not in results:
            results[ipc_section] = ""

        results[ipc_section] += passages[hit['corpus_id']].replace("\n", " ")

    return results




s="Sevame Mr. Police Officer, Sir, Pulish police station dargah Ajmer, in connection with the request to Kanuni Karviya, I am requesting Lalaram Putar Ramlal 17 Jati Bhil resident Shahpura - Rupapura district Bhilwada and I was going to be a 2 -minute phone of Utaur Rahman, then Atikur Rahman Putar Athahur Rahman said to me in the talkroom, I wrote me, I refused, then he slapped me and grabbed my hair and hit the wall on the wall and abused me. Lalaram Shahpura- Rooppura District Bhilwara 8209072672 Hall in/No. 502/19 Hindu Mola Mohla Gasety Bazar Ajmer 95410505, 3/4/23 Action Police PS Dargah District Ajmer Date 04.04.2023 Time is certified that Tahiriri Hasta is certified. Written report Shri Lalaram son Shri Ram Lal caste Bhil age 17 years resident Rooppura Police Station Phoolia district Bhilwara (Raj) Hall Ataur Rahman's house 502/19 Hindi Mochi Mohalla Ghaseti Bazar Ajmer PS Dargah Ajmer, May Shri Ajizur Rahman son Mr. Ataur Rahman caste Chudghar Syed Musalman age 41 years resident M.N. 502/19 Hindu Mauchi Mauhla Ghaseti Bazaar Ajmer PS Dargah Ajmer District Ajmer was present via the police station present. On Mazid Dariyaft, the incident is from the ground floor in Ataur Rahman's house. It was read after reading. Listened to understand right. Majmoon Report 341,323,342,504,377/511 IPC, 7/8, 18 Poxo Act 2012 and Section 3 (2) (2) (2) (v) (A) SC/ST Act 1989 and filed an indictment on CCTNS portal after coming to Waku of SC/ST Act 1989. . Tafish Shri Gori Shankar was held by Deputy Superintendent of Police, Sur Dargah District Ajmer. M.N. CCTNS will be inscribed separately when received from the portal. Capital FIR was issued as per rules. A copy of FIR is free. Will be given to SR will be released separately. SD Ugma Ram Uni I/C Police Station Police Station Dargah District Ajmer"

import re

def determine_crime_nature(text, context_window=5):
    crime_keywords = {
        'Suicide': ['suicide'],
        'Prostitution': ['prostitution', 'sex'],
        'Abandonment': ['abandonment'],
        'Foeticide,Infanticide': ['foeticide', 'infanticide'],
        'Kidnapping': ['kidnap', 'abduction', 'snatch', 'capture', 'seizure', 'holding hostage'],
        'Murder': ['murder', 'homicide', 'killing', 'manslaughter', 'slaying', 'assassination', 'elimination'],
        'Rape': ['rape', 'sex', 'raped', 'intercourse'],
        'Public servant': ['public servant'],
        'Property': ['property'],
        'Indecent Exposure': ['indecent exposure', 'public nudity', 'flashing', 'exhibitionism'],
        'Theft': ['theft', 'stole', 'robbery', 'burglary', 'embezzlement', 'larceny', 'shoplifting'],
        'Assault': ['assault', 'attack', 'harm', 'battery', 'assail', 'strike', 'hit', 'punch', 'beat'],
        'Fraud': ['fraud', 'scam', 'deception', 'identity theft', 'swindling', 'hoax', 'cheating', 'forgery'],
        'Vandalism': ['vandalism', 'damage', 'destruction', 'defacement', 'mischief', 'graffiti', 'sabotage'],
        'Kidnapping': ['kidnap', 'abduction', 'snatch', 'capture', 'seizure', 'holding hostage'],
        'Homicide': ['murder', 'homicide', 'killing', 'manslaughter', 'slaying', 'assassination', 'elimination'],
        'Arson': ['arson', 'fire', 'incendiarism', 'pyromania', 'burning'],
        'Bribery': ['bribery', 'corruption', 'graft', 'subornation', 'bribing'],
        'Cybercrime': ['cybercrime', 'hacking', 'phishing', 'online crime', 'cyber attack'],
        'Drug Offense': ['drug trafficking', 'possession of drugs', 'narcotics violation', 'drug trade'],
        'Sexual Assault': ['sexual assault', 'rape', 'harassment', 'sexual abuse', 'molestation'],
        'Forgery': ['forgery', 'counterfeit', 'falsification', 'fraudulent reproduction'],
        'Burglary': ['burglary', 'break-in', 'theft by entering', 'illegal entry', 'housebreaking'],
        'Car Theft': ['car theft', 'auto theft', 'vehicle theft', 'grand theft auto'],
        'Extortion': ['extortion', 'blackmail', 'coercion', 'intimidation', 'threat'],
        'Human Trafficking': ['human trafficking', 'forced labor', 'modern slavery', 'human smuggling'],
        'Trespassing': ['trespassing', 'unlawful entry', 'intrusion', 'trespass'],
        'White Collar Crime': ['embezzlement', 'insider trading', 'money laundering', 'financial crime', 'corporate fraud'],
        'Assault with a Deadly Weapon': ['assault with a deadly weapon', 'armed assault', 'deadly force', 'aggravated assault'],
        'Organized Crime': ['organized crime', 'racketeering', 'mob activity', 'criminal syndicate'],
        'Stalking': ['stalking', 'harassment', 'persistent pursuit', 'obsessive following'],
        'Public Intoxication': ['public intoxication', 'drunk and disorderly', 'intoxicated behavior', 'public drunkenness'],
        'Child Abuse': ['child abuse', 'neglect', 'child endangerment', 'child maltreatment'],
        'Environmental Crime': ['environmental crime', 'pollution', 'ecological violation', 'environmental damage'],
        'Insurance Fraud': ['insurance fraud', 'false claim', 'claim fraud', 'insurance scam'],
        'Tax Evasion': ['tax evasion', 'tax fraud', 'tax noncompliance', 'evading taxes'],
        'Domestic Violence': ['domestic violence', 'spousal abuse', 'domestic assault', 'partner violence'],
        'Robbery': ['robbery', 'holdup', 'mugging', 'heist', 'armed robbery'],
        'Shoplifting': ['shoplifting', 'retail theft', 'lifting', 'shrinkage'],
        'Property Fraud': ['property fraud', 'real estate fraud', 'land scam', 'property deception', 'real estate scheme'],
        'Insulting': ['insulting', 'verbal abuse', 'offensive language', 'name-calling', 'derogatory remarks'],
        'Harassment': ['harassment', 'intimidation', 'bullying', 'torment', 'persecution'],
        'Disorderly Conduct': ['disorderly conduct', 'disturbing the peace', 'disruptive behavior', 'public disturbance'],
        'Public Nuisance': ['public nuisance', 'disturbing public order', 'public annoyance', 'public disruption'],
        'Hate Crime': ['hate crime', 'bias-motivated crime', 'prejudice crime', 'discriminatory crime'],
        'Blackmail': ['blackmail', 'threatening', 'coercive tactics', 'extortion'],
        'Forgery': ['forgery', 'counterfeit', 'falsification', 'fraudulent reproduction'],
        'Impersonation': ['impersonation', 'identity fraud', 'posing as another', 'false identity'],
        'Racketeering': ['racketeering', 'organized crime', 'illegal enterprise', 'criminal racket'],
        'Tax Fraud': ['tax fraud', 'tax evasion', 'tax scheme', 'fraudulent taxes'],
        'Money Laundering': ['money laundering', 'financial crime', 'money cleaning', 'laundering money'],
        'Elder Abuse': ['elder abuse', 'senior exploitation', 'abuse of the elderly', 'elder mistreatment'],
        'Illegal Gambling': ['illegal gambling', 'betting', 'unlawful wagering', 'gambling violation'],
        'Conspiracy': ['conspiracy', 'criminal conspiracy', 'plotting', 'collusion'],
        'Cyber Espionage': ['cyber espionage', 'data theft', 'online spying', 'cyber infiltration'],
        'Stolen Property': ['stolen property', 'possession of stolen goods', 'receives stolen property', 'fencing'],
        'Public Corruption': ['public corruption', 'bribery in public office', 'official misconduct', 'government corruption'],
        'Terrorism': ['terrorism', 'terrorist activity', 'terror attack', 'acts of terror'],
        'Medical Fraud': ['medical fraud', 'healthcare fraud', 'medical scam', 'insurance fraud'],
        'Environmental Pollution': ['environmental pollution', 'toxic waste dumping', 'pollution violation', 'environmental contamination'],
        'Corporate Espionage': ['corporate espionage', 'industrial spying', 'business espionage', 'corporate spying'],
        'Child Exploitation': ['child exploitation', 'child pornography', 'exploitation of minors', 'child abuse imagery'],
        'Counterfeiting': ['counterfeiting', 'fake goods', 'forgery', 'imitation'],
        'Securities Fraud': ['securities fraud', 'investment fraud', 'stock fraud', 'securities scam'],
        'Breach of Privacy': ['breach of privacy', 'invasion of privacy', 'privacy violation', 'intrusion of solitude'],
        'Credit Card Fraud': ['credit card fraud', 'identity theft', 'carding', 'credit card scam'],
        'Illegal Arms Trade': ['illegal arms trade', 'weapons trafficking', 'arms smuggling', 'weapons trade'],
        'Money Counterfeiting': ['money counterfeiting', 'counterfeit currency', 'counterfeiting money', 'forged money'],
        'Public Indecency': ['public indecency', 'indecent exposure', 'obscene behavior', 'lewd acts'],
        'Intellectual Property Theft': ['intellectual property theft', 'copyright infringement', 'IP theft', 'piracy'],
        'Smuggling': ['smuggling', 'illegal transportation', 'contraband trade', 'smuggling operation'],
        'Perjury': ['perjury', 'false testimony', 'lying under oath', 'perjurious statements'],
        'Obstruction of Justice': ['obstruction of justice', 'hindering investigation', 'interference with law', 'justice obstruction'],
        'Animal Cruelty': ['animal cruelty', 'animal abuse', 'cruelty to animals', 'inhumane treatment of animals'],
        'Corporate Fraud': ['corporate fraud', 'business deception', 'fraudulent business practices', 'corporate dishonesty'],
        'Illegal Logging': ['illegal logging', 'deforestation', 'unauthorized timber cutting', 'logging violation'],
        'Money Smuggling': ['money smuggling', 'currency transportation', 'smuggling cash', 'illicit money transfer'],
        'Criminal Mischief': ['criminal mischief', 'willful property damage', 'mischief-making', 'property vandalism'],
        'Criminal Trespass': ['criminal trespass', 'unauthorized entry', 'trespassing', 'unlawful intrusion'],
        'Criminal Negligence': ['criminal negligence', 'reckless disregard for safety', 'criminal carelessness', 'negligent behavior'],
        'Institutional Corruption': ['institutional corruption', 'corrupt practices', 'institutional dishonesty', 'corruption in institutions'],
        'Criminal Harassment': ['criminal harassment', 'persistent unwanted behavior', 'harassing behavior', 'repeated harassment'],
        'Insulting': ['insulting', 'verbal abuse', 'offensive language', 'disparagement', 'slander', 'name-calling'],
        'Public Intoxication': ['public intoxication', 'drunk and disorderly', 'intoxicated behavior', 'public drunkenness'],
        'Indecent Exposure': ['indecent exposure', 'public nudity', 'flashing', 'exhibitionism'],
        'Disorderly Conduct': ['disorderly conduct', 'disturbing the peace', 'disruptive behavior', 'public disturbance'],
    }

    detected_crimes = {}

    for crime, keywords in crime_keywords.items():
        for keyword in keywords:
            pattern = rf'\b{re.escape(keyword)}\b'
            matches = re.finditer(pattern, text, re.IGNORECASE)

            for match in matches:
                start, end = match.span()
                start_context = max(0, start - context_window)
                end_context = min(len(text), end + context_window)
                context_words = text[start_context:end_context]

                if crime not in detected_crimes:
                    detected_crimes[crime] = []

                detected_crimes[crime].append({
                    'keyword': keyword,
                    'context': context_words
                })

    return detected_crimes

# result = determine_crime_nature(s)

# for crime, details in result.items():
#     print(f"{crime}")

# print(result)


def func(str):
    dct = determine_crime_nature(str)
    print(dct)
    crime_ipc_sections = {
        'Suicide': [305, 306, 309],
        'Prostitution': [373, 372],
        'Abandonment': [317],
        'Foeticide,Infanticide': [315, 316],
        'Kidnapping': [363, 364, 365, 366, 367, 368, 369, 384],
        'Murder': [302, 315],
        'Rape': [376],
        'Theft': [379],
        'Public servant': [165, 166, 167, 168, 169, 170],
        'Property': [412, 413, 414, 441],
    }

    output_ipc_sections={}

    for keyword in dct:
        # Check if the keyword is present in the crime_ipc_sections dictionary
        if keyword in crime_ipc_sections:
            ipc_sections = crime_ipc_sections[keyword]
            # Create a list of dictionaries for each IPC section
            for ipc in ipc_sections:
                dct = df[df['IPC_Section'] ==ipc]
                if dct.empty:
                    continue
                else:
                    definition = dct.iloc[0]['Offense']
                    output_ipc_sections[ipc]=definition

    # print(output_ipc_sections) #empty

    for keyword in dct:
        x=search(keyword,2)
        for ipc in x:
            if not ipc in output_ipc_sections:
                output_ipc_sections[ipc]=x[ipc]

    # print(output_ipc_sections) #2 elements

    y=search(s,10)
    for ipc in y:
        if not ipc in output_ipc_sections:
            output_ipc_sections[ipc]=y[ipc]

    # print(output_ipc_sections) # correct

    i=0
    final_output={}
    for ipc in output_ipc_sections:
        final_output[ipc]=output_ipc_sections[ipc]
        i=i+1
        if i==10:
            break

    return final_output





