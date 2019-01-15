"""Main entrypoint."""

import argparse
from project.random_name_generator import RandomNameGenerator

PARSER = argparse.ArgumentParser(description='Random Name Generator')
PARSER.add_argument('numgen', type=int, nargs='?',
                    help='The number of names to generate. Defaults to 10.')
PARSER.add_argument('-f', '--file',
                    help='The file containing plain text sample data of names.')
PARSER.add_argument('-m', '--max-length', type=int, nargs='?', const=7,
                    help='Specifies a maximum length for generated names.')

def main():
    """
    Initialize and run the random name generator.
    """
    # Parse command line arguments and set defaults
    args = PARSER.parse_args()
    if args.numgen is None:
        args.numgen = 10
    # Initialize generator
    params = {
        'file': args.file,
        'max_length': args.max_length
    }
    generator = RandomNameGenerator(params)
    # Generate random names
    print("Generating %d names...\n" % (args.numgen))
    for _ in range(args.numgen):
        generator.generate()
    #TEST
    #generator.generated_names = ["Aesos","Apollo","Argus","Aura","Chara", "Chron", "Dio","Gaioxia","Hypea","Hyperselo","Kratos","Medusa", "Ouryne","Ouralo","Palanomes","Peritras","Talasa","Targia","Urus","Zeus"]
    #generator.generated_names = ["Anzu", "Asuki","Chiyo","Futaba","Hina","Ichikao","Kyouko","Makoto","Rien","Tsubaki"]
    # Sort and print list of generated names
    generator.generated_names.sort()
    for _ in range(len(generator.generated_names)):
        print(generator.generated_names[_])

# Identify this module as main
if __name__ == "__main__":
    main()
