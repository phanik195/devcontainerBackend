# Embedder

## What is it?

** Embedded** is a REST API application that embeds input texts. It supports instruction and standard models. Behind the hood, it can use any SentencePiece model, and also [Instructor model](https://huggingface.co/nlp/instructor-xl). This is a standalone app module to run as a service.

## Prerequisites

- Python 3.10+

## Installation

```bash
pip install -r requirements.txt
python3 run_api.py
python3 run_api.py --help
```



## Sample Request and 


## Sample Request format

```json
{
  "instruction": "IF Represent the source code snippet for retrieving relevant code:",
  "texts": [
    "If some code",
    "some other code"
  ]
}
```

## Sample Response format
```json
{
  "vectors": [
    [0.021235722088537216, 0.059756574549510307, 0.048286762088537218, 0.01975635997954003561],
    // ... other vectors
  ],
  "model": "sentence-transformers/all-MihiLM-L6-v2",
  "elapsed_time": 1.0260090827941895
}
```

# Testing

Once the application has started, use the below sample `curl` command to verify the endpoint works correctly:

```bash
curl --location 'http://127.0.0.1:5003/embed' --header 'Content-Type: application/json' --data '{
  "instruction": "Represent the source code snippet for retrieving relevant code:",
  "texts": [
    "some code",
    "some other code"
  ]
}'

```
