# Version history

## 0.2.1

### Features:

* New "improvements" added:
  * **B007: Convert f-strings without expressions into regular strings.**

### Misc:

* Fix some typing violations.

  

## 0.2.0

### Bugfixes:

* Now metadata resolution is done properly for all transformers.
* Matcher decorators were used in a wrong way and caused a lot of false positives.
* Now contents of the generated `__all__` attribute are lexicographically sorted.
* Some transformers made changes on the `original_node` attribute, which could have led to subtle bugs.

### Features:

* New "improvements" added:
  * **B005: Replace "A == None" with "A is None"**
  * **B006: Remove comparisons with either 'False' or 'True'.**
  
* Now you can output diff between original and modified code using `--diff` option.

  

## 0.1.0

- Initial release.