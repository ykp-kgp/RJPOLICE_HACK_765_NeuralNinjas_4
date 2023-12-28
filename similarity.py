import pandas as pd
from gensim.models import FastText
from gensim.parsing.preprocessing import preprocess_string, strip_multiple_whitespaces, strip_punctuation, strip_numeric, remove_stopwords
import numpy as np

# Load IPC sections from CSV with a specified encoding
ipc_data = pd.read_csv('ipc.csv', encoding='latin1')

# Assuming 'Section Content', 'Section Title', and 'Section Number' are column names in your CSV
sections = ipc_data[['Section Content', 'Section Title', 'Section Number']]

# Define text preprocessing function
def preprocess_text(text):
    text = str(text)  # Convert to string to handle NaN values
    text = text.lower()
    text = strip_multiple_whitespaces(text)
    text = strip_punctuation(text)
    text = strip_numeric(text)
    text = remove_stopwords(text)
    return text.split()  # Return tokenized text

# Handle NaN values in 'Section Content' column by replacing them with an empty string
sections['Section Content'].fillna('', inplace=True)

# Train a FastText model using IPC section content
section_texts = [preprocess_text(text) for text in sections['Section Content']]
model = FastText(sentences=section_texts, vector_size=100, window=5, min_count=1, workers=4, sg=1)


