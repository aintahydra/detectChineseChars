#!/bin/python3
###############################################################################
# A script searching for the files that includes Chinese characters
#
# -----------------------------------------------------------------------------
#  
# The MIT License
#
# Copyright (c) 2023 aintahydra (aintahydra@gmail.com)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###############################################################################
# 
# References
# - https://medium.com/the-artificial-impostor/detecting-chinese-characters-in-unicode-strings-4ac839ba313a
# - https://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
import os
import re
import sys

# to determine whether a given file is binary or text(printable)

printablechars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
is_binary_string = lambda bytes: bool(bytes.translate(None, printablechars))

def cjk_detect(texts):
    # korean
    if re.search("[\uac00-\ud7a3]", texts):
        return "ko"
    # japanese
    if re.search("[\u3040-\u30ff]", texts):
        return "ja"
    # chinese
    if re.search("[\u4e00-\u9FFF]", texts):
        return "zh"
    return None

# print each line where Chinese characters are found
def find_chinese_characters_eachline(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        line_num = 1
        for line in file:
            if re.search(r'[\u4e00-\u9fff]', line):
                print(f'File: {file_path}, Line: {line_num}\n\t{line.strip()}')
            line_num += 1

# print the file name includes Chinese characters, and print the first line where Chinese characters are found if the file is not a binary
def find_chinese_characters_firsthit(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        line_num = 1
        for line in file:
            if re.search(r'[\u4e00-\u9fff]', line):
                if is_binary_string(open(file_path, 'rb').read(1024)):
                    print(f'File: {file_path}, Line: {line_num}. This is a binary file')
                else:
                    print(f'File: {file_path}, Line: {line_num}\n\t{line.strip()}')
                return line_num
            line_num += 1
    return 0

def traverse_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                #find_chinese_characters_eachline(file_path)
                find_chinese_characters_firsthit(file_path)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 '{sys.argv[0]}' <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a valid directory.")
        sys.exit(1)

    # Perform the directory traversal
    traverse_directory(directory_path)