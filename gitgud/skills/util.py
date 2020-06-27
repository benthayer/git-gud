class NamedList:
    def __init__(self, names, items, start_index=1):
        assert len(names) == len(items)
        self._items = items
        self._name_dict = {}
        self._index_dict = {}
        for index, name in enumerate(names):
            mapped_index = str(index + start_index)
            self._name_dict.update({name: index})  # key to list
            self._name_dict.update({mapped_index: index})  # index to list
            self._index_dict.update({name: mapped_index})

    def __getitem__(self, query):
        return self._items[self._name_dict[query]]

    def __iter__(self):
        return self._items.__iter__()

    def __len__(self):
        return len(self._items)

    def __setitem__(self, key, item):
        if isinstance(key, str):
            self._name_dict[key] = len(self._items)
            self._items.append(item)
        else:
            raise TypeError

    def __contains__(self, item):
        return item in self._items

    def index(self, name):
        return self._index_dict[name]

    def values(self):
        return self._items

    def keys(self):
        return self._name_dict.keys()


class AllSkills(NamedList):
    def __init__(self, skills):
        super().__init__(
                [skill.name for skill in skills],
                skills,
                start_index=0)
        last_level = None
        for skill in self:
            skill.all_skills = self
            for level in skill:
                if last_level is not None:
                    last_level.next_level = level
                level.prev_level = last_level
                last_level = level


class Skill(NamedList):
    def __init__(self, readable_name, name, levels):
        super().__init__([level.name for level in levels], levels)
        self.name = name
        self.readable_name = readable_name

        for level in levels:
            level.skill = self