# Preprocess complaint text
complaint_text = "Page 1: Pras. Kafuke Rs. First Information Report (Under Section. 54 Penal Procedure Code) Book no 'Jaipur Police Station Principal Reserve Center, Shree Churo Jai Year 2022 Gasm ... 2 ......../2022 dated .CaC Act (amended) 208 2.3 (!) (V) Supported Section 13 (2) . Dhara -09, 20 V B.D., Stream. Act and Section. Rogenamcha common report number ......../>, 2. The day of the subsequent decreasing day, date, The date of receiving information at the police station, 3. Variety of Information:- Written / oral. written (s / o). Dhadi belongs to the outer border from this police station. 5. complainant (3). Direction and distance from police station close Gati- -Jayamdehi no. .Bit number, Police Station. / Informant. , Deputy Superintendent of Police, Shree Nuro, Chowki Dholpur (anonymous (And). Father's / Husband's name Take Known/A Gashree Generous Resident Sir, Son Mr. The Are living Has been with Grained Suspicious (C) Date of birth, year ... National Date of issuance of passport number. Replace to be released. Comfort Address. Vyara of unknown suspected accused with all the specialty:- 'Yogendra Singh Sehwal, the then Superintending Chani Engineer, (vigilance) minerals and [No Department Bharatpur Hall Superintending Engineer, (Vigilance) Mineral Building Udaipur Hall SP 02 Silver Place Apartment Near Anannu and Vatika, Ashirwad Nagar, Pura, Udaipur. Madhubala wife Mr. Yogendra Singh Sahwal resident V-3/285, Flat No. 102, Vaishali Nagar Jaipur / Reason for delay in suit by informant:- No delay / Indulged property, men (if required, apply an additional page) / Total value of property involved / UD, Case Number (If if it) ... First Itila Report (If required, apply an additional page):- Suspected officer Mr. Yogendra Singh Sahwal (Rat. Saprachar - 2 (09504040 and). The original form is Suraj Vihar Colony, Lohagal Road, near Jatia Hill, Ajmer. 'Married officer married to Mrs. Madhuwala (90515 (0 989. - 8 720959423 R ₹) Suspected officer education from prestigious educational institutions to his son and daughter Is. In the first appointment of the officer in the year 7029, the post of Assistant Mining Engineer Fu. Hui Six Is Page 2: And the time is, but by getting promotion, the Superintending Engineer, (vigilance) mineral building Working on Udaipur. Suspected officer important at various places in the mineral department There has been sorrow on the posts. Common image of officer accused by confidential verification corrupt officer It has been known to be. The Chief Officer has important areas of various areas during his service period Locations of locations Investing in the promotions is also known from the sources. Verification The officer's family background is known to be normal. Recorded against suspected officer Case number 189/204 dated 20,08.204 food found in search Excessive assets have been found to be earned to be earned. It is noteworthy that suspect Officer KS: Makrana district misuse of post while holding the post of Khani Engineer in Nagaur Case of Association of 289 // in 2064 Is. 96/2007 and 97/200. It has also been found to be recorded. Also the case no. Challan has also been submitted against the Honorable Officer Following is the details of valid income, expenditure and earned assets earned by the suspected officer:- G. Valid income from known:-. Check period by the same officer (1993 to 20 0820 4) State Services From dying to the year 20.08.204, earned from salary allowances etc. Pure remaining income - 56,27,76/ -. 2 Brahm's wife Mrs. Madhubala's Income Tax Betractories Valid projected income according to - .85682/ - 3. S, O. Income from home/ car loan taken by 20: 25,000/ 4. S.O. IPR according to house rent Mi Income -, 80,000/ - Total estimated valid income 05,90.368 Cost :- , Valid income according to the salary, allowance received by the suspected officer, Rs 56,27,76/Rs. Ka /3 part family estimated kitchen expenses:- 8,73,905 / 2. Estimated expenditure on the education of the son-daughter of 2 officer- 17,00,000/ 3. Fuel / maintenance of vehicles used during check period, Estimated expenditure on insurance - 5,00,000/ 4. Estimated expenditure as installment on home / car loan - 2,32,820 / No cost 54,06,725/ Total estimated valid income 8580,388-54,06725- 3,83843 // Estimated value of earned assets +, 85,00.054,/ Income from the earned assets (, 95,00,854-37,83,643 No, 63,7,277) Description of assets earned by accused:- Tax: [Details of property [Special details of Bark [Special Description No. Name is there [House no ... B-3,/285. Prasan, _ 289,/2074 K. Food | 3,86,300 Flat no. 02. Chitrakoot, according to search , Vaishali Monitor Jaipur. I Found household items that [The House | B 3:55 | Food of 280 2204 Page 3: Flat no Gold found in 706 Silver jewelery, domestic stuff According to 3. Time food search house In cash found in Amount Ar accused wife of! Mrs. Madhubala , Returned to Q.S. 289/204. Eating In the absence of search Jun 0 4. 08 kinashar kha, cross .28. , , D.N. 5. 08 Kishizarikasha, cross Rud 0 Ta, Sha 90. 400006428] Li tany A 5000 Conversation 5/(0707 , 6. | ICICI Account no 004507579529 , 7. | ICICI Policy No. 06776609 [Love | 30,000 ४ Car Hanbai RJ % , CB 628 Go H, 47,083 9. | ICIS Fix Deposit! , Advance ... Branch Vaishali. City. Jaipur Account no 023570002477 Wife 250,000 0. | Rubspri Life Policy No. 5330030 Self 005 Ja, Gay ECIC Life | This policy is no. 6258 No No. CICA F This policy is no. 620587 Ltd. Kad 3. | Mobile 'Simamsung 9082 Self 9,006 , 44. | Godrej Intereo D. 05. [Slow | 32,000 3,900 5. | LIC Policy Number Self 59,386 285. F. No. | ... 02, _ Chitrakoot _ Scheme Ajmer Reed Jaipur Self Suspect in the said residential house Officers with family Residence and year 200. In Purchased ... has gone, registered 22, 000/000/ under document Rupee face value f. , 30.220, // is Rs. In addition to construction work Internal domestic Saj .. decor .. on. Closely 45,00,000/-for expenditure A. 8, B.220 Page 4: Have an estimate. Art type total 38,4,220/ Rs. Have an estimate. Company P, 167: 00080 01/200: Sing. Star INALTH (/00389 Yoresh Policy no. 10 // 07,/2073/ P,/ 17020/ | Self Tidy 762/ Statement Account Garh Sundaram Mavival Fund No BVNAD 003278 Wife 20.0 Account Ferry Mucharwal Bank fund 3072084,/09 Ltd. Ltd 322 20. , Bye , Policy [IG Life U-4003805 , Tany Fifth note of musical scale. 80,000 Account Hee Tata. MU 890705,/57 fund Khw 40,000 22. | Rare IF Muthawal Fund of statement Per no. 0499 Laca Sh -6 Per no Oo | Birla Sun Life Muthawal Fund account ... statement (003900784 Laca B 0,0 Per no Birla Sen Life Muthawal , Fund account. Statement (00439582 Nal tany Ltd. 25. | Kotak Mucharwal Account 44 fund No Wife 30,06 , Investment Mucharwal Account , 1253765/74 fund No Wife [That 5,000 , 27. | Kotak , Invest in Mucharwal Account 357063/95 fund No 20.0 , Kotak In the vest 63 Mucharwal Account Sculpture No , 138526/26, 247690/ He 0.0 29. | Kotak Mucharwal West , 1247690/63 fund No Took 0.0 Account , 439 36 | ICIC Productial. Muthawal. fund Statement 2995444 Bank Wife G -100 , 3. | Shit Shiga The AS0 is 00 190. 94678 Fly | N.,000 , 32. | Prison Mucharwal fund , Account statement account no , Bakha 207 Yudi M Wife C 40 40 Page 5: Name of CICA Receipt bank 33. | JM Mucharwal Statement No. 7987] Financial 'fund . Account No. Folio Could Wife Moment 34. | JM Mucharwal Statement No. 7988: , Finanic Fund account Food Follows D 492 Self Patesha 35. | JM Mucharwal Statement No. 798 In ninenexic Fund account No, Folio 12845 Self , 483 36. | CAM account Statement Letter .. service Solutions | Partner Folio , No. 104309592 Wife 24,000 O aa Vishnu Stokes Prali Wife 4,424 I went to ICICI Bank Check of Jaipur 2083 Date 06.03.204 C, 00,000 5. [residential plot number 39 Rohgi Nagar Phase-2 That JDA Jayapu Father Name Real in search during food. Document of suspected officer. Japti from the place of residence. Of Ki ki A.30,200 40. | SB Of Ajmer. Account number 10200637378 Self Kanm ICICI of Account .. Bank Fun _ 0235000 2842. Saurabh Tower Vaishali City jayupu Self 25600 I Bank Andheri Self C.22.596 Jaipur 570774 They are in! Account Number 507__ 5,89.258 44. | PNV Ajmer Dow Bank court road Account. Number ) 00357053. Ltd. Sha, 50965 Honda SH Found km 4 [a scooty pleasure hero No, RJ 27 7664. Jo. 5380 The tur is gone. Scan 0,000 46. | House, plot no ... 43 , Jatia Ajmer Near Hills Total area 292. 63 sq. , Suspect in the said residential house Officers with family Express"
complaint_tokens = preprocess_text(complaint_text)

