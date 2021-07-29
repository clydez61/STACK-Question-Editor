# STACK Question Editor
A user-friendly GUI for writing Moodle STACK type Questions

The STACK Question Editor, is a Python based Graphic User Interface that aims to simplify the process of making stack questions.

The STACK Question Editor works in complement with Dr. John Bowman’s program of stack tools, available gitlab: https://gitlab.com/stacktools/tools

# Features
- Automates user input
- Provides organized visualization of adding input fields
- Allows an interactive approach to edit potential tree
- Shows live preview for latex and STACK specific syntax
- Provides fast response, as it works offline and does not have to deal with servers

# Installation
The STACK Question Editor installation package is available for download through the GitHub repository


# Usage
The STACK Question Editor preserves and simplifies the Moodle STACK input fields. There are six input pages and
the user can switch pages through the left menubar. It is recommended for users to edit them in the order of 'Display' to 'Tree' page to fully utlize the automation feature.

For details of each input field, simply point mouse cursor over the label for 1 second or more for a tooltip.
## Display Page
The display page features a split view, where the left side is a rich text editor, which also support editing in html, once the button is toggled. The right side text previewer renders LaTeX and STACK specific code live. 

## Variables Page
The variable page allows user to define variables with Maxima syntax. Variable values can be called and displayed using {@...@} syntax in General Feedback, Input, and Potential Tree.

## Feedback Page
The feedback page will show the solution to students after they have submitted their answer. It is an optional input page with idential layout and function to the display page.

## Attributes Page
The Attributes page consists of 3 optional input fields.

## Tree Page


# License
Distributed under the MIT License. See LICENSE for more information.




