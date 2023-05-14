import random
import string
import loremipsum as lorem
from datetime import date, timedelta

def generate_title():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    random_string = ''.join(random.choice(chars) for _ in range(5))
    return random_string

def generate_description():
    return lorem.paragraph()

def get_weighted_result(tuple_list):
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

### Services ###
# GitHub
token = "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"
user = "beige-sweatshirt";
am_repo = "AM_part";
oem_repo = "OEM_part"

# Jira
token = "ATATT3xFfGF0-FntKXJfWyO3V-lE1bdSIPPZomhHdAIs72IBofpait0KezLbLLo6wl7aJ4uyDE6hutL3AG6smIP_-Het9a_dDglUrzf6mmRXdAHI6YOSS7YO_89wLZHGURov-74-FvahTxx_BKOAIqCCnp_i5QQI7blJh_PRgHht9kg4qpsOY7w=47CF0519"
user = "mholford@protonmail.com"
project_key = "PART"
am_domain = "am-company"
oem_domain = "mholford"

### Data ###
# GitHub
gh_issues = ("bug", 0.75), ("enhancement", 0.25)

# Jira
jira_issues = ("Epic", 0.1), ("Bug", 0.4), ("Story", 0.1), ("Task", 0.4)
reasons = ("Repair", 0.1), ("Upgrade",0.2), ("Maintenance",0.4), ("New Functionality",0.1), ("Other",0.1)
risks = ("Critical", 0.1), ("High", 0.2), ("Medium", 0.4), ("Low", 0.2)
impacts = ("Extensive", 0.1), ("Significant", 0.2), ("Moderate", 0.4), ("Minor", 0.2)
sprint_length = 4 # Normally this would be longer, but since we're limited in time.