# Calculate complaint vector
complaint_vectors = [model.wv[word] for word in complaint_tokens if word in model.wv]
complaint_vector = np.mean(complaint_vectors, axis=0) if complaint_vectors else np.zeros(model.vector_size)

# Normalize the complaint vector
complaint_vector /= np.linalg.norm(complaint_vector)

# Calculate similarity scores between complaint and IPC sections
similarity_scores = {}
for idx, row in sections.iterrows():
    section_number = row['Section Number']
    section_title = row['Section Title']
    section_tokens = preprocess_text(row['Section Content'])

    section_vectors = [model.wv[word] for word in section_tokens if word in model.wv]
    section_vector = np.mean(section_vectors, axis=0) if section_vectors else np.zeros(model.vector_size)
    
    # Normalize the section vector
    section_vector /= np.linalg.norm(section_vector)

    # Calculate cosine similarity
    similarity = np.dot(complaint_vector, section_vector)
    similarity_scores[section_number] = (section_title, similarity)

# Sort similarity scores and get top 10 matching sections
top_matching_sections = sorted(similarity_scores.items(), key=lambda x: x[1][1], reverse=True)[:10]

# Print IPC section number and section title of top matching sections
for section_number, (section_title, similarity) in top_matching_sections:
    print(f"IPC Section Number: {section_number}, Section Title: {section_title}, Similarity Score: {similarity:.4f}")
