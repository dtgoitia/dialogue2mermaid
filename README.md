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

## Other bits and pieces
* For the time being, the JSON dialogue should be in `test.jsonc`, which should live in the root of the repo.
* For the time being, the output Markdown file with the Mermaid diagram will be saved to `output.md`.
* For the time being, use the extension "Markdown Preview Enhanced" (within Visual Studio Code) to render `output.md` and see the diagram.

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