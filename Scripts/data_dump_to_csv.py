import csv
import json
import pandas as pd
import re

def parse_data(data_str):
    # Replace unnecessary characters and split by commas
    cleaned_data_str = data_str.replace('{', '').replace('}', '').replace('"', '').replace("'", "").split(',')
    # Construct a dictionary from key-value pairs
    data_dict = {}
    for pair in cleaned_data_str:
        if ':' in pair:
            key, value = pair.split(':', 1)
            # Remove extra spaces from key and value
            key = key.strip()
            value = value.strip()
            data_dict[key] = value
    return data_dict

def extract_numeric_part(text):
    numeric_part = ''.join(filter(str.isdigit, text))
    return numeric_part if numeric_part else "--"  # Return "--" if no numeric part found

def extract_decimal(string):
    match = re.search(r'\d+\.\d+', string)  # Match any sequence of digits followed by a dot and more digits
    if match:
        return match.group()  # Return the matched decimal part
    else:
        return "--"  # Return "--" if no decimal part found


# Read the file and process each line
trials_data = []
meta_data = []
merged_data = []
comments_data = []
pcid_data = []
with open('study_data_dump.csv', 'r') as file:
    for line in file:
        # Split the line into its three components
        components = line.strip().split(';')
        if len(components) == 3:
            data_id, data_str, timestamp = components
            # Parse the JSON-like string
            data = parse_data(data_str)
            time_stamp = parse_data(timestamp)
            # Check if the condition is satisfied
            my_pcid = data.get("my_pcid", "")
            uuid = data.get("uuid","")
            gender = data.get("gender","")
            education = data.get("education","")
            expertise = data.get("expertise","")
            age_category = data.get("age_category","")
            
            if my_pcid and uuid and gender: 
                meta_data.append([my_pcid, uuid, gender, education, expertise, age_category])
                pcid_data.append([my_pcid, uuid])

            if data.get("data_type") == "study:comments":
                clarity_rating = data.get("clarity","")
                difficulty_rating = data.get("difficulty","")
                comments_general = data.get("comments", "")
                if clarity_rating and difficulty_rating: 
                    comments_data.append([uuid,clarity_rating, difficulty_rating, comments_general ])

            if data.get("data_type") == "study:data":
                uuid = data.get("uuid","")
                trial_idx = data.get("trial_idx", "")
                resp_time = data.get("rt", "")
                is_practice = data.get("is_practice","")
                is_debug = str(data.get("is_debug", ""))
                sanity_check_failed = data.get("sanity_check_failed","")
                question = data.get("question", "")
                ans = data.get("ans","")
                response = data.get("response","")
                category = data.get("category", "")
                img = data.get("img","")
                img_parts = img.split('/')
                sanity_check_failed = data.get("sanity_check_failed", "")
                point_density = "--"
                no_of_outliers = "--"
                outlier_distance = "--"
                no_of_clusters = "--"
                cluster_distance = "--"
                distribution_type = "--"
                r_value = "--"
                correlation_trend = "--"
 
                if category == "cat1_gist_outliers":
                    point_density = extract_numeric_part(img_parts[-4]) 
                    no_of_outliers = extract_numeric_part(img_parts[-3])  
                    outlier_distance = extract_numeric_part(img_parts[-2])
                elif category == "cat2_gist_clusters":
                    point_density = extract_numeric_part(img_parts[-4]) 
                    no_of_clusters = extract_numeric_part(img_parts[-3])  
                    cluster_distance = extract_numeric_part(img_parts[-2])
                elif category == "cat3_gist_distributions":
                    point_density = extract_numeric_part(img_parts[-3])  
                    distribution_type = img_parts[-2]

                elif category == "cat4_gist_correlation":
                    point_density = extract_numeric_part(img_parts[-4]) 
                    r_value = extract_decimal(img_parts[-3])
                    correlation_trend = img_parts[-2]
                elif category == "cat5_gist_clusters_outliers" and is_practice.lower() == 'false':
                    point_density = extract_numeric_part(img_parts[-5]) 
                    no_of_outliers = extract_numeric_part(img_parts[-3])  
                    outlier_distance = extract_numeric_part(img_parts[-2])
                    no_of_clusters = extract_numeric_part(img_parts[-4])  
                    cluster_distance = '3'

                elif category == "filler" and "title" in question:
                    category = "filler_title"
                elif category == "filler" and "legend" in question:
                    category = "filler_legend"
                elif category == "filler" and "scatterplot" in question:
                    category = "filler_plot_idea"
                elif category == "filler" and "highest" in question:
                    category = "filler_details"
                elif category == "filler" and "range" in question:
                    category = "filler_range"
                elif category == "filler" and "marker" in question:
                    category = "filler_marker"

                else:
                    point_density = "--"
                    no_of_outliers = "--"
                    outlier_distance = "--"
                    no_of_clusters = "--"
                    cluster_distance = "--"
                    distribution_type = "--"
                    r_value = "--"
                    correlation_trend = "--"

                exposuretime = data.get("timeout","")
                # Append the extracted information to csv_data list
                if trial_idx and trial_idx != '0' and is_debug.lower() == 'false' and is_practice.lower() == 'false' and category != 'sanity' and sanity_check_failed.lower() == 'false':
                    trials_data.append([uuid, exposuretime, trial_idx, category, img, point_density, no_of_outliers, outlier_distance, no_of_clusters, cluster_distance, distribution_type, r_value, correlation_trend, question, ans, response, resp_time])

# Convert lists to pandas DataFrames
meta_df = pd.DataFrame(meta_data, columns=["pid", "uuid", "gender", "education", "expertise", "age_category"])
trials_df = pd.DataFrame(trials_data, columns=["uuid", "exposure_time", "trial_id", "category", "image", "point_density", "no_of_outliers", "outlier_distance",  "no_of_clusters", "cluster_distance", "distribution_type", "r_value", "correlation_trend", "question", "correct_ans", "user_response", "response_time"])
pcid_df = pd.DataFrame(pcid_data, columns = ["pid", "uuid"])
comments_df = pd.DataFrame(comments_data, columns = ["uuid", "clarity_rating", "difficulty_rating", "comments"])

# Merge DataFrames on 'uuid' column
merged_data = pd.merge(pcid_df, trials_df, on='uuid', how='left')
merged_data_comments = pd.merge(pcid_df, comments_df, on='uuid', how='left')

# Write the extracted information to a CSV file
merged_data.to_csv('study_trials_data_11Apr2024.csv', index=False)
meta_df.to_csv('study_meta_data_11Apr2024.csv',index = False)
merged_data_comments.to_csv('study_comments_data_11Apr2024.csv', index= False)
