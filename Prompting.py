# “function calling” or “질문 의도 파악하는 프롬프팅” 추가 필요한지 의논!
# elastic처럼 고정해두는 것도 괜찮은 것 같음



from langchain_core.prompts import PromptTemplate

# Prompt
#prompt = hub.pull("rlm/rag-prompt")
template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are an assistant for question-answering tasks.<|eot_id|><|start_header_id|>user<|end_header_id|>

Use the following pieces of retrieved context to answer the question. \
Provide an answer between one to three sentences and keep it concise. \
Answer only the question being asked. \
Write the answer in Korean.

context: {context}

question: {question}

answer:<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

def prompting(template):
    return PromptTemplate.from_template(template)