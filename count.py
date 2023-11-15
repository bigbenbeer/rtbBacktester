import os

def count_python_lines(directory, excluded_directories):
  """Counts the total number of lines of Python code inside .py files in a directory, excluding directories in the excluded_directories list.

  Args:
    directory: The directory to count the lines of Python code in.
    excluded_directories: A list of directories to exclude from the count.

  Returns:
    The total number of lines of Python code inside .py files in the directory, excluding directories in the excluded_directories list.
  """

  total_lines = 0
  for root, dirs, files in os.walk(directory):
    for file in files:
      if file.endswith(".py") and not any(excluded_directory in root for excluded_directory in excluded_directories):
        with open(os.path.join(root, file), "r") as f:
          total_lines += len(f.readlines())
  return total_lines


if __name__ == "__main__":
  directory = "rtbBacktester"
  excluded_directories = ["rtbBacktester/rtbbacktester/rtb_Indicators/IndicatorPlots"]
  total_lines = count_python_lines(directory, excluded_directories)
  print(f"The total number of lines of Python code in {directory}, excluding directories in {excluded_directories} is {total_lines}.")
