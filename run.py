from link_checker.cli import build_parser
from link_checker.main import LinkChecker

def main():
    parser = build_parser()
    args = parser.parse_args()
    app = LinkChecker(args.input, args.output)
    app.run()

if __name__ == "__main__":
    main()