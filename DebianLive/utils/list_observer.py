class ListObserver(list):
    """
    Observed list implementation.

    Calls fn_observed whenever you alter the list.

    >>> my_list = ['spam', 'eggs']
    >>> def fn(): print "Observed."
    >>> my_list = list_observer(my_list, fn)
    >>> my_list.append('bacon')
    Observed.
    >>> my_list.pop()
    Observed.
    bacon
    >>>

    """

    def __init__(self, value, fn_observed):
        list.__init__(self, value)
        self.fn_observed = fn_observed

    def __iter__(self):
        return list.__iter__(self)

    def __setitem__(self,key,value):
        list.__setitem__(self, key, value)
        self.fn_observed()

    def __delitem__(self,key):
        list.__delitem__(self, key)
        self.fn_observed()

    def __setslice__(self, i, j, sequence):
        list.__setslice__(self, i, j, sequence)
        self.fn_observed()

    def __delslice__(self, i, j):
        list.__delslice__(self, i, j)
        self.fn_observed()

    def append(self, value):
        list.append(self, value)
        self.fn_observed()

    def pop(self):
        self.fn_observed()
        return list.pop(self)

    def extend(self, newvalue):
        self.fn_observed()
        list.extend(self, newvalue)

    def insert(self, i, element):
        list.insert(self, i, element)
        self.fn_observed()

    def remove(self, element):
        list.remove(self, element)
        self.fn_observed()

    def reverse(self):
        list.reverse(self)
        self.fn_observed()

    def sort(self, cmpfunc=None):
        list.sort(self, cmpfunc)
        self.fn_observed()
