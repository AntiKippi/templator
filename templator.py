#!/usr/bin/env python3

import argparse
import json
import os
import string
import sys

class Constants:
    NAME_KEY_PLACEHOLDER="<name-key>"
    DEFAULT_NAME_KEY= "name"
    DEFAULT_NAME_TEMPLATE=f"${NAME_KEY_PLACEHOLDER}.html"

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def main():
    parser = argparse.ArgumentParser(description="Create files based on a template.")
    parser.add_argument("-f",
                        "--force",
                        action="store_true",
                        help="Overwrite existing files without asking")
    parser.add_argument("-k",
                        "--name-key",
                        required=False,
                        default=Constants.DEFAULT_NAME_KEY,
                        help=f"The JSON key which should be used as name. Defaults to \"{Constants.DEFAULT_NAME_KEY}\".")
    parser.add_argument("-n",
                        "--name-template",
                        required=False,
                        default=None,
                        help=f"The template which should be used for the name. Defaults to \"{Constants.DEFAULT_NAME_TEMPLATE}\".")
    parser.add_argument("-o",
                        "--output-dir",
                        required=False,
                        help="The directory to write the files to. If omitted the current working directory will be used.")
    parser.add_argument("-t",
                        "--template",
                        required=False,
                        help="The template file to use. If omitted stdin will be used.")
    parser.add_argument("-r",
                        "--replacements",
                        required=True,
                        help="A JSON file containing an array of replacement dictionaries.")

    args = parser.parse_args()
    force = args.force
    name_key = args.name_key
    name_template_arg = args.name_template
    output_dir = args.output_dir
    template_file = args.template
    replacements_file = args.replacements

    if name_template_arg is None:
        name_template_arg = Constants.DEFAULT_NAME_TEMPLATE.replace(Constants.NAME_KEY_PLACEHOLDER, name_key)

    name_template = string.Template(name_template_arg)

    with open(replacements_file, 'r') as f:
        replacements = json.load(f)

    template_content = ''
    if template_file is None:
        template_content = sys.stdin.read()
    else:
        with open(template_file, 'r') as f:
            template_content = f.read()

    template = string.Template(template_content)

    if output_dir:
        os.chdir(output_dir)

    i=0
    for replacement in replacements:
        if name_key not in replacement:
            eprint(f"error: Array element {i} is missing the \"{name_key}\" key. The replacements file is malformed.")
            sys.exit(1)
        i += 1

    for replacement in replacements:
        outfile = name_template.safe_substitute(replacement)

        if not force and os.path.exists(outfile):
            ans = input(f"File {outfile} already exists. Overwrite? [y/N]: ").upper()
            if ans != 'Y':
                continue

        res = template.safe_substitute(replacement)

        with open(outfile, 'w') as f:
            f.write(res)

if __name__ == '__main__':
    main()