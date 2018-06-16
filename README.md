## Quick start

1. Install python from their oficial website.
2. Install `pipenv` package from a command line:
    ```
    pip install pipenv
    ```
3. Clone this repo.
4. From a command line, navigate to your repo folder and run:
    ```
    pipenv install --dev
    ```
5. Install current package:
    ```
    pipenv run python setup.py develop
    ```
6. Run it:
    ```
    pipenv run do
    ```

7. Take a look to the option by running:
```
pipenv run do --help
```


## TODO
- [x] Split `cli.py` file in a more logic structure
- [x] Prepare script for release.
- [x] Allow comments in JSON file
- [x] Add CLI arguments:
  - [x] Input file
  - [x] Output file
  - [x] Open output in browser
  - [ ] Watch input file
- [ ] Support `passNode` and `failNodeIndex`
- [ ] Grey out nodes with `"skip": true`