import pandas as pd
from tqdm import tqdm
import time
import pickle
import json
import requests
import argparse

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--api_key", required=True, type=str, help="Your Perplexity AI API key"
    )
    parser.add_argument(
        "--api_model", required=True, type=str, help="Model name"
    )
    parser.add_argument(
        "--model", required=True, type=str, help="Model to evaluate"
    )

    return parser

parser = setup_parser()
args = parser.parse_args()
api_key = args.api_key
api_model = args.api_model
model = args.model

def ppl(question):
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
    "model": api_model,
    "messages": [
        {
            "role": "system",
            "content": "Be precise and concise."
        },
        {
            "role": "user",
            "content": "Is this true or false? Answer in one word.\n" + question
        }
    ]
}
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer " + api_key
}

    response = requests.post(url, json=payload, headers=headers)
    response = json.loads(response.text)
    response = response["choices"][0]["message"]["content"]

    return response

def count(lst, target):
    count = 0
    for element in lst:
        if element == target:
            count += 1
    return count


file = "../response/" + model 
    
response = pd.read_csv(file + ".csv")

score_list = []
tf_list = []
good = []

for i in tqdm(range(len(score_list),len(atomic_response_list))):  
    atomic = response["atomic"][i]
    try:
        atomic_list = atomic.split("\n")
    except:
        atomic_list = []

    tfs = []
    for j in range(len(atomic_list)):
        try:
            tf = ppl(atomic_list[j])
            
        except:
            time.sleep(2)
            try:
                tf = ppl(atomic_list[j])
            except:
                tf = "bad"

        tf = tf.lower()
        if "true" in tf and "false" in tf:
            tf = "bad"
        elif "true" in tf:
            tf = "true"
        elif "false" in tf:
            tf = "false"
        else:
            tf = "bad"
            
        tfs.append(tf)

    tf_list.append(tfs)

    try:
        score = tfs.count("true")/len(tfs)
    except:
        score = 0
    score_list.append(score)
    
    if len(tfs) == len(atomic_list) and (tfs.count("true") + tfs.count("false") == len(tfs)):
        good.append("good")
    else:
        good.append("bad")

    with open(file + "_tf.pickle", "wb") as f:
        pickle.dump(tf_list, f)
        
    with open(file + "_score.pickle", "wb") as f:
        pickle.dump(score_list, f)
        
    with open(file + "_good.pickle", "wb") as f:
        pickle.dump(good, f)

response["tf"] = tf_list
response["score"] = score_list
response["good"] = good

response.to_csv(file + ".csv", index = False)
    

