import argparse
import pandas as pd
import openai
from tqdm import tqdm
import time
import pickle

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--model", required=True, type=str, default="gpt-4o", help="Name of model e.g. `gpt-4o`"
    )
    parser.add_argument(
        "--api_key", required=True, type=str, help="Your openAI API key"
    )
    parser.add_argument(
        "--temperature", required=False, type=float, default=0.6, help="Temperature e.g. 0.6"
    )

    return parser




def chat(question, model, temperature):

    prompt = f"""An examination question from the biomedical domain will be given. Please answer the question as truthfully as possible. If you don't know the answer to a question, tell me you don't know. Never share false information.\n {question}"""

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}, 
    ],
        
        temperature=temperature,
)

    return response['choices'][0]['message']['content']




if __name__ == "__main__":
    
    parser = setup_parser()
    args = parser.parse_args()
    model = args.model
    api_key = args.api_key
    temperature = args.temperature

    openai.api_key = api_key

    questions = pd.read_csv("./questions.csv")
    
    response_list = []
    

    for i in tqdm(range(len(questions))):
        question = questions["question"][i]
        try: 
            response = chat(question, model, temperature)
        except:
            time.sleep(5)
            response = chat(question, model, temperature)
        
        response_list.append(response)

        with open(f"./response/{model}.pickle", "wb") as f:
            pickle.dump(response_list, f)

    
    questions["response"] = response_list
    questions.to_csv(f"./response/{model}.csv", index = False)