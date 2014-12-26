from __future__ import print_function
from io import open

from github3 import login, create_gist
import argparse
import sys
import os

try:
    # Python 2
    prompt = raw_input
except NameError:
    # Python 3
    prompt = input

def two_factor_function():
    code = ''
    while not code:
       	# The user could accidentally press Enter before being ready,
       	# let's protect them from doing that.
      	code = prompt('Enter 2FA code: ')
    return code

def usage(argv0):
    print ("\tusage: %s [-h] -u <username> -p <password> -f <input filename> -d <description>\n"%argv0, file=sys.stdout)
    print ("\tusage: %s -f <input filename> -d <description>\n"%argv0, file=sys.stdout)

def is_valid_file(parser,arg):
    if not os.path.exists(arg):
        parser.error("File %s not found"%arg)
    else:
        return arg

def read_file(infilename):
    try:
        infile = open(infilename, 'r')
        content = infile.read()
        infile.close()
        return content
    except IOError as err:
	print("Error reading file: %s"%str(err), file=sys.stderr)


def gist_up(args):
    basename = os.path.basename(args.filename)
    files = {
        basename: {
            'content': read_file(args.filename)
        }
    }

    if args.user and args.passwd:
        gh = login(args.user, args.passwd)
        gist = gh.create_gist(args.description, files, public=args.private)
        return gist.html_url
    elif args.user and args.passwd and args.two-factor:
	gh = login(args.user, args.passwd, two_factor_callback=two_factor_function)
        gist = gh.create_gist(args.description, files, public=args.private)
        return gist.html_url

    else:  # Anonymous gist, public by default.
        gist = create_gist(args.description, files)
        return gist.html_url


def main(argc, argv):
    parser = argparser.Argumentparser(description='Upload code/text files to Gist on Github.')
    parser.add_argument("-i", "--input", dest="filename", required=True,
    		help="Input code/text file to upload to Gist",
    		metavar="FILENAME",type=lambda x:is_valid_file(parser,x))
    parser.add_argument("-u", "--user", required=False, help="Username for Github for non-anonymous uploads.")
    parser.add_argument("-p", "--passwd", required=False, help="Password for Github for non-anonymous uploads.")
    parser.add_argumant("-d", "--description", required=True, help="Description of the gist.")
    parser.add_argument("--two-factor", required=False, action='store_true', help="Enable two-factor authentication.")
    parser.add_argument("--private", required=False, action='store_true', 
		default=False, help="Create a private gist, default if public")
    args = parser.parse_args()

    gist_url = gist_up(args)
    print("File Gisted and Available at : %s" %
          gist_url, end='\n', file=sys.stdout)


if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
