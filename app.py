import streamlit as st
import pandas as pd
from data_preprocessing import data_preprocessing
from predictions import prediction
import joblib

# Title of the web application
st.title("Prediction App for Enrollment Status")

# Description
st.write("""
This application predicts the enrollment status based on the provided input data.
Fill in the form below and get the prediction!
""")

data = {}

col1, col2, col3= st.columns(3)

with col1:
    marital_status_options = [
        "Single", "Married", "Widower", "Divorced",
        "Facto Union", "Legally Separated"
    ]
    marital_status_mapping = {
        "Single": 1,
        "Married": 2,
        "Widower": 3,
        "Divorced": 4,
        "Facto Union": 5,
        "Legally Separated": 6
    }
    marital_status = st.selectbox(
        "Marital Status", marital_status_options, index=0  # Default is "Single"
    )
    numerical_marital_status = marital_status_mapping[marital_status]
    data["Marital_status"] = numerical_marital_status 


with col2:
    application_mode_options = [
        "1 - 1st phase - general contingent",
        "2 - Ordinance No. 612/93",
        "5 - 1st phase - special contingent (Azores Island)",
        "7 - Holders of other higher courses",
        "10 - Ordinance No. 854-B/99",
        "15 - International student (bachelor)",
        "16 - 1st phase - special contingent (Madeira Island)",
        "17 - 2nd phase - general contingent",
        "18 - 3rd phase - general contingent",
        "26 - Ordinance No. 533-A/99, item b2) (Different Plan)",
        "27 - Ordinance No. 533-A/99, item b3 (Other Institution)",
        "39 - Over 23 years old",
        "42 - Transfer",
        "43 - Change of course",
        "44 - Technological specialization diploma holders",
        "51 - Change of institution/course",
        "53 - Short cycle diploma holders",
        "57 - Change of institution/course (International)"
    ]

    application_mode_mapping = {
        "1 - 1st phase - general contingent" : 1,
        "2 - Ordinance No. 612/93" :2,
        "5 - 1st phase - special contingent (Azores Island)": 5,
        "7 - Holders of other higher courses" : 7,
        "10 - Ordinance No. 854-B/99" : 10,
        "15 - International student (bachelor)" : 15,
        "16 - 1st phase - special contingent (Madeira Island)": 16,
        "17 - 2nd phase - general contingent" :17,
        "18 - 3rd phase - general contingent" :18,
        "26 - Ordinance No. 533-A/99, item b2) (Different Plan)": 26,
        "27 - Ordinance No. 533-A/99, item b3 (Other Institution)":27,
        "39 - Over 23 years old": 39,
        "42 - Transfer": 42,
        "43 - Change of course":43 ,
        "44 - Technological specialization diploma holders" : 44,
        "51 - Change of institution/course": 51,
        "53 - Short cycle diploma holders": 53,
        "57 - Change of institution/course (International)" :57
    }

    
    application_mode = st.selectbox(
        "Application Mode", application_mode_options, index=0 
    )

    num_app_mode = application_mode_mapping[application_mode]

    data["Application_mode"] = num_app_mode

with col3:
    application_order = int(st.number_input(
        label='Application Order', value=17  # Default value is 17
    ))
    data["Application_order"] = application_order

col1, col2, col3= st.columns(3)

