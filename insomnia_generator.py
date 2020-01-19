import os
from flask import current_app
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument("flask_instance")
    parser.add_argument("-n", "--name", default=os.path.basename(os.getcwd()),
                        help="Postman collection name (default: current directory name)")
    parser.add_argument("-b", "--base_url", default="{{base_url}}",
                        help="the base of every URL (default: {{base_url}})")
    parser.add_argument("-a", "--all", action="store_true",
                        help="also generate OPTIONS/HEAD methods")
    parser.add_argument("-s", "--static", action="store_true",
                        help="also generate /static/{{filename}} (Flask internal)")
    parser.add_argument("-i", "--indent", action="store_true",
                        help="indent the output")
    parser.add_argument("-f", "--folders", action="store_true",
                        help="add Postman folders for blueprints")
    args = parser.parse_args()

    print(args)
    w = mantap()
    print(w.nama)


if __name__ == "__main__":
    main()


def mantap():
    return "waw"