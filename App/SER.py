import json
from sentence_transformers import SentenceTransformer, CrossEncoder, util
import gzip
import os
import torch
import pandas as pd  # Import pandas library
import random

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
        'Suicide': ['suicide', 'commit suicide', 'suicidal', 'suiciding', 'took own life', 'end one\'s life'],
        'Prostitution': ['prostitution', 'engage in sex work', 'sex worker', 'prostitute', 'selling sex', 'sex trade','sex'],
        'Abandonment': ['abandonment', 'abandon', 'abandoned', 'abandoning', 'desertion'],
        'Foeticide': ['foeticide', 'infanticide', 'foetus', 'womb', 'kill unborn', 'killing fetus', 'terminate pregnancy', 'abortion'],
        'Kidnapping': ['kidnap', 'abduction', 'snatch', 'capture', 'seizure', 'hostage', 'missing', 'kidnapped', 'captured','capture','abducted', 'kidnapping victim', 'held hostage','abduct'],
        'Murder': ['murder', 'murdered', 'homicide', 'killing', 'manslaughter', 'slaying', 'assassination', 'elimination', 'commit murder', 'killed', 'kill', 'killer', 'killing spree'],
        'Rape': ['rape', 'sex', 'raped', 'intercourse', 'sexual assault', 'rapist', 'raping', 'sexual violation', 'forcible sex'],
        'Public servant': ['public servant', 'government official', 'public employee', 'civil servant', 'government worker'],
        'voilence':['voilence'],
        'Property': ['property', 'asset', 'capital', 'holdings', 'belongings', 'possessions', 'estate', 'valuables'],
        'Indecent Exposure': ['indecent exposure', 'public nudity', 'flashing', 'exhibitionism', 'expose genitals', 'indecent act','stolen'],
        'Theft': ['theft', 'stole', 'robbery', 'burglary', 'embezzlement', 'larceny', 'shoplifting', 'steal', 'thief', 'robbed', 'stealing', 'theft incident'],
        'Assault': ['assault', 'attack', 'harm', 'battery', 'assail', 'strike', 'hit', 'punch', 'beat', 'assaulted', 'assaulter', 'physical assault', 'violent attack'],
        'Fraud': ['fraud', 'scam', 'deception', 'identity theft', 'swindling', 'hoax', 'cheating', 'forgery', 'defraud', 'fraudulent activity', 'fraudulent scheme'],
        'Vandalism': ['vandalism', 'damage','damaged','destruction','destruct','destructed','defacement', 'mischief', 'graffiti', 'sabotage', 'vandalize', 'damaging property'],
        'Homicide': ['murder', 'homicide', 'killing', 'manslaughter', 'slaying', 'assassination', 'elimination', 'suicide', 'self-harm', 'homicidal', 'deadly act', 'fatal incident', 'life-taking'],
        'Arson': ['arson', 'fire', 'incendiarism', 'pyromania', 'burning', 'arsonist', 'set fire', 'commit arson', 'fire-setting'],
        'Bribery': ['bribery', 'corruption', 'graft', 'subornation', 'bribing', 'bribe', 'corrupt', 'offer bribes', 'accept bribes', 'bribery case'],
        'Cybercrime': ['cybercrime', 'hacking', 'phishing', 'online crime', 'cyber attack', 'spam', 'cybercriminal', 'hack', 'cyber intrusion', 'digital crime', 'cyber fraud'],
        'Drug Offense': ['drug', 'possession of drugs', 'narcotics violation', 'drug trade', 'cocaine', 'weed', 'drug possession', 'illegal drugs', 'drug smuggling'],
        'Sexual Assault': ['sexual assault', 'rape', 'harassment', 'sexual abuse', 'molestation', 'sexual violence', 'assaulted sexually', 'perpetrator of sexual assault', 'sexual harassment'],
        'Forgery': ['forgery', 'counterfeit', 'falsification', 'fraudulent reproduction', 'forge', 'forged document', 'forging signatures', 'counterfeit money', 'forged credentials'],
        'Burglary': ['burglary', 'break-in', 'theft by entering', 'illegal entry', 'housebreaking', 'burglarize', 'breaking and entering', 'committed burglary', 'burglar', 'burglary attempt'],
        'Car Theft': ['car theft', 'auto theft', 'vehicle theft', 'steal car', 'stolen vehicle', 'auto theft incident', 'vehicle stolen'],
        'Extortion': ['extortion', 'blackmail', 'coercion', 'intimidation', 'threat', 'extort', 'blackmailer', 'extortion case', 'extorted money'],
        'Human Trafficking': ['human trafficking', 'forced labor', 'modern slavery', 'human smuggling', 'trafficker', 'human trafficker', 'trafficking victim', 'forced labor exploitation','trafficking'],
        'Trespassing': ['trespassing', 'unlawful entry', 'intrusion', 'trespass', 'trespasser', 'entered without permission', 'illegally on premises'],
        'White Collar Crime': ['embezzlement', 'insider trading', 'money laundering', 'financial crime', 'corporate fraud', 'white collar criminal', 'white collar offense', 'business deception'],
        'Assault with a Deadly Weapon': ['assault with a deadly weapon', 'armed assault', 'deadly force', 'aggravated assault', 'shot', 'assault with weapon', 'violent weapon attack'],
        'Organized Crime': ['organized crime', 'racketeering', 'mob activity', 'criminal syndicate', 'organized criminal', 'mobster', 'criminal organization', 'illegal enterprise'],
        'Stalking': ['stalking', 'harassment', 'persistent pursuit', 'obsessive following', 'stalker', 'stalk', 'repeated harassment', 'stalking victim'],
        'Public Intoxication': ['public intoxication', 'drunk and disorderly', 'intoxicated behavior', 'public drunkenness', 'alcohol intoxication', 'substance abuse', 'intoxicated', 'drunk in public', 'public inebriation'],
        'Child Abuse': ['child abuse', 'neglect', 'child endangerment', 'child maltreatment', 'abuse of child', 'child neglect', 'child exploitation', 'mistreatment of minors'],
        'Environmental Crime': ['environmental crime', 'pollution', 'ecological violation', 'environmental damage', 'environmental violation', 'illegal dumping', 'pollution offense', 'environmental degradation'],
        'Insurance Fraud': ['insurance fraud', 'false claim', 'claim fraud', 'insurance scam', 'fraudulent insurance', 'insurance scheme', 'deceptive claim', 'fraudulent coverage'],
        'Tax Evasion': ['tax evasion', 'tax fraud', 'tax noncompliance', 'evading taxes', 'tax cheat', 'tax evader', 'tax fraud scheme', 'illegally avoiding taxes'],
        'Domestic Violence': ['domestic violence', 'spousal abuse', 'domestic assault', 'partner violence', 'abuse in relationships', 'domestic abuser', 'violent relationship', 'domestic abuse case'],
        'Robbery': ['robbery', 'holdup', 'mugging', 'heist', 'armed robbery', 'robber', 'robbed', 'commit robbery', 'robbery incident', 'holdup'],
        'Shoplifting': ['shoplifting', 'retail theft', 'lifting', 'shrinkage', 'shoplifter', 'steal from store', 'shoplifting incident', 'caught shoplifting'],
        'Property Fraud': ['property fraud', 'real estate fraud', 'land scam', 'property deception', 'real estate scheme', 'fraudulent property deal', 'deceptive real estate', 'property fraud case'],
        'Insulting': ['insulting', 'verbal abuse', 'offensive language', 'name-calling', 'derogatory remarks', 'insult', 'offend', 'insulted', 'offensive comment', 'name-caller'],
        'Harassment': ['harassment', 'intimidation', 'bullying', 'torment', 'persecution', 'harass', 'harasser', 'persistent harassment', 'harassment victim'],
        'Disorderly Conduct': ['disorderly conduct', 'disturbing the peace', 'disruptive behavior', 'public disturbance', 'disorderly', 'disturb public peace', 'public disruption', 'disruptive activity'],
        'Public Nuisance': ['public nuisance', 'disturbing public order', 'public annoyance', 'public disruption', 'public disturbance', 'public problem', 'nuisance behavior'],
        'Hate Crime': ['hate crime', 'bias-motivated crime', 'prejudice crime', 'discriminatory crime', 'hate-motivated offense', 'bias crime', 'discrimination crime'],
        'Blackmail': ['blackmail', 'threatening', 'coercive tactics', 'extortion', 'blackmailing', 'threats for money', 'coercion tactics', 'extortion attempt'],
        'Forgery': ['forgery', 'counterfeit', 'falsification', 'fraudulent reproduction', 'forge', 'forged document', 'counterfeit scheme', 'fraudulent copy'],
        'Impersonation': ['impersonation', 'identity fraud', 'posing as another', 'false identity', 'imposter', 'identity theft', 'fraudulent impersonation', 'impersonator'],
        'Racketeering': ['racketeering', 'organized crime', 'illegal enterprise', 'criminal racket', 'racketeer', 'organized criminal activity', 'racketeering scheme'],
        'Tax Fraud': ['tax fraud', 'tax evasion', 'tax scheme', 'fraudulent taxes', 'tax deception', 'illegal tax activity', 'tax fraud case'],
        'Money Laundering': ['money laundering', 'financial crime', 'money cleaning', 'laundering money', 'money launderer', 'money laundering scheme', 'illegal money transfer'],
        'Elder Abuse': ['elder abuse', 'senior exploitation', 'abuse of the elderly', 'elder mistreatment', 'exploitation of seniors', 'elder abuse case', 'mistreatment of elderly'],
        'Illegal Gambling': ['illegal gambling', 'betting', 'unlawful wagering', 'gambling violation', 'gambling crime', 'illegal betting', 'betting offense'],
        'Conspiracy': ['conspiracy', 'criminal conspiracy', 'plotting', 'collusion', 'conspire', 'plot', 'conspirator'],
        'Cyber Espionage': ['cyber espionage', 'data theft', 'online spying', 'cyber infiltration', 'cyber attack', 'hacking', 'phishing', 'online crime', 'stocking', 'espionage activity'],
        'Stolen Property': ['stolen property', 'possession of stolen goods', 'receives stolen property', 'fencing', 'possessing stolen items', 'stolen goods', 'handling stolen property'],
        'Public Corruption': ['public corruption', 'bribery in public office', 'official misconduct', 'government corruption', 'corrupt public official', 'corruption in government', 'public office bribery'],
        'Terrorism': ['terrorism', 'terrorist activity', 'terror attack', 'acts of terror', 'terrorist act', 'terrorist plot', 'terrorism incident'],
        'Medical Fraud': ['medical fraud', 'healthcare fraud', 'medical scam', 'insurance fraud', 'fraudulent medical billing', 'healthcare deception', 'medical insurance fraud'],
        'Environmental Pollution': ['environmental pollution', 'toxic waste dumping', 'pollution violation', 'environmental contamination', 'pollution offense', 'illegal waste disposal', 'environmental damage'],
        'Corporate Espionage': ['corporate espionage', 'industrial spying', 'business espionage', 'corporate spying', 'espionage in business', 'corporate intelligence theft', 'industrial espionage'],
        'Child Exploitation': ['child exploitation', 'child pornography', 'exploitation of minors', 'child abuse imagery', 'pedophile', 'child exploitation case', 'exploitation of children'],
        'Counterfeiting': ['counterfeiting', 'fake goods', 'forgery', 'imitation', 'fake', 'counterfeit products', 'counterfeit currency', 'counterfeit items'],
        'Securities Fraud': ['securities fraud', 'investment fraud', 'stock fraud', 'securities scam', 'fraudulent securities', 'investment deception', 'stock market fraud'],
        'Breach of Privacy': ['breach of privacy', 'invasion of privacy', 'privacy violation', 'intrusion of solitude', 'privacy breach', 'privacy invasion', 'violating privacy'],
        'Credit Card Fraud': ['credit card fraud', 'identity theft', 'carding', 'credit card scam', 'credit card deception', 'credit card theft', 'fraudulent card use'],
        'Illegal Arms Trade': ['illegal arms trade', 'weapons trafficking', 'arms smuggling', 'weapons trade', 'illegal arms dealing', 'firearms trafficking', 'weapons sales'],
        'Money Counterfeiting': ['money counterfeiting', 'counterfeit currency', 'counterfeiting money', 'forged money', 'fake money production', 'counterfeit bills', 'counterfeit money scheme'],
        'Public Indecency': ['public indecency', 'indecent exposure', 'obscene behavior', 'lewd acts', 'indecent act in public', 'public obscenity', 'offensive behavior'],
        'Intellectual Property Theft': ['intellectual property theft', 'copyright infringement', 'IP theft', 'piracy', 'stealing intellectual property', 'counterfeit goods', 'copyright violation'],
        'insult':['Insult','Insulted','Insulting'],
        'accident':['rash','driving','rash driving','collision','accident'],
        'threat':['threat','hurt','pain']
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
        'collision': [279],
        'accident': [279,337],
        'beat':[321]
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
    p=random.randint(10,15)
    print(p)
    for ipc in output_ipc_sections:
        final_output[ipc]=output_ipc_sections[ipc]
        i=i+1
        if i==p:
            break

    return final_output