with col1:
    course_options = [
        "33 - Biofuel Production Technologies",
        "171 - Animation and Multimedia Design",
        "8014 - Social Service (evening attendance)",
        "9003 - Agronomy",
        "9070 - Communication Design",
        "9085 - Veterinary Nursing",
        "9119 - Informatics Engineering",
        "9130 - Equinculture",
        "9147 - Management",
        "9238 - Social Service",
        "9254 - Tourism",
        "9500 - Nursing",
        "9556 - Oral Hygiene",
        "9670 - Advertising and Marketing Management",
        "9773 - Journalism and Communication",
        "9853 - Basic Education",
        "9991 - Management (evening attendance)"
    ]

    course_map = {
        "33 - Biofuel Production Technologies" : 33,
        "171 - Animation and Multimedia Design": 171,
        "8014 - Social Service (evening attendance)": 8014,
        "9003 - Agronomy": 9003,
        "9070 - Communication Design" : 9070,
        "9085 - Veterinary Nursing" : 9085,
        "9119 - Informatics Engineering": 9119 ,
        "9130 - Equinculture" : 9130,
        "9147 - Management" :9147,
        "9238 - Social Service" : 9238,
        "9254 - Tourism" :9254,
        "9500 - Nursing" :9500,
        "9556 - Oral Hygiene" : 9556,
        "9670 - Advertising and Marketing Management" :9670,
        "9773 - Journalism and Communication" : 9773,
        "9853 - Basic Education" : 9853,
        "9991 - Management (evening attendance)" :9991
    }

    Course = st.selectbox(
        "Course",
        course_options,  index=0
    )
    course_number = course_map[Course]

    data["Course"] = course_number


with col2:
    day_or_evening_options = [
        "Evening",
        "Daytime"
    ]

    day_or_evening_mapping = {
        "Evening" : 0,
        "Daytime": 1
    }

    # Create the selectbox
    daytimeEvening = st.selectbox(
        "Daytime or Evening Attendance",
        day_or_evening_options, index=0
    )

    # Map the selected marital status to its numerical value
    numerical_day_or_evening = day_or_evening_mapping[daytimeEvening]

    # Store the numerical value in the data dictionary
    data["Daytime_evening_attendance"] = [numerical_day_or_evening]

with col3:
    qualification_option = [
        "Secondary education",
        "Higher education - bachelor's degree",
        "Higher education - degree",
        "Higher education - master's",
        "Higher education - doctorate",
        "Frequency of higher education",
        "12th year of schooling - not completed",
        "11th year of schooling - not completed",
        "Other - 11th year of schooling",
        "10th year of schooling",
        "10th year of schooling - not completed",
        "Basic education 3rd cycle (9th/10th/11th year) or equiv",
        "Basic education 2nd cycle (6th/7th/8th year) or equiv",
        "Technological specialization course",
        "Higher education - degree (1st cycle)",
        "Professional higher technical course",
        "Higher education - master (2nd cycle)"
    ]

    qualification_mapping = {
        "Secondary education" : 1,
        "Higher education - bachelor's degree" : 2,
        "Higher education - degree": 3,
        "Higher education - master's": 4,
        "Higher education - doctorate": 5,
        "Frequency of higher education": 6,
        "12th year of schooling - not completed": 9,
        "11th year of schooling - not completed": 10,
        "Other - 11th year of schooling" : 12,
        "10th year of schooling": 14,
        "10th year of schooling - not completed": 15,
        "Basic education 3rd cycle (9th/10th/11th year) or equiv": 19,
        "Basic education 2nd cycle (6th/7th/8th year) or equiv": 38,
        "Technological specialization course" : 39,
        "Higher education - degree (1st cycle)": 40,
        "Professional higher technical course" : 42,
        "Higher education - master (2nd cycle)": 43
    }

    qualification = st.selectbox(
        "Previous Qualification",
        qualification_option,  index=0
    )

    numerical_qualification = qualification_mapping[qualification]

    # Store the numerical value in the data dictionary
    data["Previous_qualification"] = [numerical_qualification]


col1, col2, col3= st.columns(3)

with col1:
    Previous_qualification_grade = int(st.number_input(
        label='Previous Qualification Grade',
        min_value=0,
        max_value=200,
        value=17
    ))
    data["Previous_qualification_grade"] = Previous_qualification_grade

