import collections
import pandas as pd

class Magic():
    def __init__(self, d):
        self.rowdata = None
        self.rowdata = []
        self.dictdata = self.flatten(d)

    def flatten(self, d, parent_key='', sep='.', force_toplevel=False):
        '''
        The vast majority of the data comes in dictionaries thats good.
        For lists you have two options, you can enumarate them or you can make new rows.
        For each item you want to make a row.
        But for 6 Bulletpoints, which are part of a much larger attribute set, you want to enumarate them.
        We use the fact that those values of e.g. Bulletpointlist are most likely strings.
        Somewhere else we can maybe punch even more together.
        
        Usage: input a dictionary, also it makes sense to give it only partial data.
        m = Magic(fp_r.parsed.FinancialEvents.ShipmentEventList)
        so we have rowdata or listdata just look at both
        listdata you can easily use in a dataframe, like so
        pd.DataFrame(m.listdata)
        '''
        items = []

        # works only for toplevel dict like objects
        assert d.items()

        # cdata, we unpack the unit into the parent key with underscores
        if len(d.keys()) == 2 and d.get('#text') and d.get('@Units'):
            units = d.get('@Units')
            cdata_key = f'{parent_key}_in_{units}'
            cdata_value = d.get('#text')
            items.append((cdata_key, cdata_value))
        else:
            for k, v in d.items():
                new_key = parent_key + sep + k if parent_key else k
                if isinstance(v, collections.MutableSequence):
                    i = 0
                    for j in v:
                        i += 1
                        num_key = f'{new_key}_{i}'
                        # this is resolving a list by numerating
                        if isinstance(j, str):
                            items.append((num_key, j))
                        # this is resolving a list by making new rows
                        elif isinstance(j, dict):
                            if not force_toplevel:
                                items.extend(self.flatten(j, new_key, sep=sep, force_toplevel=True).items())
                                self.rowdata.append(dict(items))
                            else:
                                # print('#'*20+str(j))
                                return dict(self.flatten(j, new_key, sep=sep, force_toplevel=True).items())
                            # print('ψ'*20+str(items))
                            # print(force_toplevel)
                            # print('_'*20)
                            items = []
                        else:
                            assert False
                elif isinstance(v, collections.MutableMapping):
                    if force_toplevel:
                        # items.append((new_key, v))
                        # print('ξ'*20+str(v))
                        items.extend(self.flatten(v, new_key, sep=sep, force_toplevel=True).items())
                        # that's another multiple times nested dictionary we want to resvolve into a single row

                    else:
                        items.extend(self.flatten(v, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))

        return dict(items)
