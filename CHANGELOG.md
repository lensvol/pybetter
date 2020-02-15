# Version history



## 0.3.3 WIP

### Bugfixes:

* Fix issue with `noqa` directive with one argument being treated as `noqa` without any arguments.

### Misc:

* Use `pygments` for highlighting of diffs.
* Output time taken to apply selected transformations.
* Output total time taken to process all files in provided paths.

### Features:

* New "improvements" added:
  * **B008: Replace nested 'with' statements with a compound one.**
  * **B009: Replace unhashable list literals in set constructors**

## 0.3.2

### Bugfixes:

* (B002) Fix issue when new inits were added before docstrings.
* (B002) Remove unneeded indent after generated initializations.

### Misc:

* Nothing is displayed if no changes were made to the file.



## 0.3.1

### Bugfixes:

* (B003) No longer remove parentheses from multi-line return statements.

* (B004) `a == False` is now correctly reduced to `not a`.

  

## 0.3.0

### Features:

* Now we will recurse over every path provided and process all `*.py` files found.
* Added support for `--select`/`--ignore` options for fine-tuning set of checks being run.
* Added support for per-line disabling of specific checks using `noqa` comments.

### Bugfixes:

* Variable names and constants are now properly added to `__all__` attribute.

* Small fixes in README.

  

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