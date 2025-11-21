# Load necessary libraries
# You will need to install these packages if you haven't already:
# install.packages(c("readxl", "tidyverse"))

library(readxl)   # For reading .xlsx files
library(dplyr)    # For data manipulation (the core of the simplification)
library(tidyr)    # For reshaping data (part of tidyverse)
library(ggplot2)  # For plotting

# --- SET WORKING DIRECTORY ---
# IMPORTANT: This line sets the working directory to your specified path.
setwd("C:/Users/shahz/Downloads/root volume scripts")

# Define constant: section thickness (delta_x)
SECTION_THICKNESS_MM <- 20


# --- 1. Data Loading and Core Volume Calculation ---

# Load the data and calculate all total volumes in a single, simple pipeline.
tryCatch({
  
  volume_totals_df <- read_excel(
    path = 'PRFB_2B_anatomy.xlsx',
    sheet = 'B73 Total per section',
    col_types = "guess"
  ) %>%
    # 1. Select the relevant columns: sample_id, conversion rate, and the area columns
    select(sample_id, conversion_rate_mm_per_px, root_area, stele_area, pith_area) %>%
    
    # 2. Reshape the data from wide (3 area columns) to long (1 area column)
    # This prepares the data for a single volume calculation step.
    pivot_longer(
      cols = ends_with("_area"), # Selects root_area, stele_area, pith_area
      names_to = "volume_type",
      values_to = "area_px"
    ) %>%
    
    # 3. Calculate the volume for each section/row
    mutate(
      # Coerce area_px to numeric (similar to Python's pd.to_numeric(errors='coerce'))
      area_px = as.numeric(area_px), 
      # Calculate Area in mm^2: area_px * (conversion_rate)^2
      area_mm2 = area_px * (conversion_rate_mm_per_px ^ 2),
      # Calculate Volume (mm^3): Area_mm2 * SECTION_THICKNESS_MM
      Total_Volume = area_mm2 * SECTION_THICKNESS_MM
    ) %>%
    
    # 4. Aggregate the total volume by sample and volume type
    group_by(sample_id, volume_type) %>%
    summarize(
      # Sum the volume. na.rm = TRUE safely ignores NA values, matching the original logic.
      Total_Volume = sum(Total_Volume, na.rm = TRUE),
      .groups = 'drop' 
    )
  
}, error = function(e) {
  # This block handles file errors
  stop(paste("Error loading data. Make sure 'PRFB_2B_anatomy.xlsx' is in your specified directory.\nOriginal error:", e$message))
})


# --- 2. Separate Data for Plotting (Easier to manage plot titles) ---

# We filter the aggregated dataframe to create the three required datasets for the graphs.
root_volumes <- volume_totals_df %>% filter(volume_type == "root_area")
stele_volumes <- volume_totals_df %>% filter(volume_type == "stele_area")
pith_volumes <- volume_totals_df %>% filter(volume_type == "pith_area")

# Display the aggregated data
print("--- Aggregated Root Volumes (mm^3) ---")
print(volume_totals_df)


# --- 3. Plotting Function ---

# The plotting function remains the same as it was already clear and effective.

create_bar_plot <- function(data, title) {
  p <- ggplot(data, aes(x = sample_id, y = Total_Volume)) +
    # Create the bar chart
    geom_col(fill = "#1F77B4", color = "darkblue") + 
    # Add text labels on top of the bars
    geom_text(
      aes(label = round(Total_Volume, 2)), 
      vjust = -0.5, 
      angle = 90,   
      size = 3.5    
    ) +
    # Add titles and labels
    labs(
      title = title,
      x = "Sample ID",
      y = expression(paste("Total Volume (", mm^3, ")")) 
    ) +
    # Theme adjustments for readability
    theme(
      axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5),
      plot.title = element_text(hjust = 0.5, face = "bold"),
      panel.background = element_rect(fill = "white", colour = NA),
      panel.grid.major.y = element_line(colour = "grey90"),
      panel.grid.minor.y = element_blank(),
      panel.grid.major.x = element_blank()
    ) +
    scale_y_continuous(expand = expansion(mult = c(0, 0.1)))
  
  return(p)
}


# --- 4. Generate Plots ---

# Create and print the three separate plots
plot_root <- create_bar_plot(root_volumes, "Total Root Volume per Sample")
print(plot_root)

plot_stele <- create_bar_plot(stele_volumes, "Total Stele Volume per Sample")
print(plot_stele)

plot_pith <- create_bar_plot(pith_volumes, "Total Pith Volume per Sample")
print(plot_pith)