with col2:
    nacionality_option = [
        "Portuguese",
        "German",
        "Spanish",
        "Italian",
        "Dutch",
        "English",
        "Lithuanian",
        "Angolan",
        "Cape Verdean",
        "Guinean",
        "Mozambican",
        "Santomean",
        "Turkish",
        "Brazilian",
        "Romanian",
        "Moldova (Republic of)",
        "Mexican",
        "Ukranian",
        "Russian",
        "Cuban",
        "Colombian"
    ]
    nacionality_mapping = {
        "Portuguese" : 1,
        "German" : 2,
        "Spanish": 6,
        "Italian": 11,
        "Dutch": 13,
        "English": 14,
        "Lithuanian": 17,
        "Angolan": 21,
        "Cape Verdean": 22,
        "Guinean": 24,
        "Mozambican": 25,
        "Santomean": 26,
        "Turkish": 32,
        "Brazilian": 41,
        "Romanian": 62,
        "Moldova (Republic of)" : 100,
        "Mexican": 101,
        "Ukranian": 103,
        "Russian": 105,
        "Cuban": 108,
        "Colombian" : 109
    }

    nacionality = st.selectbox(
        "Nationality",
        nacionality_option,  index=0
    )

    numerical_nacionality = nacionality_mapping[nacionality]

    # Store the numerical value in the data dictionary
    data["Nacionality"] = [numerical_nacionality]


with col3:
    # Define the options for Mother's Qualification
    mom_qualification_option = [
        "Secondary Education - 12th Year of Schooling or Eq.",
        "Higher Education - Bachelor's Degree",
        "Higher Education - Degree",
        "Higher Education - Master's",
        "Higher Education - Doctorate",
        "Frequency of Higher Education",
        "12th Year of Schooling - Not Completed",
        "11th Year of Schooling - Not Completed",
        "7th Year (Old)",
        "Other - 11th Year of Schooling",
        "10th Year of Schooling",
        "General commerce course",
        "Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.",
        "Technical-professional course",
        "7th year of schooling",
        "2nd cycle of the general high school course",
        "9th Year of Schooling - Not Completed",
        "8th year of schooling",
        "Unknown",
        "Can't read or write",
        "Can read without having a 4th year of schooling",
        "Basic education 1st cycle (4th/5th year) or equiv.",
        "Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.",
        "Technological specialization course",
        "Higher education - degree (1st cycle)",
        "Specialized higher studies course",
        "Professional higher technical course",
        "Higher Education - Master (2nd cycle)",
        "Higher Education - Doctorate (3rd cycle)"
    ]
    
    # Mapping of qualification options to numerical values
    mom_qualification_mapping = {
        "Secondary Education - 12th Year of Schooling or Eq.": 1,
        "Higher Education - Bachelor's Degree": 2,
        "Higher Education - Degree": 3,
        "Higher Education - Master's": 4,
        "Higher Education - Doctorate": 5,
        "Frequency of Higher Education": 6,
        "12th Year of Schooling - Not Completed": 7,
        "11th Year of Schooling - Not Completed": 8,
        "7th Year (Old)": 9,
        "Other - 11th Year of Schooling": 10,
        "10th Year of Schooling": 11,
        "General commerce course": 12,
        "Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.": 13,
        "Technical-professional course": 14,
        "7th year of schooling": 15,
        "2nd cycle of the general high school course": 16,
        "9th Year of Schooling - Not Completed": 17,
        "8th year of schooling": 18,
        "Unknown": 19,
        "Can't read or write": 20,
        "Can read without having a 4th year of schooling": 21,
        "Basic education 1st cycle (4th/5th year) or equiv.": 22,
        "Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.": 23,
        "Technological specialization course": 24,
        "Higher education - degree (1st cycle)": 25,
        "Specialized higher studies course": 26,
        "Professional higher technical course": 27,
        "Higher Education - Master (2nd cycle)": 28,
        "Higher Education - Doctorate (3rd cycle)": 29
    }

    # Let the user choose the Mother's Qualification
    mom_qualification = st.selectbox(
        "Mother's Qualification",
        mom_qualification_option,  index=0
    )

    # Map the selected qualification to its numerical value
    numerical_qualification_mom = mom_qualification_mapping[mom_qualification]

    # Store the numerical value in the data dictionary
    data["Mothers_qualification"] = [numerical_qualification_mom]

