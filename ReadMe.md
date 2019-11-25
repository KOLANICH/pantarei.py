[πανταρει](https://en.wikipedia.org/wiki/Heraclitus#Panta_rhei,_%22everything_flows%22).py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===========
[wheel (GHA via `nightly.link`)](https://nightly.link/KOLANICH-libs/pantarei.py/workflows/CI/master/urm-0.CI-py3-none-any.whl)
![GitLab Build Status](https://gitlab.com/KOLANICH/pantarei.py/badges/master/pipeline.svg)
[![TravisCI Build Status](https://travis-ci.org/KOLANICH-libs/pantarei.py.svg?branch=master)](https://travis-ci.org/KOLANICH/pantarei.py)
![GitLab Coverage](https://gitlab.com/KOLANICH/pantarei.py/badges/master/coverage.svg)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/pantarei.py.svg)](https://coveralls.io/r/KOLANICH/pantarei.py)
[![GitHub Actions](https://github.com/KOLANICH-libs/pantarei.py/workflows/CI/badge.svg)](https://github.com/KOLANICH-libs/pantarei.py/actions)
[![N∅ hard dependencies](https://shields.io/badge/-N∅_Ъ_deps!-0F0)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH-libs/pantarei.py.svg)](https://libraries.io/github/KOLANICH/pantarei.py)

Just an abstraction layer around various progress reporters.

When making a lib/tool doing long operations we have several options:

1. Not to show progress at all. Pro: no code for that. Con: No progress.
2. Take a dependency on a specific lib to show fancy progress. Pro: Fancy progress. Con: A dependency on a specific lib. A user can say "I can't install that lib on my PC, I prefer another one. Don't force me to install that shit".
3. Inline an existing lib. The same drawbacks like in 2., but also code bloat and a try to cheat the user.
4. Create an own small and simple progress visualizer and inline it. Pro: some progress report. Con: code bloat and the report is not fancy.
5. Create a **small** and **simple** abstraction layer on different popular reporters (that it is likely that at least one of them is already present on user's machine) and use it. **This library does this.** Pro: fancy progress reports, not enforcing a single dependency. Con: dependency on the abstraction layer itself.
