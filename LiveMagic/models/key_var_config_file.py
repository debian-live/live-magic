import re
import os

class KeyVarConfigFile(object):
    """
    Represents a shell KEY=VAR configuration file.
    """

    # Escape mappings (<unescaped>, <escaped>)
    escapes = (
        (r'\ '[:-1], r'\\ '[:-1]),
        (r'"',  r'\"'),
        (r'`', r'\`'),
        (r'$', r'\$'),
        (r"'", r'\''),
    )

    def __init__(self, filename, spec):
        self.filename = filename
        self.spec = spec

        self.shortname = filename.split(os.sep)[-1]
        self._line_numbers = {}
        self._stale = set()

        self.load()

    @staticmethod
    def is_lh_variable(var):
        """
        Returns True if var is a configuration variable for Debian Live.
        """
        return var.startswith('LH_') or var.startswith('LH_')

    def __setattr__(self, k, v):
        if self.is_lh_variable(k):
            self._stale.add(k)
        self.__dict__[k] = v

    def __iter__(self):
        return filter(self.is_lh_variable, self.__dict__.keys()).__iter__()

    def load(self):
        """
        Loads and parses file.
        """
        # Clear old state
        self._line_numbers.clear()
        self._stale.clear()
        for var in self.__dict__.keys():
            if self.is_lh_variable(var): del self.__dict__[var]

        lineno = 1
        regex = re.compile(r"""^\s*(\w+)=(?:(["\'])(([^\\\2]|\\.)*|)\2|((\w|\\["'])*))\s*(?:#.*)?$""")
        f = open(self.filename, 'r')
        for line in f:

            # Check and parse key=value lines
            match = regex.match(line)
            if match:
                key = match.groups()[0]

                # Find the correct match group
                for m in match.groups()[2:]:
                    if m is not None:
                        val = m
                        break

                # Unescape value
                for to, from_ in self.escapes:
                    val = val.replace(from_, to)

                # Save line number
                self._line_numbers[key] = lineno

                # Mutate to file type
                val_type = self.spec.get(key, 'string')
                typed_val = {
                    'int' : self._parse_int,
                    'list' : self._parse_list,
                    'string' : lambda k, v: v,
                    'boolean' : lambda k, v: {'enabled' : True, 'disabled' : False, 'yes' : True, 'no' : False}.get(v, None),
                }[val_type](key, val)
                self.__dict__[key] = typed_val

            lineno += 1

    def _parse_list(self, k, v):
        if v == '':
            return list_observer([], self._stale.add, k)
        else:
            return list_observer(v.split(' '), self._stale.add, k)

    def _parse_int(self, k, v):
        if v == '':
            return None
        else:
            return int(v)

    def altered(self):
        """Returns True if this configuration file has changed since last save."""
        return len(self._stale) != 0

    def save(self):
        """
        Update all updated entries in the file.
        """
        if len(self._stale) == 0:
            return

        f = open(self.filename, 'r+')
        lines = f.readlines()

        for k in self._stale:
            val = getattr(self, k)

            # Escape value
            if type(val) in (list, list_observer):
                for from_, to in self.escapes:
                    val = map(lambda x: x.replace(from_, to), val)
                val = map(str.strip, val)
            elif type(val) is str:
                for from_, to in self.escapes:
                    val = val.replace(from_, to)

            # Format value depending on its type
            line_value = {
                list : lambda v: " ".join(val),
                bool : lambda v: {True: 'enabled', False: 'disabled'}.get(val, None),
                str : lambda v: v,
                type(None) : lambda v: "",
            }[type(val)](val)

            line = '%s="%s"\n' % (k, line_value)

            try:
                # Overwrite original line in file
                lines[self._line_numbers[k] - 1] = line
            except KeyError:
                # Append line to end of file
                lines.append("\n# The following option was added by live-magic\n")
                lines.append(line)
        f.close()

        f = open(self.filename, 'w')
        f.writelines(lines)
        f.close()

        self._stale.clear()


class list_observer(list):
    def __init__ (self, value, observer, observer_arg):
        list.__init__(self, value)
        self.observer = observer
        self.observer_arg = observer_arg

    def __iter__(self):
        return list.__iter__(self)

    def __setitem__(self,key,value):
        list.__setitem__(self, key, value)
        self.observer(self.observer_arg)

    def __delitem__(self,key):
        list.__delitem__(self, key)
        self.observer(self.observer_arg)

    def __setslice__(self, i, j, sequence):
        list.__setslice__(self, i, j, sequence)
        self.observer(self.observer_arg)

    def __delslice__(self, i, j):
        list.__delslice__(self, i, j)
        self.observer(self.observer_arg)

    def append(self, value):
        list.append(self, value)
        self.observer(self.observer_arg)

    def pop(self):
        self.observer(self.observer_arg)
        return list.pop(self)

    def extend(self, newvalue):
        self.observer(self.observer_arg)
        list.extend(self, newvalue)

    def insert(self, i, element):
        list.insert(self, i, element)
        self.observer(self.observer_arg)

    def remove(self, element):
        list.remove(self, element)
        self.observer(self.observer_arg)

    def reverse(self):
        list.reverse(self)
        self.observer(self.observer_arg)

    def sort(self, cmpfunc=None):
        list.sort(self, cmpfunc)
        self.observer(self.observer_arg)