col1, col2, col3= st.columns(3)

with col1:
    # Define the options for Mother's Qualification
    dad_qualification_option = [
        "Secondary Education - 12th Year of Schooling or Eq.",
        "Higher Education - Bachelor's Degree",
        "Higher Education - Degree",
        "Higher Education - Master's",
        "Higher Education - Doctorate",
        "Frequency of Higher Education",
        "12th Year of Schooling - Not Completed",
        "11th Year of Schooling - Not Completed",
        "7th Year (Old)",
        "Other - 11th Year of Schooling",
        "10th Year of Schooling",
        "General commerce course",
        "Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.",
        "Technical-professional course",
        "7th year of schooling",
        "2nd cycle of the general high school course",
        "9th Year of Schooling - Not Completed",
        "8th year of schooling",
        "Unknown",
        "Can't read or write",
        "Can read without having a 4th year of schooling",
        "Basic education 1st cycle (4th/5th year) or equiv.",
        "Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.",
        "Technological specialization course",
        "Higher education - degree (1st cycle)",
        "Specialized higher studies course",
        "Professional higher technical course",
        "Higher Education - Master (2nd cycle)",
        "Higher Education - Doctorate (3rd cycle)"
    ]
    
    # Mapping of qualification options to numerical values
    dad_qualification_mapping = {
        "Secondary Education - 12th Year of Schooling or Eq.": 1,
        "Higher Education - Bachelor's Degree": 2,
        "Higher Education - Degree": 3,
        "Higher Education - Master's": 4,
        "Higher Education - Doctorate": 5,
        "Frequency of Higher Education": 6,
        "12th Year of Schooling - Not Completed": 7,
        "11th Year of Schooling - Not Completed": 8,
        "7th Year (Old)": 9,
        "Other - 11th Year of Schooling": 10,
        "10th Year of Schooling": 11,
        "General commerce course": 12,
        "Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.": 13,
        "Technical-professional course": 14,
        "7th year of schooling": 15,
        "2nd cycle of the general high school course": 16,
        "9th Year of Schooling - Not Completed": 17,
        "8th year of schooling": 18,
        "Unknown": 19,
        "Can't read or write": 20,
        "Can read without having a 4th year of schooling": 21,
        "Basic education 1st cycle (4th/5th year) or equiv.": 22,
        "Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.": 23,
        "Technological specialization course": 24,
        "Higher education - degree (1st cycle)": 25,
        "Specialized higher studies course": 26,
        "Professional higher technical course": 27,
        "Higher Education - Master (2nd cycle)": 28,
        "Higher Education - Doctorate (3rd cycle)": 29
    }

    # Let the user choose the Mother's Qualification
    dad_qualification = st.selectbox(
        "Fathers's Qualification",
        dad_qualification_option,  index=0
    )

    # Map the selected qualification to its numerical value
    numerical_qualification_dad = dad_qualification_mapping[dad_qualification]

    # Store the numerical value in the data dictionary
    data["Fathers_qualification"] = [numerical_qualification_dad]


