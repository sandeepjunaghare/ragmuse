import os
import sys
import argparse
import time

from dotenv import load_dotenv

# add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helper_functions import encode_pdf
from helper_functions import retrieve_context_per_question
from helper_functions import show_context
# load the .env file
load_dotenv()

# set the OPENAI_API_KEY environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

print(os.environ["OPENAI_API_KEY"])


class SimpleRAG:
  
  def __init__(self,path, chunk_size=1000, chunk_overlap=200, n_retrieved=2):

    print("\n--- Initializing Simple RAG Retriever ---")

    # Encode the PDF document into vector store using openai embeddings
    start_time = time.time() 
    self.vector_store = encode_pdf(path=path, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    self.time_records = {'Chunking': time.time() - start_time}
    print(f"Chunking Time: {self.time_records['Chunking']:.2f} seconds")

    self.chunks_query_retriever = self.vector_store.as_retriever(search_kwargs={"k": n_retrieved})

  def run(self, query):

    start_time = time.time()
    context = retrieve_context_per_question(query, self.chunks_query_retriever)
    self.time_records['Retrieval'] = time.time() - start_time
    print(f"Retrieval Time: {self.time_records['Retrieval']:.2f} seconds")
    show_context(context)


# function to validate command line inputs
def validate_args(args):
  if args.chunk_size <= 0:
    raise ValueError("chunk_size must be a positive integer")
  if args.chunk_overlap < 0:
    raise ValueError("chunk_overlap must be a non-integer")
  if args.n_retrieved <= 0:
    raise ValueError("n_retrieved must be a positive integer")
  return args

# function to parse command line arguments
def parse_args():
  parser = argparse.ArgumentParser(description="Encode a PDF document and test a simple RAG")
  parser.add_argument("--path", type=str, default="../data/Coaching_Psychology_Manual_Margaret_Moo.pdf",
                      help="Path to the PDF file to encode")
  parser.add_argument("--chunk_size", type=int, default=1000,
                      help="Size of each text chunk (default: 1000).")
  parser.add_argument("--chunk_overlap", type=int, default=200,
                      help="Overlap between consecutive chunks (default: 200).")
  parser.add_argument("--n_retrieved", type=int, default=2,
                      help="Number of chunks to retrieve for each query (default: 2).")
  parser.add_argument("--query", type=str, default="what is a drop volley?",
                      help="--query to test the retriever (default: what is the main cause of climate change?).")
  parser.add_argument("--evaluate", action='store_true',
                      help="Whether to evaluate the retriever's performance (default: false).")
  
  

  return validate_args(parser.parse_args()) 

def main (args):
  
    simple_rag = SimpleRAG(
        path=args.path,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        n_retrieved=args.n_retrieved    
    )

    simple_rag.run(args.query)



if __name__ == '__main__':
  main(parse_args())