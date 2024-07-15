import pandas as pd
import argparse

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--model", required=True, type=str, help="Model name"
    )

    return parser

parser = setup_parser()
args = parser.parse_args()
model = args.model

response = pd.read_csv("../response/"+model+".csv")

good_rows = response[response['good'] == 'good']
average_score_for_good_responses = good_rows['score'].mean()
print(f"DAHL Score of {model}: {average_score_for_good_responses}")

with open(f"../result/{model}.txt", "w") as f:
    f.write(f"DAHL Score of {model}: {average_score_for_good_responses}")