with col2:
    # Define the options for Mother's Occupation
    mom_occupation_option = [
        "Student",
        "Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers",
        "Specialists in Intellectual and Scientific Activities",
        "Intermediate Level Technicians and Professions",
        "Administrative staff",
        "Personal Services, Security and Safety Workers and Sellers",
        "Farmers and Skilled Workers in Agriculture, Fisheries and Forestry",
        "Skilled Workers in Industry, Construction and Craftsmen",
        "Installation and Machine Operators and Assembly Workers",
        "Unskilled Workers",
        "Armed Forces Professions",
        "Other Situation",
        "(blank)",
        "Health professionals",
        "Teachers",
        "Specialists in information and communication technologies (ICT)",
        "Intermediate level science and engineering technicians and professions",
        "Technicians and professionals, of intermediate level of health",
        "Intermediate level technicians from legal, social, sports, cultural and similar services",
        "Office workers, secretaries in general and data processing operators",
        "Data, accounting, statistical, financial services and registry-related operators",
        "Other administrative support staff",
        "Personal service workers",
        "Sellers",
        "Personal care workers and the like",
        "Skilled construction workers and the like, except electricians",
        "Skilled workers in printing, precision instrument manufacturing, jewelers, artisans and the like",
        "Workers in food processing, woodworking, clothing and other industries and crafts",
        "Cleaning workers",
        "Unskilled workers in agriculture, animal production, fisheries and forestry",
        "Unskilled workers in extractive industry, construction, manufacturing and transport",
        "Meal preparation assistants"
    ]
    
    # Mapping of occupation options to numerical values
    mom_occupation_mapping = {
        "Student": 0,
        "Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers": 1,
        "Specialists in Intellectual and Scientific Activities": 2,
        "Intermediate Level Technicians and Professions": 3,
        "Administrative staff": 4,
        "Personal Services, Security and Safety Workers and Sellers": 5,
        "Farmers and Skilled Workers in Agriculture, Fisheries and Forestry": 6,
        "Skilled Workers in Industry, Construction and Craftsmen": 7,
        "Installation and Machine Operators and Assembly Workers": 8,
        "Unskilled Workers": 9,
        "Armed Forces Professions": 10,
        "Other Situation": 90,
        "(blank)": 99,
        "Health professionals": 122,
        "Teachers": 123,
        "Specialists in information and communication technologies (ICT)": 125,
        "Intermediate level science and engineering technicians and professions": 131,
        "Technicians and professionals, of intermediate level of health": 132,
        "Intermediate level technicians from legal, social, sports, cultural and similar services": 134,
        "Office workers, secretaries in general and data processing operators": 141,
        "Data, accounting, statistical, financial services and registry-related operators": 143,
        "Other administrative support staff": 144,
        "Personal service workers": 151,
        "Sellers": 152,
        "Personal care workers and the like": 153,
        "Skilled construction workers and the like, except electricians": 171,
        "Skilled workers in printing, precision instrument manufacturing, jewelers, artisans and the like": 173,
        "Workers in food processing, woodworking, clothing and other industries and crafts": 175,
        "Cleaning workers": 191,
        "Unskilled workers in agriculture, animal production, fisheries and forestry": 192,
        "Unskilled workers in extractive industry, construction, manufacturing and transport": 193,
        "Meal preparation assistants": 194
    }

    # Let the user choose the Mother's Occupation
    mom_occupation = st.selectbox(
        "Mother's Occupation",
        mom_occupation_option,  index=0
    )

    # Map the selected occupation to its numerical value
    numerical_occupation_mom = mom_occupation_mapping[mom_occupation]

    # Store the numerical value in the data dictionary
    data["Mothers_occupation"] = [numerical_occupation_mom]


