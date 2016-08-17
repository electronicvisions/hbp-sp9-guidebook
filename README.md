# HBP Neuromorphic Computing Platform Guidebook

This repository contains the Sphinx sources for the HBP Neuromorphic Computing Platform Guidebook.

For instruction on how to clone the guidebook, see [GitHub documentation](https://help.github.com/articles/cloning-a-repository/).

The contents of this repository are under review, we use GitHub pull requests.
To create a pull request, first create a [fork](https://help.github.com/articles/fork-a-repo/) of this repository, clone it, edit files, create a git commit and push to your fork.
Afterwards you can create a [pull request](https://help.github.com/articles/creating-a-pull-request/).

To build the guidebook, first install Sphinx:

    pip install sphinx

then run:

    make html       # home page generated in _build/html/index.html

or

    make latexpdf   # generates _build/latex/HBPNeuromorphicComputingPlatformGuidebook_vX.Y.pdf
