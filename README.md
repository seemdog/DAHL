# DAHL

## Install
```
git clone https://github.com/seemdog/DAHL.git
cd DAHL
```
## Response Generation
Huggingface Models
```
python generate_response_hf.py --model meta-llama/Meta-Llama-3-8B-Instruct \
--temperature 0.6 \
--max_new_tokens 256
```
OpenAI Models
```
python generate_response_gpt.py --model gpt-4o \
--api_key YOUR_API_KEY \
--temperature 0.6
```
