# Releasing

This summarises what 'releasing' means for ybd - it's a work-in-progress. 

### Past

In the first months there were no 'releases' of ybd. The early goals of the
project were to parse definitions as fast as possible, then build them, then
deploy them.

No automated tests were produced because
- the project aimed (and still aims) to have as little code as possible
- upstream wanted to shoe that reliable software can be written without tests
- it was possible to test ybd on actual definitions

### Present

Currently the process is light-weight but ad-hoc:

- ybd has no automated tests, so
- changes are assumed to be tested by their creators
- pull requests are typically merged with little or no upstream review/testing
- breakages are discovered post-merge, typically by
- a full run of ybd on ci.morph x86_64 and/or arm7lhf
- broken changes to ybd are reverted (or sometimes fixed)
- Pep8 is applied post-merge
- releases are tagged periodically, usually after building ci.morph  

There are some weaknesses in this:

- many use-cases are not tested
- breakages happen
- 
- a full build of ci.morph now takes 3 hours on a huge AWS machine
- documentation can get out-of-step

### Future

Ultimately ybd releases should be as automated as possible, to make the
process efficient (minimum work) and reliable (minimum breakage).

The preferred approach for automation is expected to be Concourse.


### Some Test Cases

- build old releases of definitions, as far back as possible
- build with empty, partial and full cache
- verify reproducible components are still the same
- verify installation works, on
  - Vagrant
  - AWS
  - Fedora
  - Debian/Ubuntu