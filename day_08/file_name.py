import os
import re

# Define the directory
#
dir_path = r'Z:\APSdata_201904\projection'

# Define the regex pattern
pattern = '_(.*?_.*?_.*?_.*?_.*?)(?:_|$)'

# Iterate over the files in the directory
for filename in os.listdir(dir_path):
    # Search for the pattern in the filename
    match = re.search(pattern, filename)
    if match:
        # Print the matched part
        print(match.group(1))

for filename in os.listdir(dir_path):
    # Split the filename on underscore
    parts = filename.split('_')
    # Print the part before the first underscore
    print(parts[0])