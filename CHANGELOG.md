# Version history


## 0.4.1

### Misc
* Updated dependencies.
* Now we use [LibCST](https://github.com/Instagram/LibCST) 0.4.1, which means that you should be able to run `pybetter` on all the Python 3 versions up to **3.11**!
* Please be kind to each other and hug your loved ones.

## 0.4.0

### Features:

* (B010) Added  new fixer for `not A is B => A is not B` situation. (kudos to @rs2)

### Bugfixes:

* (B003) Prevent removal of parentheses around empty tuple (kudos to @rs2) 
* (B008) Invalid translation with async context manager block (kudos to @lummax)

## 0.3.7

### Bugfixes:

* (B004) Fix `typing.overload` annotations causing appearance of duplicate identifiers in `__all__` attribute (thanks, [Bernát Gábor](https://github.com/gaborbernat)!).

### Misc

* Added [support](https://github.com/lensvol/pybetter/blob/master/.pre-commit-hooks.yaml) for `pre-commit` hooks (thanks, [Pavel Kedrinskiy](https://github.com/pavelpy)!).
* Updated version of LibCST used from **0.3.16** to **0.3.19**. 

## 0.3.6.1

### Misc

* Fix another edge case with transforming "raw" f-strings (thanks, Zac Hatfield-Dodds!)


## 0.3.6

### Misc

* Fix triple quotes being mangled by 'trivial f-string' transform (thanks, Zac Hatfield-Dodds!)
* Updated dependencies.


## 0.3.5

### Misc:

* Add `--exit-code` option to facilitate use as a static analysis tool.



## 0.3.4

### Bugfixes:

* (B001) Fix issue with trying to convert multiple consecutive comparisons.
* (B002) Properly process nested functions.
* (B002) Ensure that order of arguments is preserved during iteration.
* (B003) Fix unnecessary elimination of parens inside returned expression.

### Misc:

* `--diff` option behaviour has changed:
  * Output is now being printed on `sys.stderr` instead if `sys.stdout`.
  * Source lines are no longer highlighted if `sys.stderr` is redirected away from TTY.



## 0.3.3

### Bugfixes:

* Fix issue with `noqa` directive with one argument being treated as `noqa` without any arguments.
* (B001) Fix arrangement of parentheses on transformed comparisons. 

### Misc:

* Use `pygments` for highlighting of diffs.
* Output time taken to apply selected transformations.
* Output total time taken to process all files in provided paths.
* Now we use Travis CI to run tests on each commit.

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