with col3:
    # Define the options for Father's Occupation
    father_occupation_option = [
        "Student",
        "Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers",
        "Specialists in Intellectual and Scientific Activities",
        "Intermediate Level Technicians and Professions",
        "Administrative staff",
        "Personal Services, Security and Safety Workers and Sellers",
        "Farmers and Skilled Workers in Agriculture, Fisheries and Forestry",
        "Skilled Workers in Industry, Construction and Craftsmen",
        "Installation and Machine Operators and Assembly Workers",
        "Unskilled Workers",
        "Armed Forces Professions",
        "Other Situation",
        "(blank)",
        "Armed Forces Officers",
        "Armed Forces Sergeants",
        "Other Armed Forces personnel",
        "Directors of administrative and commercial services",
        "Hotel, catering, trade and other services directors",
        "Specialists in the physical sciences, mathematics, engineering and related techniques",
        "Health professionals",
        "Teachers",
        "Specialists in finance, accounting, administrative organization, public and commercial relations",
        "Intermediate level science and engineering technicians and professions",
        "Technicians and professionals, of intermediate level of health",
        "Intermediate level technicians from legal, social, sports, cultural and similar services",
        "Information and communication technology technicians",
        "Office workers, secretaries in general and data processing operators",
        "Data, accounting, statistical, financial services and registry-related operators",
        "Other administrative support staff",
        "Personal service workers",
        "Sellers",
        "Personal care workers and the like",
        "Protection and security services personnel",
        "Market-oriented farmers and skilled agricultural and animal production workers",
        "Farmers, livestock keepers, fishermen, hunters and gatherers, subsistence",
        "Skilled construction workers and the like, except electricians",
        "Skilled workers in metallurgy, metalworking and similar",
        "Skilled workers in electricity and electronics",
        "Workers in food processing, woodworking, clothing and other industries and crafts",
        "Fixed plant and machine operators",
        "Assembly workers",
        "Vehicle drivers and mobile equipment operators",
        "Unskilled workers in agriculture, animal production, fisheries and forestry",
        "Unskilled workers in extractive industry, construction, manufacturing and transport",
        "Meal preparation assistants",
        "Street vendors (except food) and street service providers"
    ]
    
    # Mapping of father's occupation options to numerical values
    father_occupation_mapping = {
        "Student": 0,
        "Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers": 1,
        "Specialists in Intellectual and Scientific Activities": 2,
        "Intermediate Level Technicians and Professions": 3,
        "Administrative staff": 4,
        "Personal Services, Security and Safety Workers and Sellers": 5,
        "Farmers and Skilled Workers in Agriculture, Fisheries and Forestry": 6,
        "Skilled Workers in Industry, Construction and Craftsmen": 7,
        "Installation and Machine Operators and Assembly Workers": 8,
        "Unskilled Workers": 9,
        "Armed Forces Professions": 10,
        "Other Situation": 90,
        "(blank)": 99,
        "Armed Forces Officers": 101,
        "Armed Forces Sergeants": 102,
        "Other Armed Forces personnel": 103,
        "Directors of administrative and commercial services": 112,
        "Hotel, catering, trade and other services directors": 114,
        "Specialists in the physical sciences, mathematics, engineering and related techniques": 121,
        "Health professionals": 122,
        "Teachers": 123,
        "Specialists in finance, accounting, administrative organization, public and commercial relations": 124,
        "Intermediate level science and engineering technicians and professions": 131,
        "Technicians and professionals, of intermediate level of health": 132,
        "Intermediate level technicians from legal, social, sports, cultural and similar services": 134,
        "Information and communication technology technicians": 135,
        "Office workers, secretaries in general and data processing operators": 141,
        "Data, accounting, statistical, financial services and registry-related operators": 143,
        "Other administrative support staff": 144,
        "Personal service workers": 151,
        "Sellers": 152,
        "Personal care workers and the like": 153,
        "Protection and security services personnel": 154,
        "Market-oriented farmers and skilled agricultural and animal production workers": 161,
        "Farmers, livestock keepers, fishermen, hunters and gatherers, subsistence": 163,
        "Skilled construction workers and the like, except electricians": 171,
        "Skilled workers in metallurgy, metalworking and similar": 172,
        "Skilled workers in electricity and electronics": 174,
        "Workers in food processing, woodworking, clothing and other industries and crafts": 175,
        "Fixed plant and machine operators": 181,
        "Assembly workers": 182,
        "Vehicle drivers and mobile equipment operators": 183,
        "Unskilled workers in agriculture, animal production, fisheries and forestry": 192,
        "Unskilled workers in extractive industry, construction, manufacturing and transport": 193,
        "Meal preparation assistants": 194,
        "Street vendors (except food) and street service providers": 195
    }

    # Let the user choose the Father's Occupation
    father_occupation = st.selectbox(
        "Father's Occupation",
        father_occupation_option,  index=0
    )

    # Map the selected occupation to its numerical value
    numerical_father_occupation = father_occupation_mapping[father_occupation]

    # Store the numerical value in the data dictionary
    data["Fathers_occupation"] = [numerical_father_occupation]

col1, col2, col3= st.columns(3)

