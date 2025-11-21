# Load necessary libraries
library(readxl)   # For reading .xlsx files
library(dplyr)    # For data manipulation (e.g., pipe operator %>%, mutate)
library(stringr)  # For string operations (e.g., str_replace, str_extract)
library(ggplot2)  # Although not used for plotting in the Python script's final output,
# it's good practice to include if plotting might be needed.

# --- Data Loading and Initial Cleaning ---

# Read the Excel file. Assumes the file 'Light_microscopy_volumes.xlsx' is in the working directory.
df <- read_excel('Light_microscopy_volumes.xlsx')


# --- Calculation and String Manipulation ---

# Calculate 'root_volume'. Note: R's ** operator is for exponents.
# The formula is (root_area / (conversion_rate_px_per_mm ^ 2)) * length * 10
df <- df %>%
  mutate(
    root_volume = (root_area / (conversion_rate_px_per_mm ^ 2)) * length * 10
  )

# Equivalent to df['sample_id'].str.replace('_[a-z]*_[0-9]X.JPG$', '', regex=True)
# This removes the suffix like '_a_10X.JPG' or '_b_4X.JPG' from sample_id
df <- df %>%
  mutate(
    sample_id = str_replace(sample_id, '_[a-z]*_[0-9]X\\.JPG$', '')
  )

# Print the resulting data frame (equivalent to print(df) in Python)
print(df)

# --- Grouping and Summing Volumes ---

# The Python script's loop calculates a cumulative volume for *each* sample ID
# but resets the sum *only* if the second number extracted from the sample_id
# changes. This logic appears flawed for calculating *total* volume per unique sample_id.
# The most likely intended logic is to calculate the total root volume for each unique sample_id.

# R's 'group_by' and 'summarise' is the idiomatic way to achieve the intended final result:
# total volume per unique sample_id.

volumes_df <- df %>%
  group_by(sample_id) %>%
  summarise(
    total_volume_light_microscopy = sum(root_volume, na.rm = TRUE)
  ) %>%
  ungroup() # Ungroup the data frame

# Equivalent to printing the final volumes dictionary from Python
# The R data frame shows the same key-value pairs
print(volumes_df)

# --- Exporting the Final Data ---

# Write the final data frame to a new Excel file
# You might need to install 'writexl' package if not already installed: install.packages('writexl')
# Using 'writexl' is generally preferred over 'openxlsx' or others for simple Excel writing.

# Check if writexl is installed, if not, use base R's write.csv as a robust alternative.
# If 'writexl' is available:
# library(writexl)
# write_xlsx(volumes_df, 'final_volumes.xlsx')

# Using base R function to write to CSV, which is very common and reliable:
# write.csv(volumes_df, 'final_volumes.csv', row.names = FALSE)

# Or, if you specifically need an Excel file and have a suitable package:
# Using the 'openxlsx' package (assuming it's installed):



#library(openxlsx)
#write.xlsx(volumes_df, 'final_volumes.xlsx', rowNames = FALSE)
