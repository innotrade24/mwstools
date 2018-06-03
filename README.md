# mwstools


## flatten.py

That should be able to parse and flatten every json like response from mws.

The finance api is probably one of the hardest. There are lists somewhere in the middle, which consists of sometimes multiple nested dicts.
There we get too many columns, because the nesting we get is not consistend.

We can solve this, tough need to be careful to not mess up the namespace.

The vast majority of the data comes in dictionaries thats good.
For lists you have two options, you can enumarate them or you can make new rows.
For each item you want to make a row.
But for 6 Bulletpoints, which are part of a much larger attribute set, you want to enumarate them.
We use the fact that those values of e.g. Bulletpointlist are most likely strings.
Somewhere else we can maybe punch even more together.

## Usage
input a dictionary, also it makes sense to give it only partial data.
```python
m = Magic(fp_r.parsed.FinancialEvents.ShipmentEventList)
# so we have rowdata or listdata just look at both
# listdata you can easily use in a dataframe, like so
pd.DataFrame(m.dictdata)
```
