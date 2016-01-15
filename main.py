"""
Main module for the script
"""

import argparse
from datetime import datetime  # pylint: disable=no-name-in-module

from api import review_count


def valid_date(s):
    """
    Convert argparse date into datetime.

    via http://stackoverflow.com/a/25470943/4972
    """
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{}'".format(s)
        raise argparse.ArgumentTypeError(msg)


def get_arguments():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description="Count reviews on github")
    parser.add_argument(
        '--sentinel',
        dest='sentinel',
        default=':+1:',
        help='String to look for to count something as "reviewed"'
    )
    parser.add_argument(
        '--repo',
        dest='repo',
        action='append',
        help="Repos to search through"
    )
    parser.add_argument(
        '--token',
        dest='token',
        help="Your github personal access token"
    )
    parser.add_argument(
        '--since',
        dest='since',
        type=valid_date,
        help="YYYY-MM-DD format of when to outer bound the request"
    )
    arguments = parser.parse_args()
    if not arguments.repo:
        raise RuntimeError("You must specify one or more repos with --repo")
    if not arguments.since:
        raise RuntimeError("You must specify a valid time to start the check")
    return arguments


if __name__ == '__main__':

    args = get_arguments()
    most_common = review_count(
        args.sentinel, args.repo, args.token, args.since)
    print '\n'.join(
        ['%s: %s' % (author, num_pr) for author, num_pr in most_common]
    )
