# 답변 평가 프롬프팅 추가!

from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from Prompting import prompting
from ModelSelect import llm_model

# seed
import torch
import random
from transformers import set_seed
seed = 42
random.seed(seed)
torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)
set_seed(seed)


def format_docs(docs):
    global references
    references = docs
    context = ""
    for doc in docs:
        context += "\n\n" + doc.page_content
    return context

# Inference
prompt = prompting()
llm = llm_model()

results = []

question = {input}
retriever = {input} #elastic 불러오거나, 여기서 실행

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 답변 추론
print(f"Question: {question}")

# function calling or 직접 프롬프팅 과정 추가??

response = rag_chain.invoke(question).strip()

print(f"Answer: {response}")

# 답변 평가 프롬프팅 과정

ref_text = [reference.page_content for reference in references]
ref_path = [reference.metadata["FilePath"] for reference in references]
ref_name = [reference.metadata["DocName"] for reference in references]
ref_page = [reference.metadata["DocPage"] for reference in references]

# 결과 저장
results.append({
    "Question": question,
    "Answer": response,
    "Reference": ref_text,
    "FilePath": ref_path,
    "DocName": ref_name,
    "DocPage": ref_page,
})

torch.cuda.empty_cache()