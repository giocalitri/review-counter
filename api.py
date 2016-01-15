"""
APIs for review count
"""

import collections
from github import Github


def review_count(sentinel, repos, token, since):
    """
    Loop through merged prs in the available repos to find comments which
    contain sentinel values. Credit those users with reviewing it.

    Args:
        sentinel (string): the text to be searched in the comment
        repos (list): a list of repositories
        token (string): the access token for github
        since (string): a text representation of the date since when the count
            should be done

    Returns:
        list: a list of tuples containing couples of author names and
            number of reviewed pull requests
    """
    github = Github(token)
    to_check = set()
    for repo_str in repos:
        repo = github.get_repo(repo_str)
        for pr in repo.get_pulls(state='closed'):
            if pr.merged_at and pr.merged_at >= since:
                to_check.add(pr)

    total_reviews = []
    for pr in to_check:
        for comment in pr.get_issue_comments():
            if sentinel in comment.body:
                total_reviews.append(comment.user.name)

    counter = collections.Counter(total_reviews)
    return counter.most_common()
