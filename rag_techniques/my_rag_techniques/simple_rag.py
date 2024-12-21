import os
import sys
import argparse

from dotenv import load_dotenv

# add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# load the .env file
load_dotenv()

# set the OPENAI_API_KEY environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

print(os.environ["OPENAI_API_KEY"])



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
  parser.add_argument("--path", type=str, default="../data/Understanding_Climate_Change.pdf",
                      help="Path to the PDF file to encode")
  parser.add_argument("--chunk_size", type=int, default=1000,
                      help="Size of each text chunk (default: 1000).")
  parser.add_argument("--chunk_overlap", type=int, default=200,
                      help="Overlap between consecutive chunks (default: 200).")
  parser.add_argument("--n_retrieved", type=int, default=2,
                      help="Number of chunks to retrieve for each query (default: 2).")
  
  

  return validate_args(parser.parse_args()) 

def main (args):
  return

if __name__ == '__main__':
  main(parse_args())