import argparse
import getpass

import requests


def organisation_repos(url=None):
    if url is None:
        url = 'https://api.github.com/orgs/%s/repos?per_page=%s' % (ORG, 100)

    repos = requests.get(
        url,
        auth=AUTH,
    )
    repositories = set([repo['name'] for repo in repos.json()])

    next_url = repos.links.get('next', {}).get('url')
    if next_url:
        repositories.update(organisation_repos(url=next_url))

    return repositories


parser = argparse.ArgumentParser(
    description="Finds all the deletable branches of yours in your organisation"
                "'s github repositories."
)

parser.add_argument('username', help='Your github username.')
parser.add_argument('org', help='Your github organisation.')
args = parser.parse_args()

USER = args.username
ORG = args.org
PASS = getpass.getpass('Enter your github password:\n')
AUTH = (USER, PASS)

print('Starting...')

NAME = requests.get('https://api.github.com/users/%s' % USER)

print('Connected...')

branch_counter = 0
org_branch_url = ('https://api.github.com/repos/%s/%s/branches' %
                  (ORG, '%s'))

org_repos = organisation_repos()
print('Checking repositories...')
total_repos = len(org_repos)
repo_count = 0

for repo in org_repos:
    repo_count += 1
    print('%d/%d - %s' % (repo_count, total_repos, repo))
    branches_url = org_branch_url % repo
    repo_branches = requests.get(branches_url, auth=AUTH).json()

    for repo_branch in repo_branches:
        repo_name = repo_branch['name']
        if repo_name not in ['master', 'release']:
            branch_url = branches_url + '/' + repo_name
            branch_info = requests.get(branch_url, auth=AUTH).json()

            if branch_info['commit']['author']:
                branch_owner = branch_info['commit']['author']['login']

                if branch_owner == USER:
                    print '\t\tDELETE: %s' % repo_name
                    branch_counter += 1
            else:
                committer_name = \
                    branch_info['commit']['commit']['author']['name']
                print '\t%s' % repo_name
                print (('\t\t + Author null\n'
                        '\t\t | Committer name: %s\n'
                        '\t\t - Possibly yours: %s') %
                       (committer_name, committer_name == NAME))

print('\nFound %d branches to investigate.' % branch_counter)
