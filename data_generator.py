import random
import string
import lorem

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

# Issue Fields and their probabilities
reasons = ("Repair", 0.1), ("Upgrade",0.2), ("Maintenance",0.4), ("New Functionality",0.1), ("Other",0.1)
risks = ("Critical", 0.1), ("High", 0.2), ("Medium", 0.4), ("Low" 0.2)
impacts = ("Extensive", 0.1), ("Significant", 0.2), ("Moderate", 0.4), ("Minor", 0.2)