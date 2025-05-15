# blah

import argparse
import sys

 # basic script that prints out whatever the user inputs on the command line back to them
class Main():

     def __init__(self, args):
       self.args= args
       

     def retrieve_input(self):
     # handles parsing command line arguments
        parser = argparse.ArgumentParser( 
        description="takes in a command line argument"
        )

        parser.add_argument("input", help="input file or value") #what arguments the script expects


        self.args = parser.parse_args()

        print(f"You've entered: {self.args.input}") #prints out the input for now, obviously this will change later
    
    
     def run(self):
        self.retrieve_input()
        
        
        

def main(args):
   app = Main(args)
   app.run()


if __name__ == "__main__":
    main(sys.argv[1:])