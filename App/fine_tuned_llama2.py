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


def generate_query(complaint_text, ipc_dict):
    print(complaint_text)
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
    return response_text

