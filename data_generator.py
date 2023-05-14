import random
import string
from datetime import date, timedelta
from github import Github

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
    return random.uniform(1,longest_spring+1)

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

### Services ###
# GitHub
gh_token = "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"
gh_user = "beige-sweatshirt"
gh_am_repo = "AM_part"
gh_oem_repo = "OEM_part"

# Jira
jira_token = "ATATT3xFfGF0-FntKXJfWyO3V-lE1bdSIPPZomhHdAIs72IBofpait0KezLbLLo6wl7aJ4uyDE6hutL3AG6smIP_-Het9a_dDglUrzf6mmRXdAHI6YOSS7YO_89wLZHGURov-74-FvahTxx_BKOAIqCCnp_i5QQI7blJh_PRgHht9kg4qpsOY7w=47CF0519"
jira_user = "mholford@protonmail.com"
jira_project_key = "PART"
jira_am_domain = "am-company"
jira_oem_domain = "mholford"

### Data ###

# Jira
jira_issues = ("Epic", 0.1), ("Bug", 0.4), ("Story", 0.1), ("Task", 0.4)
reasons = ("Repair", 0.1), ("Upgrade",0.2), ("Maintenance",0.4), ("New Functionality",0.1), ("Other",0.1)
risks = ("Critical", 0.1), ("High", 0.2), ("Medium", 0.4), ("Low", 0.2)
impacts = ("Extensive", 0.1), ("Significant", 0.2), ("Moderate", 0.4), ("Minor", 0.2)
sprint_length = 4 # Normally this would be longer, but since we're limited in time.

#print(lorem.get_sentences(2))
close_github_issue(gh_token, gh_user, gh_oem_repo)
close_github_issue(gh_token, gh_user, gh_am_repo)