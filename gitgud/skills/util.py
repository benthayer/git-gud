class NamedList:
    # names is a list populated with type str, items is a list populated with any type 
    def __init__(self, names, items):
        assert len(names) == len(items)
        self._name_dict = {name: index for index, name in enumerate(names)}
        self._items = items
    
    def __getitem__(self, query):
        if isinstance(query, str):
            if query.isnumeric():
                if 0 < int(query) <= len(self):
                    return self._items[int(query) - 1]
                else:
                    raise KeyError
            return self._items[self._name_dict[query]]
        else:
            raise KeyError

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

    def values(self):
        return self._items
    
    def keys(self):
        set_indices = { str(i) for i in range(1, len(self) + 1) }
        set_names = set(self._name_dict.keys())
        return set_indices | set_names
        


class AllSkills(NamedList):
    def __init__(self, skills):
        super().__init__([skill.name for skill in skills], skills)
        last_level = None
        for skill in self:
            for level in skill:
                if last_level is not None:
                    last_level.next_level = level
                level.prev_level = last_level
                last_level = level



class Skill(NamedList):
    def __init__(self, name, levels):
        super().__init__([level.name for level in levels], levels)
        self.name = name

        for level in levels:
            level.skill = self
