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
## Evaluation
`model_to_evaluate`: The target model for evaluation. It should be the huggingface directory after the slash('/')  
e.g. Meta-Llama-3-8B-Instruct (O) meta-llama/Meta-Llama-3-8B-Instruct (X)  
`openAI_API_key`: Your openAI API key.   
`perplexityAI_API_key`: Your perplexityAI API key.  
`model_to_use_perplexityAI`: The model which will be used in perplexity AI.  
e.g. llama-3-8b-instruct  
```
cd evaluate
sh run.sh model_to_evaluate openAI_API_key perplexityAI_API_key model_to_use_perplexityAI
```

## Saving Results
The final DAHL score will be saved in a `.txt` file.
