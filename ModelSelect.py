# llama 등 모델 계열에 따라 tokenizer 설정도 필요함
# tokenizer에서 eos와 같은 설정이 모델마다 필요할 수도 안 필요할 수도 있음 
# FAISS는 Elastic으로 변경
# documents는 청킹 쪽에서 생성할거면, 생성한 값 받도록 해야 됨

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline,
    BitsAndBytesConfig
)

from langchain_huggingface import HuggingFacePipeline
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import warnings
warnings.filterwarnings('ignore')

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


# Embedding
def embedding_model(embed_name):
    model_path = embed_name
    model_kwargs={"device": "cuda"}
    encode_kwargs={"normalize_embeddings": True}
    embeddings = HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    torch.cuda.empty_cache()

    return embeddings


# Model
def llm_model(model_name):
    model_id = model_name
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    eos_token_id = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    text_generation_pipeline = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        temperature=0.1,
        do_sample=True,
        return_full_text=False,
        max_new_tokens=256,
        eos_token_id=eos_token_id,
    )

    hf = HuggingFacePipeline(pipeline=text_generation_pipeline)
    # llm = hf
    return hf


# Retriever
embeddings = embedding_model()
faiss_db = FAISS.from_documents(
    documents=docs,
    embedding=embeddings
)
faiss_retriever = faiss_db.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 10,
    }
)