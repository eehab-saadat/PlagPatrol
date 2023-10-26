import os

# Get the current working directory
current_directory = os.getcwd()

# Loop through all files in the current directory
for filename in os.listdir(current_directory):
    if filename.endswith('.txt'):
        # Form the full path of the file
        file_path = os.path.join(current_directory, filename)

        # Read the content of the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Modify the content by removing the first three characters from each non-empty line
        modified_lines = []
        for line in lines:
            if line.strip():  # Check if the line is non-empty
                modified_line = line[2:]
                modified_lines.append(modified_line)
            else:
                modified_lines.append(line)  # Preserve empty lines

        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.writelines(modified_lines)
