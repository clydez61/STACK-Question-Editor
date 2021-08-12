# STACK Question Editor
The STACK Question Editor, is a Python based Graphic User Interface that aims to simplify the process of making Moodle STACK type questions.


# Features
- Automates user input
- Provides organized visualization of adding input fields
- Allows an interactive approach to edit potential tree
- Shows live preview for latex and STACK specific syntax
- Provides fast response, as it works offline and does not have to deal with servers

# License
Distributed under the MIT License. See [LICENSE](https://github.com/clydez61/STACK-Question-Editor/blob/main/LICENSE) file for more information.

# Installation
The STACK Question Editor installation package is available for download through the [GitHub repository](https://github.com/clydez61/STACK-Question-Editor). 

To contribute or modify the code, clone the repository with git in your desired directory:
```
git clone https://github.com/clydez61/STACK-Question-Editor.git --recursive 
```
# Usage
The STACK Question Editor preserves and simplifies the Moodle STACK input fields. There are six input pages and
the user can switch pages through the left menubar. It is recommended for users to edit them in the order of 'Display' to 'Tree' page to fully utlize the automation feature.

For details of each input field, simply point mouse cursor over the label for 1 second or more for a tooltip.

The user interface uses json type file for file operations within the program. When the look, variables, inputs, and potential response trees have been made, users can export to achieve a Moodle XML file capable of being imported into Moodle. The export function uses Dr. John Bowman's [Stack Tools](https://gitlab.com/stacktools/tools) for serialization.

## Display Page
The display page features a split view, where the left side is a rich text editor, which also support editing in html, once the button is toggled. The right side text previewer renders LaTeX and STACK specific code live. 

## Variables Page
The variable page allows user to define variables with Maxima syntax. Variable values can be called and displayed using @...@ syntax in General Feedback, Input, and Potential Tree.

## Feedback Page
The feedback page will show the solution to students after they have submitted their answer. It is an optional input page with idential layout and function to the display page.

## Attributes Page
The attributes page consists of 3 optional input fields, mostly used to categorize and distiguish the question.

## Inputs Page
The inputs page visually displays the attributes of each user input. The inputs are generated by clicking on "Update Input" in display page.

## Tree Page
The tree page contains a workarea where you can drag nodes to construct how the question will grade the student. The green output indicates what happens if the user answers correctly for that node, and the red output insidate what happens if the user answers incorrectly for that node. For generating the potential response tree, ensure "Display" page is filled out, "Variables" page is filled out, and inputs have been generated. Then click on the top right "Generate" -> "Generate Tree".






