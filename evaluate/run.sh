#model = $1
#key1 = $2
#key2 = $3
#api_model = $4

python to_atomic_units.py --api_key $2 --model $1

python evaluate_with_pplai.py --api_key $3 --api_model $4 --model $1

python score.py --model $1

