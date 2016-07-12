# Reloadable containers in Python
This repo shows a recipe for reloadable containers in Python. We often face an issue that our long running services need some parts to be reloadable without restart of such service. To achieve this I implemented simple abstract class that wraps any container we could use. Simply implement two methods `_initialize_data` and `_fill_data` and you will have your container reloaded every few second as you can specify. This code run under Python 3. 

```python
>>> from reloadable_containers import ReloadableList
>>> l = ReloadableList("content_list.txt", reload_every_secs=5)
>>> print(len(l))
7
```

Then you can add something to file:
```
$ echo "bit.ly" > content_list.txt
```

And your running application will now respond differently:
```python
>>> print(len(l))
8
>>> print(l[-1])
bit.ly
```

Similarly with json:
```python
>>> from reloadable_containers import ReloadableList
>>> j = ReloadableJson("content.json")
>>> print(j.get("lastName", "MISSING"))
Smith
```