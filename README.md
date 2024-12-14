# Python to EXE Converter

## Introduction
The Python to EXE Converter is a user-friendly application that allows you to convert Python scripts into standalone executable files. This tool is particularly useful for developers who want to distribute their Python applications without requiring users to have Python installed on their systems. The converter supports both Windows and macOS operating systems and includes features for setting an expiry time for the executable.

## Features
- **Cross-Platform Support**: Convert Python scripts to executables for both Windows and macOS.
- **Expiry Time**: Set an expiry time for the executable, after which it will no longer run.
- **Progress Tracking**: Visual progress bar to track the conversion process.
- **User-Friendly GUI**: Simple and intuitive graphical user interface for easy navigation.
- **Custom Icon Support**: Option to set custom icons for the generated executables.
- **Error Handling**: Built-in error handling to manage issues during the conversion process.

## Installation
To install and run the Python to EXE Converter, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SafeerAbbas624/python_to_exe.git
   cd python-to-exe-converter
   ```

2. **Install Required Packages**:
   Make sure you have Python installed on your system. Then, install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   Launch the application by running:
   ```bash
   python python_to_exe.py
   ```
4. **Error OR exe not running**
   After conversion you will find the exe file with same name of script in folder of script. If that conversion is not running try adding your script libraries in code with below variable.
   ```bash
   # Add specific imports that might be missed
        additional_imports = [
            'selenium',
            'seleniumbase',
            'selenium.webdriver',
            'selenium.webdriver.common',
            'selenium.webdriver.common.by',
            'selenium.webdriver.common.keys',
            'selenium.webdriver.support',
            'selenium.webdriver.support.ui',
            'selenium.webdriver.support.expected_conditions',
            'selenium.webdriver.support.wait',
            'openpyxl.styles',
            'openpyxl',
            'tkinter',
            'math',
            'csv',
            'docx',

        ]
   ```
   add your libraries here and there will be no error!!!

## Picture
![Python to EXE Converter Screenshot](https://github.com/SafeerAbbas624/python_to_exe/blob/main/python_to_exe.JPG)

## Contribution
Contributions are welcome! If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

---

Feel free to customize the content, especially the repository link and the path to the screenshot, to fit your project specifics.
