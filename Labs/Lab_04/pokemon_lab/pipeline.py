import os
import sys

from update_portfolio import main as update_portfolio_main
from generate_summary import main as generate_summary_main

def run_production_pipeline():
    print("Start running the production pipeline for pokemon cards ETL...", file=sys.stderr)
    print("Start updating the portfolio...")
    update_portfolio_main()
    print("Finish updating. Start generating summary...")
    generate_summary_main()
    print("Production pipeline complete.", file=sys.stderr)

if __name__ == "__main__":
    run_production_pipeline()