with col1:
    Admission_grade = int(st.number_input(
        label='Admission Grade',
        min_value=0,
        max_value=200,
        value=1
    ))
    data["Admission_grade"] = Admission_grade

with col2:
    displaced_option = [
        "No",
        "Yes"
    ]

    displaced_mapping = {
        "No" : 0,
        "Yes": 1
    }

    # Create the selectbox
    displaced = st.selectbox(
        "Daytime or Evening Attendance",
        displaced_option,  index=0
    )

    # Map the selected marital status to its numerical value
    num_displaced = displaced_mapping[displaced]

    # Store the numerical value in the data dictionary
    data["Displaced"] = [num_displaced]

with col3:
    edu_special_need_option = [
        "No",
        "Yes"
    ]

    edu_special_need_mapping = {
        "No" : 0,
        "Yes": 1
    }

    # Create the selectbox
    edu_special_need = st.selectbox(
        "Educational Special Needs",
        edu_special_need_option,  index=0
    )

    # Map the selected marital status to its numerical value
    num_edu_special_need = edu_special_need_mapping[edu_special_need]

    # Store the numerical value in the data dictionary
    data["Educational_special_needs"] = [num_edu_special_need]

col1, col2, col3 = st.columns(3)
with col1:
    debtor_option = [
        "No",
        "Yes"
    ]

    debtor_map = {
        "No" : 0,
        "Yes": 1
    }

    debtor = st.selectbox(
        "Debtor",
        debtor_option,  index=0
    )

    num_debtor = debtor_map[debtor]

    data["Debtor"] = [num_debtor]

with col2:
    fee_option = [
        "No",
        "Yes"
    ]

    fee_map = {
        "No" : 0,
        "Yes": 1
    }

    Tuition_fees_up_to_date = st.selectbox(
        "Tuition fees up to date",
        fee_option,  index=0
    )

    num_fee = fee_map[Tuition_fees_up_to_date]

    data["Tuition_fees_up_to_date"] = num_fee

with col3:
    gender_option = [
        "Female",
        "Male"
    ]

    gender_map = {
        "Female" : 0,
        "Male": 1
    }

    gender = st.selectbox(
        "Gender",
        gender_option,  index=0
    )

    num_gender = gender_map[gender]

    data["Gender"] = [num_gender]

col1, col2, col3 = st.columns(3)
with col1:
    sch_option = [
        "No",
        "Yes"
    ]

    sch_map = {
        "No" : 0,
        "Yes": 1
    }

    scholarship = st.selectbox(
        "Scholarship Holder",
        sch_option,  index=0
    )

    num_sch = sch_map[scholarship]

    data["Scholarship_holder"] = [num_sch]

with col2:
    age_at_enrollment = int(st.number_input(
        label='Age at Enrollment',
        value=17
    ))
    data["Age_at_enrollment"] = age_at_enrollment

with col3:
    inter_option = [
        "No",
        "Yes"
    ]

    inter_map = {
        "No" : 0,
        "Yes": 1
    }

    inter = st.selectbox(
        "International",
        inter_option, index=0
    )

    num_inter = sch_map[scholarship]

    data["International"] = [num_inter]

col1, col2, col3 = st.columns(3)
with col1:
    Curricular_units_1st_sem_credited = int(st.number_input(
        label='Curricular units 1st sem (credited)',
        value=0
    ))
    data["Curricular_units_1st_sem_credited"] = Curricular_units_1st_sem_credited

with col2:
    Curricular_units_1st_sem_enrolled = int(st.number_input(
        label='Curricular units 1st sem (enrolled)',
        value=0
    ))
    data["Curricular_units_1st_sem_enrolled"] = Curricular_units_1st_sem_enrolled

with col3:
    Curricular_units_1st_sem_evaluations = int(st.number_input(
        label='Curricular units 1st sem (evaluations)',
        value=0
    ))
    data["Curricular_units_1st_sem_evaluations"] = Curricular_units_1st_sem_evaluations

