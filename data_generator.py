import random
import string
from datetime import date, timedelta
from github import Github
import requests
import json
from jira import JIRA
from jira.resources import Issue
import os


def generate_title():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    random_string = ''.join(random.choice(chars) for _ in range(5))
    return random_string

def generate_description():
    with open("lorem.txt", 'r') as file:
        text = file.read()
        sentences = text.split(". ")
        num_sentences = random.randint(1, 3)
        return ". ".join(random.sample(sentences, num_sentences))

def weighted_str(tuple_list):
    dict_list = dict(tuple_list)
    total_prob = sum(dict_list.values())
    rand_num = random.uniform(0, total_prob)

    # Iterate through the items in the dictionary and return the associated string if the random number falls within the probability range
    prob_sum = 0
    for string, prob in dict_list.items():
        prob_sum += prob
        if rand_num <= prob_sum:
            return string

def generate_story_pts(longest_spring):
    return random.integer(1,longest_spring+1)

def generate_duedate(story_pts):
    today = date.today()
    delta = timedelta(days=story_pts)
    new_date = today + delta
    return new_date.strftime("%Y-%m-%d")

def open_github_issue(token, user, repo):
    title = generate_title()
    descr = generate_description()
    gh_issue_types = ("bug", 0.75), ("enhancement", 0.25)
    type = weighted_str(gh_issue_types)

    g = Github(token)
    repo = g.get_user(user).get_repo(repo)
    issue = repo.create_issue(title=title, body=descr, labels=[type])
    print(f"Created issue: {issue.html_url}")

def close_github_issue(token, user, repo):
    g = Github(token)
    repo = g.get_user(user).get_repo(repo)
    issues = repo.get_issues(state="open")
    if issues.totalCount == 0:
        print("No open issues to close")
        return
    random_issue = random.choice(list(issues))
    random_issue.edit(state="closed")
    print(f"Closed issue #{random_issue.number}: {random_issue.title}")

def github_test(token: str, owner: str, repo: str, workflow_id: int):
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}",
    }

    data = {
        "ref": "main",  # or the name of the branch you want to use
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        response.raise_for_status()
        print("Workflow dispatched successfully.")
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")

def jira_create_issue(token, user, key, domain):
    jira_issues = ("Epic", 0.1), ("Bug", 0.4), ("Story", 0.1), ("Task", 0.4)
    risks = ("Critical", 0.1), ("High", 0.2), ("Medium", 0.4), ("Low", 0.2)
    impacts = ("Extensive / Widespread", 0.1), ("Significant / Large", 0.2), ("Moderate / Limited", 0.4), ("Minor / Localized", 0.2)
    sprint_length = 4 # Normally this would be longer, but since we're limited in time.

    jira_connection = JIRA(
    basic_auth=(user, token),
    server=f"https://{domain}.atlassian.net"
    )

    story_pts = generate_story_pts(4)

    issue_dict = {
        'project': {'key': key},
        'summary': generate_title(),
        'description': generate_description(),
        'customfield_10006': {'value': weighted_str(risks)},   # Risks
        'customfield_10004': {'value': weighted_str(impacts)}, # Impacts
        'issuetype': {'name': weighted_str(jira_issues)},
        'customfield_10016': story_pts,                        # Story Point Estimate
        'duedate': generate_duedate(story_pts)
    }

    new_issue = jira_connection.create_issue(fields=issue_dict)
    print(f"New issue created: {new_issue.key}")

def jira_move_issue(token, user, key, domain):
    jira = JIRA(
    basic_auth=(user, token),
    server=f"https://{domain}.atlassian.net"
    )

    # Get all issues for the project, shuffle and iterate until one with transitions is found
    issues = jira.search_issues(f'project={key}', maxResults=False)
    if not issues:
        print(f"No issues found for project {key}.")
        return
    
    random.shuffle(issues)
    for issue in issues:
        # Get the possible transitions for the issue
        transitions = jira.transitions(issue)
        if transitions:
            # Pick 1st available transition and do it
            transition = transitions[0] 
            jira.transition_issue(issue, transition['id'])
            print(f"Issue {issue.key} has been moved to the next status.")
            return

    print(f"No transitions available for any issue in project {key}.")

### Services ###
# GitHub
gh_token = os.getenv('GH_TOKEN')
gh_user = "beige-sweatshirt"
gh_am_repo = "AM_part"
gh_oem_repo = "OEM_part"
gh_testID_AM = 57184472
gh_testID_OEM = 56996570

# Jira
jira_token = os.getenv('JIRA_TOKEN')
jira_user = "mholford@protonmail.com"
jira_project_key = "PART"
jira_am_domain = "am-company"
jira_oem_domain = "mholford"

# # NOTE: This script fires once every four hours. 
if random.random() <= 0.33:
    open_github_issue(gh_token, gh_user, gh_am_repo)
if random.random() <= 0.33:
   open_github_issue(gh_token, gh_user, gh_oem_repo)
if random.random() <= 0.33:
    jira_create_issue(jira_token, jira_user, jira_project_key, jira_am_domain)
if random.random() <= 0.33:
   jira_create_issue(jira_token, jira_user, jira_project_key, jira_oem_domain)

# Moving existing issues
if random.random() <= 0.33:
    close_github_issue(gh_token, gh_user, gh_am_repo)
if random.random() <= 0.33:
   close_github_issue(gh_token, gh_user, gh_oem_repo)
if random.random() <= 0.33:
    jira_move_issue(jira_token, jira_user, jira_project_key, jira_am_domain)
if random.random() <= 0.33:
    jira_move_issue(jira_token, jira_user, jira_project_key, jira_oem_domain)

# Testing
if random.random() <= 0.20:
   github_test(gh_token, gh_user, gh_oem_repo, gh_testID_OEM)
if random.random() <= 0.20:
   github_test(gh_token, gh_user, gh_am_repo, gh_testID_AM)
