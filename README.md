# DAHL

This repository provides the benchmark dataset and automated pipeline for hallucintion evaluation of long-form text generated by Large Language Models.

## Dataset Construction

We generate possible examination questions based on research papers crawled from PMC through gpt-4-1106-preview and manually filter out, leaving only high-quality questions.   

<img width="400" alt="construction" src="https://github.com/user-attachments/assets/1f86a354-b7bc-48b4-8c22-f61dea7f85b7">

## Evaluation Pipeline

The automtaed evaluation pipeline includes two stages: Splitting the response into atomic units, and checking the factuality of each atomic unit.  

<img width="600" alt="pipeline" src="https://github.com/user-attachments/assets/29cd8765-461e-4632-b520-302b2ab2d260">



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

## Citation 
```
TBD
```
