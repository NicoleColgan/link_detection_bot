

import argparse

 # basic function that prints out whatever the user inputs on the command line back to them
def main():

    # handles parsing command line arguments
    parser = argparse.ArgumentParser( 
        description="takes in a command line argument"
    )

    parser.add_argument("input", help="input file or value") #what arguments the script expects


    args = parser.parse_args()

    print(f"You've entered: {args.input}") #prints out the input for now, obvioulsy will change later

 
if __name__ == "__main__":
 main()