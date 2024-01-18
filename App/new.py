from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import GradientLLM

import os
from getpass import getpass

if not os.environ.get("GRADIENT_ACCESS_TOKEN", None):
    # Access token under https://auth.gradient.ai/select-workspace
    os.environ["GRADIENT_ACCESS_TOKEN"] = "smX00wSAmvAZSJLLUhkVOqf0UYhdStj3"
if not os.environ.get("GRADIENT_WORKSPACE_ID", None):
    # `ID` listed in `$ gradient workspace list`
    # also displayed after login at at https://auth.gradient.ai/select-workspace
    os.environ["GRADIENT_WORKSPACE_ID"] = "880ee27e-5b8f-4057-a266-209896ce267c_workspace"


complaint_text = "In Sevam, Mr. Police Station Officer Police Station Jaipur subject:- To register a report. Sir, it is requested that I Manju Devi went to work as usual in Sanganer on 7.4.17 am yesterday at 9 am when I came home at 6.30 in the evening, my daughter Puja was not found at home (Pooja) daily At 12.30, Aryan Inter Nession School goes to Rampura Road and comes home at 4.30 pm. Puja falls in the 11th class, but when we did not come home till 6.30 am tomorrow, we found all the places around but they did not get the report. Huliya Naam Puja Raghuvanshi daughter Rameshwar ji age 15 years, caste hero colors, colorful length of 4.5 feet, left with left legs, the clothes of the school are worn in the school dress. 9057645110. Pratyaraya Angutha Nishani Manju Devi wife Rameshwar Nayak resident village Ladana police station Fagi Hall Hall House No. 38 Gulab Nagar Railway Station Sanganer Police Station Muhana Jaipur Mo. 8209107811, 9587305353 action police ………………… is certified that the above report Bakht Hindi Valvadiya Mrs. Mannu Devi wife late Shri Rameshwar caste hero age 35 years resident village Ladana police station Fagi District Jaipur Hall tenant house no. In front of 38 Gulab Nagar railway station Sanganer, the police station Muhana Jaipur presented the police station, whose copy was recorded in the computer. Case Section 363 IPC from Majmoon Report It is found to come to Vaku. Adi report sued the report no. 222/17 Section is recorded in the above and Tafish S.I. Mr. Bane Singh was performed. F.I.R. The copy was released as per rules. A copy was given free of cost to Mustagisa. Hulia:- Varana Kumari Pooja Ranghuvanshi age 16 years in length 4.5 inch color is applied with a dark left leg. In the legs, we are wearing a plowing and wearing a school dress, who is a student of class 11th."
ipc_dict = {323: 'Robbery', 363:"Kidnapping", 201:"Erasing evidence"}
question = "Given the following FIR description, {complaint_text}\nTell me which of the following IPC sections could be applied\n{ipc_dict}"

llm = GradientLLM(
model="62f07e2b-c760-46c4-b512-452640dc3b63_model_adapter",
model_kwargs=dict(max_generated_token_count=128),
)
question = f"Given the following FIR description, {complaint_text}\nTell me which of the following IPC sections could be applied\n{ipc_dict}"

template = """Question: {question}

Answer: """

prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)
response = llm_chain.run(question=question)
response_text = response.split("Response: ", 1)[-1].strip()
print(response_text)


# This code is giving same response even after changing complaint_text and ipc_dict