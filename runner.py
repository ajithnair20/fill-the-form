import argparse

# Instantiate a parser to parse command line arguments
from form_filler.form_filler import fill_form_by_url

runner_parser = argparse.ArgumentParser(description='This parser parses command line arguments for the runner.py script')

# Add command line arguments to be parsed
runner_parser.add_argument('--url', type=str, default="https://github.com/join", required=False, help="The URL to be filled.")
runner_parser.add_argument('--iterations', type=int, default=1, required=False, help="The no. of iterations to run.")

if __name__ == '__main__':
    parsed_arguments = runner_parser.parse_args()
    fill_form_by_url(parsed_arguments.url, parsed_arguments.iterations)