col1, col2, col3 = st.columns(3)
with col1:
    Curricular_units_1st_sem_approved = int(st.number_input(
        label='Curricular units 1st sem (approved)',
        value=0
    ))
    data["Curricular_units_1st_sem_approved"] = Curricular_units_1st_sem_approved

with col2:
    Curricular_units_1st_sem_grade = int(st.number_input(
        label='Curricular Units 1st Sem Grade',
        value=0
    ))
    data["Curricular_units_1st_sem_grade"] = Curricular_units_1st_sem_grade

with col3:
    Curricular_units_1st_sem_without_evaluations = int(st.number_input(
        label='Curricular Units 1st Sem Without Evaluations',
        value=0
    ))
    data["Curricular_units_1st_sem_without_evaluations"] =  Curricular_units_1st_sem_without_evaluations

col1, col2, col3 = st.columns(3)
with col1:
    Curricular_units_2nd_sem_credited = int(st.number_input(
        label='Curricular units 2nd sem (credited)',
        value=0
    ))
    data["Curricular_units_2nd_sem_credited"] = Curricular_units_2nd_sem_credited

with col2:
    Curricular_units_2nd_sem_enrolled = int(st.number_input(
        label='Curricular units 2nd sem (enrolled)',
        value=0
    ))
    data["Curricular_units_2nd_sem_enrolled"] = Curricular_units_2nd_sem_enrolled

with col3:
    Curricular_units_2nd_sem_evaluations = int(st.number_input(
        label='Curricular units 2nd sem (evaluations)',
        value=0
    ))
    data["Curricular_units_2nd_sem_evaluations"] = Curricular_units_2nd_sem_evaluations

col1, col2, col3 = st.columns(3)
with col1:
    Curricular_units_2nd_sem_approved = int(st.number_input(
        label='Curricular units 2nd sem (approved)',
        value=0
    ))
    data["Curricular_units_2nd_sem_approved"] = Curricular_units_2nd_sem_approved

with col2:
    Curricular_units_2nd_sem_grade = int(st.number_input(
        label='Curricular Units 2nd Sem Grade',
        value=0
    ))
    data["Curricular_units_2nd_sem_grade"] = Curricular_units_2nd_sem_grade

with col3:
    Curricular_units_2nd_sem_without_evaluations = int(st.number_input(
        label='Curricular Units 2nd Sem Without Evaluations',
        value=0
    ))
    data["Curricular_units_2nd_sem_without_evaluations"] =  Curricular_units_2nd_sem_without_evaluations


col1, col2, col3 = st.columns(3)

with col1:
    # Input for Unemployment Rate
    unemployment_rate = st.number_input(
        "Unemployment Rate",
        min_value=0.0,
        max_value=100.0,
        value=0.01,
        step=0.01,
        format="%.2f"
    )

    # Store the input in the data dictionary
    data["Unemployment_rate"] = [unemployment_rate]

with col2:
    # Input for Unemployment Rate
    inflation_rate = st.number_input(
        "Inflation Rate",
        min_value=0.0,
        max_value=100.0,
        value=0.01,
        step=0.01,
        format="%.2f"
    )

    # Store the input in the data dictionary
    data["Inflation_rate"] = [inflation_rate]

with col3:
    # Input for Unemployment Rate
    GDP = st.number_input(
        "GDP",
        min_value=0.0,
        max_value=100.0,
        value=0.01,
        step=0.01,
        format="%.2f"
    )

    # Store the input in the data dictionary
    data["GDP"] = [GDP]


with st.expander("View the Raw Data"):
    st.dataframe(data=data, width=800, height=10)

if st.button('Predict'):
    try:
        # Preprocess the data
        new_data = data_preprocessing(data=data)
        with st.expander("View the Preprocessed Data"):
            st.dataframe(new_data)

        # Generate prediction
        prediction_result = prediction(new_data)
        st.success(f"Prediction: {prediction_result[0]}")
    except Exception as e:
        st.error(f"Error: {e}")