from typing import List


class Skill:
    def __init__(self, name: str, level: int) -> None:
        self.name = name
        self.level = level

    def __str__(self) -> str:
        return self.name + " " + str(self.level)

    def __repr__(self) -> str:
        return self.name + " " + str(self.level)


class Contributor:
    def __init__(self, name: str, skills: List[Skill]) -> None:
        self.name = name
        self.skills = skills

    def __str__(self) -> str:
        return self.name + " " + str(self.skills)

    def __repr__(self) -> str:
        return self.name + " " + str(self.skills)


class Project:
    def __init__(
        self,
        name: str,
        n_complete: int,
        score: int,
        best_before: int,
        roles: List[Skill],
    ) -> None:
        self.name = name
        self.n_complete = n_complete
        self.score = score
        self.best_before = best_before
        self.roles = roles

    def __str__(self) -> str:
        return self.name + " " + str(self.roles)

    def __repr__(self) -> str:
        return self.name + " " + str(self.roles)

    def has_enough_contributors(self, people: List[Contributor]):
        skill_pool = {}  # name > level > count
        for r in people:
            for r in r.skills:
                if not r.name in skill_pool:
                    skill_pool[r.name] = {}
                if not skill_pool[r.name][r.level]:
                    skill_pool[r.name][r.level] = 0
                skill_pool[r.name][r.level] = skill_pool[r.name][r.level] + 1

        project_needs = {}  # name > level > count
        for r in self.roles:
            if not r.name in project_needs:
                project_needs[r.name] = {}
            if not project_needs[r.name][r.level]:
                project_needs[r.name][r.level] = 0
            project_needs[r.name][r.level] = project_needs[r.name][r.level] + 1

        # for skill_name in project_needs:
        #     if skill_name not in skill_pool:
        #         return False
        #     for level in project_needs[skill_name]:
        #       if level in skill_pool[skill_name]:

