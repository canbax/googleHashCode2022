import copy
from collections import defaultdict

from numpy import sort

def default_value():
    return 0

def default_value2():
    return []

def read_input(filename):
    cont_dict = {}
    proj_dict = {}
    skill_to_cont = defaultdict(default_value2)

    file = open(filename, "r")

    num_cont, num_proj = (int(x) for x in file.readline().split())

    for i in range(num_cont):
        cont_name, num_skills = file.readline().split()
        num_skills = int(num_skills)

        skill_dict = defaultdict(default_value)

        for j in range(num_skills):
            skill_name, skill_level = file.readline().split()
            skill_level = int(skill_level)

            skill_dict[skill_name] = skill_level

            skill_to_cont[(skill_name, skill_level)].append(cont_name)
        
        cont_dict[cont_name] = skill_dict


    for i in range(num_proj):
        proj_name, num_days_complete, score, num_days_deadline, num_roles = file.readline().split()
        num_days_complete, score, num_days_deadline, num_roles = int(num_days_complete), int(score), int(num_days_deadline), int(num_roles)

        skill_dict = {}
        skill_dict["xxx_num_days_complete"] = num_days_complete
        skill_dict["xxx_score"] = score
        skill_dict["xxx_num_days_deadline"] = num_days_deadline
        skill_dict["xxx_num_roles"] = num_roles

        for j in range(num_roles):
            skill_name, skill_level = file.readline().split()
            skill_level = int(skill_level)

            skill_dict[skill_name] = skill_level

        proj_dict[proj_name] = skill_dict

    return cont_dict, proj_dict, skill_to_cont

invalid_skill_names = set(["xxx_num_days_complete", "xxx_score", "xxx_num_days_deadline", "xxx_num_roles"])

for filename in ["a_an_example.in.txt"]:
    base_cont_dict, proj_dict, skill_to_cont = read_input(filename)
    print(base_cont_dict, proj_dict, skill_to_cont)
    cont_dict = copy.deepcopy(base_cont_dict)
    assigned_conts = {}
    projects_in_progress = {}

    possible_project_names = set(x for x in proj_dict.keys())
    for proj_name, skill_dict in proj_dict.items():
        for skill_name in skill_dict.keys() - invalid_skill_names:
            skill_level = skill_dict[skill_name]
            cont_exists = False
            for cont_name, cont_skill_dict in cont_dict.items():
                if cont_skill_dict[skill_name] >= skill_level:
                    cont_exists = True
                    break

            if not cont_exists:
                possible_project_names.remove(proj_name)

    # en kisa suren
    possible_project_names = sorted(possible_project_names, key= lambda name: proj_dict[name]["xxx_num_days_complete"])

    for proj_name in possible_project_names:
        proj_skill_dict = proj_dict[proj_name]
        projects_in_progress[proj_name] = []

        for proj_skill_name in proj_skill_dict.keys() - invalid_skill_names:
            proj_skill_level = proj_skill_dict[proj_skill_name]
            possible_conts = skill_to_cont[(proj_skill_name, proj_skill_level)]
            print(possible_conts)
            if [] != possible_conts:
                selected_cont = possible_conts[0]
                assigned_conts[selected_cont] = cont_dict[selected_cont]
                del cont_dict[selected_cont]
                skill_to_cont[(proj_skill_name, proj_skill_level)] = possible_conts[1:]

                projects_in_progress[proj_name].append(selected_cont)
            else:
                print("Hata {} {} {} {}".format(filename, proj_name, proj_skill_name, proj_skill_level))
