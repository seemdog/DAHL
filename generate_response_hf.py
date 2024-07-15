import pandas as pd
import argparse
from tqdm import tqdm
import random
import pickle
from transformers import AutoTokenizer, AutoModelForCausalLM

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--model", required=True, type=str, default="meta-llama/Meta-Llama-3-8B-Instruct", help="Name of HF model e.g. `meta-llama/Meta-Llama-3-8B-Instruct`"
    )

    parser.add_argument(
        "--temperature", required=False, type=float, default=0.6, help="Temperature e.g. 0.6"
    )

    parser.add_argument(
        "--max_new_tokens", required=False, type=int, default=256, help="Maximum new tokens e.g. 256"
    )

    return parser



if __name__ == "__main__":
    
    parser = setup_parser()
    args = parser.parse_args()
    model_name = args.model
    temperature = args.temperature
    max_new_tokens = args.max_new_tokens

    tokenizer = AutoTokenizer.from_pretrained(model_name) 
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto") 

    model_name = model_name[model_name.find("/")+1:]
  
    questions = pd.read_csv("./questions.csv")
    
    response_list = []
    
    for i in tqdm(range(len(response_list), len(questions))):
        question = questions["question"][i]
        instruction = "An examination question from the biomedical domain will be given. Please answer the question as truthfully as possible. If you don't know the answer to a question, tell me you don't know. Never share false information."
    
        prompt = f"instruction\nQUESTION: {question}\nANSWER: "
        inputs = tokenizer(prompt, return_tensors="pt",return_token_type_ids=False).to("cuda")
    
        outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=True, top_p=0.9, temperature = temperature, eos_token_id=tokenizer.eos_token_id)
        response = tokenizer.batch_decode(outputs, skip_special_tokens=True)

        response = response[0].replace(prompt, "")
        response = response.strip()
        
        response_list.append(response)
    
        with open(f"./response/{model_name}.pickle", "wb") as f:
            pickle.dump(response_list, f)
 

    questions["response"] = response_list

    questions.to_csv(f"./response/{model_name}.csv", index = False)

