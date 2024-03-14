"""This module contains the Flask app server to embed input texts using the provided instruction."""
import argparse
import time
from InstructorEmbedding import INSTRUCTOR
from sentence_transformers import SentenceTransformer
from flask import Flask, request
from utils.config import config

app = Flask(__name__)
model = None
model_name = None

@app.route('/status', methods=['GET'])
def live_check():
    return "App is running"

@app.route("/embed", methods=['POST'])
def embed():
    """Encodes texts with the embedding model and returns the resulting vectors."""
    # It uses the instructor model to encode the texts; the instruction is provided by the user.
    start_time = time.time()

    # Retrieve the request body as a dictionary
    request_body = request.get_json()

    # Extract the instruction and texts from the request body
    instruction = request_body.get('instruction')
    texts = request_body['texts']
    print(texts)
    if instruction is None:
        # Encode the texts using the model
        vector_array = model.encode(texts)
    else:
        # Encode the instruction and texts using a model
        vector_array = model.encode([[instruction, text] for text in texts])

    # Convert the vector array to a list of vectors
    vector_list = [vector.tolist() for vector in vector_array]

    # Return the resulting vectors as a list
    return {
        "vectors": vector_list,
        "model": model_name,  # Return the name of the model
        "elapsed_time": time.time() - start_time
    }

if __name__ == '__main__':
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Run the embedder")

    # Define arguments/parameters to override
    parser.add_argument("--model", type=str, help="Override the model name from config.",
                        default=config.get("MODEL", "model_name"))
    parser.add_argument("--port", type=int, default=config.getint("API", "port"),
                        help="Port to run the Flask app on.")
    parser.add_argument("--host", type=str, default=config.get("API", "host"),
                        help="Host to run the Flask app on.")

    args = parser.parse_args()

    # Load the model
    if 'instructor' in args.model.lower():
        model = INSTRUCTOR(args.model)
    # elif 'minilm' in args.model.lower():
    #     # Your logic for handling 'minilm'
    #     pass this not needed
    else:
        model = SentenceTransformer(args.model)

    model_name = args.model

    # Run the app
    app.run(debug=True, host=args.host, port=args.port)