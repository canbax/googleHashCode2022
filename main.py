from typing import List, Tuple
from helper import Project, Contributor, Skill


def read_input(filename) -> Tuple[List[Contributor], List[Project]]:

    projects: List[Project] = []
    contributors: List[Contributor] = []
    file = open(filename, "r")

    num_cont, num_proj = (int(x) for x in file.readline().split())

    for _ in range(num_cont):
        cont_name, num_skills = file.readline().split()
        num_skills = int(num_skills)

        cont_skills: List[Skill] = []
        for _ in range(num_skills):
            skill_name, skill_level = file.readline().split()
            skill_level = int(skill_level)
            cont_skills.append(Skill(skill_name, skill_level))
        contributors.append(Contributor(cont_name, cont_skills))

    for _ in range(num_proj):
        (
            name,
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

        project_skills: List[Skill] = []
        for _ in range(num_roles):
            skill_name, skill_level = file.readline().split()
            skill_level = int(skill_level)
            project_skills.append(Skill(skill_name, skill_level))

        projects.append(
            Project(name, num_days_complete, score, num_days_deadline, project_skills)
        )

    return contributors, projects


def algo_random(filename):
    contributors, projects = read_input(filename)

    for p in projects:
        for r in p.roles:
            r.name
    return projects


print(algo_random("inp/a_an_example.in.txt"))
