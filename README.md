# Mockinator
-This is under development and not yet reached a maturity level. Please use at your own risk.-
A Mock Generation Helper.

# About 
This is a simple Mock Generator tool for generating mocked classes for Google Test Framework.
To do so, the starting point for this is to generate an Abstract Syntax Tree (AST). The starting point for reaching the AST is the python cppclean component (https://github.com/myint/cppclean). 

This component uses a slightly modified version of the cppclean's AST parser. The folder `mycpp` includes a stripped down version of the cppclean. I intentionally changed the folder name to avoid compatibility issues with any cppclean pip installed version.

It has a PyQt Based GUI to ease the mocking process, supporting file opening, saving and drag and drop files.

# Current limitations
This is not yet thoroughly tested, specially for templated classes.
