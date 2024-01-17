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



# llm = GradientLLM(
#     # `ID` listed in `$ gradient model list`
#     model="fda8e0b4-e908-4644-8e9c-ecc43ffe57ab_model_adapter",
#     # # optional: set new credentials, they default to environment variables
#     # gradient_workspace_id=os.environ["GRADIENT_WORKSPACE_ID"],
#     # gradient_access_token=os.environ["GRADIENT_ACCESS_TOKEN"],
#     model_kwargs=dict(max_generated_token_count=128),
# )


def generate_query(complaint_text, ipc_dict):
    question = "Given the following FIR description, {complaint_text}\nTell me which of the following IPC sections could be applied\n{ipc_dict}"
    llm = GradientLLM(
    model="fda8e0b4-e908-4644-8e9c-ecc43ffe57ab_model_adapter",
    model_kwargs=dict(max_generated_token_count=128),
)
    template = """Question: {question}

Answer: """
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response = llm_chain.run(question=question)
    response_text = response.split("Response: ", 1)[-1].strip()
    return response_text

