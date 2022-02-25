import copy
from collections import defaultdict
import random


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

            for k in range(0, skill_level + 1):
                skill_to_cont[(skill_name, k)].append(cont_name)

        cont_dict[cont_name] = skill_dict

    for i in range(num_proj):
        (
            proj_name,
            num_days_complete,
            score,
            num_days_deadline,
            num_roles,
        ) = file.readline().split()
        num_days_complete, score, num_days_deadline, num_roles = (
            int(num_days_complete),
            int(score),
            int(num_days_deadline),
            int(num_roles),
        )

        skill_dict = {}
        skill_dict[("xxx_num_days_complete", 0)] = num_days_complete
        skill_dict[("xxx_score", 0)] = score
        skill_dict[("xxx_num_days_deadline", 0)] = num_days_deadline
        skill_dict[("xxx_num_roles", 0)] = num_roles

        for j in range(num_roles):
            skill_name, skill_level = file.readline().split()
            skill_level = int(skill_level)

            skill_dict[(skill_name, skill_level)] = skill_level

        proj_dict[proj_name] = skill_dict

    return cont_dict, proj_dict, skill_to_cont


invalid_skill_names = set(
    ["xxx_num_days_complete", "xxx_score", "xxx_num_days_deadline", "xxx_num_roles"]
)


def append_output(output_filename, line1, line2):
    with open(output_filename, "a") as of:
        of.write(line1 + "\n")
        of.write(line2 + "\n")

    # for filename in ["a_an_example.in.txt", "b_better_start_small.in.txt", "c_collaboration.in.txt"]:
    # for filename in ["d_dense_schedule.in.txt", "e_exceptional_skills.in.txt", "f_find_great_mentors.in.txt"]:
    # for filename in ["b_better_start_small.in.txt"]:
    output_filename = filename[:-6] + "out.txt"

    with open(output_filename, "w") as of:
        of.write("0\n")

    base_cont_dict, base_proj_dict, skill_to_cont = read_input(filename)

    # print(base_cont_dict, base_proj_dict, skill_to_cont)
    # print(base_proj_dict)
    # print()

    cont_dict = copy.deepcopy(base_cont_dict)
    remaining_proj_dict = copy.deepcopy(base_proj_dict)

    assigned_conts = {}
    projects_in_progress = {}
    end_date_dict = defaultdict(default_value2)

    day = -1
    while len(remaining_proj_dict.keys()) != 0:
        day += 1

        # update levels
        for ending_proj in end_date_dict[day]:
            for i, cont_name in enumerate(projects_in_progress[ending_proj]):
                skill_name = list(base_proj_dict[ending_proj].keys())[4 + i]
                # print(day, ending_proj, skill_name)
                if (
                    base_proj_dict[ending_proj][skill_name]
                    == cont_dict[cont_name][skill_name]
                ):
                    new_level = cont_dict[cont_name][skill_name] + 1
                    cont_dict[cont_name][skill_name] = new_level
                    skill_to_cont[(skill_name, new_level)].append(cont_name)
                del assigned_conts[cont_name]
            del projects_in_progress[ending_proj]

        remaining_proj_list = list(remaining_proj_dict.keys())
        # print(remaining_proj_list)
        # print()
        random.shuffle(remaining_proj_list)
        for proj_name in remaining_proj_list:
            proj_skill_dict = remaining_proj_dict[proj_name]
            # print("q", proj_name, proj_skill_dict)
            projects_in_progress[proj_name] = []

            possible_project = True
            possible_assigned_conts = {}
            # print(proj_skill_dict.keys())
            for (proj_skill_name, asd) in proj_skill_dict.keys():
                if proj_skill_name in invalid_skill_names:
                    continue

                proj_skill_level = proj_skill_dict[(proj_skill_name, asd)]
                # print(proj_name, proj_skill_name)
                # print("y", set(skill_to_cont[(proj_skill_name, proj_skill_level)]), set(assigned_conts.keys()), set(possible_assigned_conts.keys()))
                possible_conts = list(
                    set(skill_to_cont[(proj_skill_name, proj_skill_level)])
                    - set(assigned_conts.keys())
                    - set(possible_assigned_conts.keys())
                )
                # print("x", proj_name, proj_skill_name, possible_conts, possible_assigned_conts)
                if 0 != len(possible_conts):
                    selected_cont = possible_conts[0]
                    possible_assigned_conts[selected_cont] = cont_dict[selected_cont]
                    # del cont_dict[selected_cont]
                    # skill_to_cont[(proj_skill_name, proj_skill_level)] = possible_conts[1:]
                else:
                    possible_project = False
                    break

            if possible_project:
                # print(proj_name, "possible")
                # print("z", assigned_conts, possible_assigned_conts, projects_in_progress)
                for cont in possible_assigned_conts:
                    assigned_conts[cont] = cont_dict[cont]
                    projects_in_progress[proj_name].append(cont)
                # print("w", assigned_conts, projects_in_progress)
                end_date_dict[
                    day + base_proj_dict[proj_name][("xxx_num_days_complete", 0)]
                ].append(proj_name)
                del remaining_proj_dict[proj_name]

                append_output(
                    output_filename, proj_name, " ".join(possible_assigned_conts)
                )

        # print(day)
        # print()
        # print(remaining_proj_dict)
        # print()
        # print(assigned_conts)
        # print()
        # print(projects_in_progress)

        # if day == 50:
        #     break
    print(filename, day)
