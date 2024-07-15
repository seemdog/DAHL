import argparse
import pandas as pd
import openai
from tqdm import tqdm
import time
import pickle

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--api_key", required=True, type=str, help="Your openAI API key"
    )
    parser.add_argument(
        "--model", required=True, type=str, help="Model name"
    )

    return parser

parser = setup_parser()
args = parser.parse_args()
api_key = args.api_key
model = args.model

openai.api_key = api_key


file = "../response/"+model 

atomic_facts = []

data = pd.read_csv(file + ".csv")
response = data["response"]


def chat(text, q):
    MODEL = "gpt-3.5-turbo"

    previous_prompt = "An examination question from the biomedical domain will be given. Please answer the question as truthfully as possible. If you don't know the answer to a question, tell me you don't know. Never share false information."

    text = text.replace(previous_prompt, "")
    text = text.replace(q, "")
    text = text.strip()

    USER_INPUT_MSG = f"""Please split the sentences in the following text into smaller sentences which contain just one single fact. If the last sentence is incomplete, just ignore the last sentence and split only the previous sentences that are complete. The sentences should be separated with a newline. Avoid using pronouns. Each sentence should be a proper full sentence which contains subject and verb. \n
    
TEXT: She is a student and he is a teacher.
SEPARATED SENTENCES: She is a student.\nHe is a teacher.

TEXT: The symptoms include: coughing, headache, toothache.
SEPARATED SENTENCES: The symptoms include coughing.\nThe symptons include headache.\nThe symptoms include toothache.

TEXT: Patrick enjoys playing basketball with his son, which is helpful for his son's emotional development.
SEPARATED SENTENCES: Patrick enjoys playing basketball with his son.\nPatrick playing basketball with his son is helpful for his son's emotional development.
    
TEXT: {text}
SEPARATED SENTENCES: 
    """

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": USER_INPUT_MSG}, 
            
    ],
        
        temperature=0,
)

    return response['choices'][0]['message']['content']


for i in tqdm(range(len(atomic_facts), len(response))):
    try:
        output = chat(str(response[i]), data["question"][i])
        atomic_facts.append(output)
    except:
        time.sleep(5)
        output = chat(str(response[i]), data["question"][i])
        atomic_facts.append(output)
        
    with open(file + '_atomic.pickle', 'wb') as f:
        pickle.dump(atomic_facts, f)
    
data["atomic"] = atomic_facts   
data.to_csv(file + ".csv", index = False)