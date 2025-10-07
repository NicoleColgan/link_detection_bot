import argparse
import os

"""are we still calling validate dir"""

def build_parser():
    """handles parsing command line arguments"""
    parser = argparse.ArgumentParser(description="Link checker")
    parser.add_argument("-i", "--input", required=True, help="Directory containing files (.md, .html, .pdf")
    parser.add_argument("-o", "--output", default=".", help="Output directory for CSV")
    return parser

def validate_directory(path: str) -> str:
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"{path} is not a directory")
    return path