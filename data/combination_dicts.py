# Dictionaries used to combine the age, income, and household income variables
# into smaller buckets for data analysis

age_categories = {
    "0-17": ["1-4", "5-17"],
    "18-24": ["18-19", "20-24"],
    "25-34": ["25-29", "30-34"],
    "35-44": ["35-39", "40-44"],
    "45-54": ["45-49", "50-54"],
    "55-64": ["55-59", "60-64"],
    "65-74": ["65-69", "70-74"],
}


income_categories = {
    "0-15k": ["no_income", "1-10k", "10-15k"],
    "25-50k": ["25-35k", "35-50k"],
    "50-75k": ["50-65k", "65-75k"],
}


household_income_categories = {
    "0-25k": ["less_than_10k", "10-15k", "15-20k", "20-25k"],
    "25-60k": ["25-30k", "30-35k", "35-40k", "40-45k", "45-50k", "50-60k"],
    "60-100k": ["60-75k", "75-100k"],
    "100-150k": ["100-125k", "125-150k"],
}