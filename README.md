# Oskui command line toolbox

## Overview

This toolbox provides a collection of utilities designed to facilitate various command line interface tasks. It includes functions for user input, file selection, and terminal output formatting.

## Features

- **User Input**: Functions to prompt users for specific types of input (e.g., floats, integers, confirmation).
- **File Selection**: Graphical dialogs to select files or directories.
- **Menu Selection**: Utilities to create and navigate through choice menus.
- **Terminal Output**: Color-coded output and utility functions for terminal display.
- **Image Interaction**: Functions to interact with images, such as clicking on points within an image.

## Installation

To use this toolbox, clone the repository or download the source code to your local machine. Ensure you have Python 3 installed, as well as the required packages listed in `requirements.txt`.

```bash
pip install oskui
pip install -r requirements.txt
```

## Usage
Import the toolbox in your Python script to access its functionalities.

```python
from oskui import ask_float_int, ask_file, ask_folder, choice_menu
```

Use the provided functions as needed within your command line application.

## Documentation
Each function in the toolbox comes with a docstring explaining its purpose, parameters, and return value. Refer to these docstrings for detailed usage information.

## Contributing
Contributions to the toolbox are welcome. Please fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.