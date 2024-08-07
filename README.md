# Overview

`Wrapper-Bar` is a python module to help wrap commands with the progress bar. `Wrapper-Bar` helps in wrapping shell commands, or even python scripts with a progress bar and ETA.

Following `v0.1.5` onwards, It allows wrapping downloads too. It could be a direct download link or from github releases (both public and private repositoies)

## Badges

![PyPI - Version](https://img.shields.io/pypi/v/wrapper-bar)
![PyPI - Status](https://img.shields.io/pypi/status/wrapper-bar)
![Dependents (via libraries.io)](https://img.shields.io/librariesio/dependents/pypi/wrapper-bar)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wrapper-bar)
![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/wrapper-bar)
![PyPI - License](https://img.shields.io/pypi/l/wrapper-bar)
[![Downloads](https://static.pepy.tech/badge/wrapper-bar)](https://pepy.tech/project/wrapper-bar)


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Uninstall](#uninstall)
- [Yanked Versions](#yanked-versions)

## Installation

To install `wrapper-bar`, use pip.

```bash
pip install wrapper-bar==0.1.5
```

## Usage

- Import the Wrapper class.

  ```python
  >>> from wrapper_bar.wrapper import Wrapper
  ```

- Initialize the Wrapper Class.

  ```python
  >>> wrapControl = Wrapper(*params) # for parameters, check docstring.
  ```

- Docstring

  ```bash
  # to check docstring, in terminal/CMD, run:
  $ pydoc wrapper_bar.wrapper.Wrapper
  ```

- Methods

  - `decoy`

    ```python
    >>> wrapControl.decoy(*params) # parameters are in the docstring.
    # decoy is for creating empty progressbar.
    ```
  
  - `shellWrapper`

    ```python
    >>> wrapControl.shellWrapper(*params) # parameters are in the docstring.
    # shellWrapper can wrap list of shell commands across the progressbar.
    ```

  - `pyWrapper`

    ```python
    >>> wrapControl.pyWrapper(*params) # parameters are in the docstring.
    # pyWrapper can wrap list of python scripts across the progressbar.
    ```
  
  - `pyShellWrapper`
  
    ```python
    >>> wrapControl.pyShellWrapper(*params) # parametes are in the docstring.
    # pyShellWrapper can wrap inline python code across a progressbar.
    ```

    Working of `pyShellWrapper`:

    - `pyShellWrapper` takes two compulsory parameters => `pythoncodes` and `dependencies`. To explain them, let us see below

      ```python
      # pythoncodes and dependencies can have any python code except 
      # return, print or yield statements as they will interfere with
      # the progress bar.

      # let us take this as an example:
      >>> pythoncodes = ["""a = b+c""", """b=c+d"""]

      # Now for the above python codes, values of 'b', 'c' and 'd' 
      # are a dependency. Therefore
      
      >>> dependencies = ["""b=10""", """c=10\nd=20\n"""] 
      
      # try to keep one statement only inside """...""", 
      # but if need be, then you can also put multiple 
      # statements followed by '\n'. Like """c=10\nd=20\n"""

      # and now we will execute them with the loading bar as the 
      # front.

      >>> from wrapper_bar.wrapper import Wrapper
      >>> w = Wrapper("Loading:")
      >>> w.pyShellWrapper(pythoncodes, dependencies) # this will output the following:
      Loading: |▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓|Time: 0:00:10
      
      # To fetch the outputs, we will use a property 'pyShellWrapperResults' 
      # defined under the `Wrapper Class`

      >>> a = w.pyShellWrapperResults['a'] # this will be 20
      >>> b = w.pyShellWrapperResults['b'] # this will be 30
      ```
    
  - `downloadWrapper` **_[[`v0.1.5`](https://pypi.org/project/wrapper-bar/0.1.5/)]_**

    ```python
    >>> wrapControl.downloadWrapper(*params) # parameters are in the docstring.
    # downloadWrapper can wrap downloads from either a direct link or from github release (both public and private)
    ```

    working of `downloadWrapper`:

    - Download files with a direct link using `downloadWrapper`:

      ```python
      # for direct download, following parameters are mandatory
      # - link
      # - download_to
      # - download_filename (optional, if not left empty,
      #   it will be derived from the link, if that fails,
      #   it will raise an Exception.)
      # - type (possible values: ['direct', 'github_release']).
      #   We will choose 'direct' here.

      >>> from wrapper_bar.wrapper import Wrapper
      >>> wrapControl = Wrapper()
      >>> wrapControl.downloadWrapper(link = "https://...",
      ...              download_to = "<download-dir>",
      ...              download_filename = "file.zip",
      ...              type = 'direct')
      
      # the above code will output the following
      file.zip: 100%|███████████████████████████████████████████| 45.1M/45.1M
      ```
    - Download files from a Github Release:
      
      - Public

        ```python
        # for downloading from a public repository release,
        # following params are necessary
        # - link (put your repository link here)
        # - download_to
        # - download_filename (optional, if not left empty,
        #   it will be derived from the link, if that fails,
        #   it will raise an Exception.)
        # - type (possible values: ['direct', 'github_release']).
        #   We will choose 'github_release' here.

        >>> from wrapper_bar.wrapper import Wrapper
        >>> wrapControl = Wrapper()
        >>> wrapControl.downloadWrapper(link = "https://github.com/d33pster/Friday",
        ...              download_to = "<download-dir>",
        ...              download_filename = "bot.zip",
        ...              type = 'github_release')

        # this will output the following output
        bot.zip: 100%|███████████████████████████████████████████| 45.1M/45.1M
        ```

      - Private

        ```python
        # for private repos, params needed:
        # - link (put your repository link here)
        # - download_to
        # - download_filename (optional, if not left empty,
        #   it will be derived from the link, if that fails,
        #   it will raise an Exception.)
        # - type (possible values: ['direct', 'github_release']).
        #   We will choose 'github_release' here.
        # - private_repo (set it to true)
        # - github_api_token (generate one, and put it here).
        # Wrapper Bar doesn't store it or use it for misuse (you can check the code.)
        # - github_release: by default it is set to 'latest', but you can put release tags here as you need, like v1.0, v2.4.3, and so on.

        >>> from wrapper_bar.wrapper import Wrapper
        >>> wrapControl = Wrapper()
        >>> wrapControl.downloadWrapper(link = "https://github.com/d33pster/Fridat",
        ...              download_to = "<download-dir>",
        ...              download_filename = "bot.zip",
        ...              type = 'github_release'
        ...              private_repo = True, github_api_token = "__your_token__")

        # this will output the following:
        bot.zip: 100%|███████████████████████████████████████████| 45.1M/45.1M
        ```

## Uninstall

To uninstall `wrapper-bar`, use pip.

```bash
pip uninstall wrapper-bar
```

## Yanked Versions

- **_v0.1.2_**
