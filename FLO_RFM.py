
###############################################################
# Customer Segmentation with RFM
###############################################################

###############################################################
# Business Problem
###############################################################
# An online shoe store (FLO) wants to segment their customers and define marketing strategies according to these segments.
# For this purpose, behaviors of customers will be defined and groups will be formed according to clusters in behaviors.
###############################################################
# Dataset Story
###############################################################

# Dataset includes information obtained from the past shopping behavior of OmniChannel
# (both online and offline shoppers) customers whose last purchases was in 2020–2021.

# master_id: Unique customer ID
# order_channel : Code for the platform that is used for the purchase (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : Code for the platform that is used for the last purchase
# first_order_date : Date of the first purchase
# last_order_date : Date of the last purchase
# last_order_date_online : Date of the last online purchase
# last_order_date_offline : Date of the last offline purchase
# order_num_total_ever_online : Total number of online purchases
# order_num_total_ever_offline : Total number of offline purchases
# customer_value_total_ever_offline : Total money spent on offline purchases
# customer_value_total_ever_online : Total money spent on online purchases
# interested_in_categories_12 : Category list that the customer purchased from in the last 12 months


###############################################################
# TASKS
###############################################################

# TASK 1: Data Understanding and Preparation
# 1. Reading dataset into pycharm:

import pandas as pd
import datetime as dt

pd.set_option('display.max_columns', None) # to see all the columns
df_ = pd.read_csv("D:/MIUUL/CRM/CASE STUDY 1/FLOMusteriSegmentasyonu/flo_data_20k.csv")
df = df_.copy()

# 2. In dataset:
    # a. First 10 rows:
    df.head(10)

    # b. Column names:
    df.columns

    # c. Descriptive statistics:
    df.describe().T
    df.shape

    # d. Empty values:
    df.isnull().sum()

    # e. Type of the variables:
    df.dtypes

df["master_id"].nunique()

# 3. Customers are both online and offline shoppers.
# Create new variables for each customer's total number of purchase and total spending
df.head() #before

    # a. Customer's total number of purchase:
    df["total_order_number"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]

    # b.Customer's total spending:
    df["total_spending"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]

df.head() #after

# 4. Check variable types. Convert date variables type into date type.
df["first_order_date"].dtypes # before: this variable means a date however its type is seen as object.

df['first_order_date'] = pd.to_datetime(df['first_order_date'])
df['last_order_date'] = pd.to_datetime(df['last_order_date'])
df['last_order_date_online'] = pd.to_datetime(df['last_order_date_online'])
df['last_order_date_offline'] = pd.to_datetime(df['last_order_date_offline'])

df.dtypes # after

# 5. Find the breakdown of the number of customers, average number of products purchased, and average spend across shopping channels.

a = df.groupby(["order_channel"]).agg({"master_id": "count", "total_order_number": "mean","total_spending": "mean"})
a.columns = ['number of customers', 'average number of products purchased', 'average spend']

# 6. Rank the top 10 customers with the highest revenue.

df[["master_id", "total_spending"]].sort_values(by = "total_spending", ascending= False).head(10)

# 7. List the top 10 customers with the most orders.

df[["master_id", "total_order_number"]].sort_values(by = "total_order_number", ascending= False).head(10)

# 8. Functionalization of the data preparation process.

def preliminary(dataframe, do_print=False):

    dataframe["total_order_number"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["total_spending"] = dataframe["customer_value_total_ever_online"] + dataframe["customer_value_total_ever_offline"]

    dataframe['first_order_date'] = pd.to_datetime(dataframe['first_order_date'])
    dataframe['last_order_date'] = pd.to_datetime(dataframe['last_order_date'])
    dataframe['last_order_date_online'] = pd.to_datetime(dataframe['last_order_date_online'])
    dataframe['last_order_date_offline'] = pd.to_datetime(dataframe['last_order_date_offline'])

    breakdown = dataframe.groupby(["order_channel"]).agg(
        {"master_id": "count", "total_order_number": "mean", "total_spending": "mean"})
    breakdown.columns = ['number of customers', 'average number of products purchased', 'average spend']

    top10renevue = dataframe[["master_id", "total_spending"]].sort_values(by="total_spending", ascending=False).head(10)
    top10order = dataframe[["master_id", "total_order_number"]].sort_values(by="total_order_number", ascending=False).head(10)

    if do_print:
        print("DATA UNDERSTANDING:\n\n\n")
        print("FIRST 10 ROWS:\n", dataframe.head(10), "\n\nCOLUMN NAMES:\n", dataframe.columns,
              "\n\nSTATISTICS:\n", dataframe.describe().T, "\nSHAPE:", dataframe.shape,
              "\n\nEMPTY VALUES:\n", dataframe.isnull().sum(), "\n\nVARIABLE TYPES:\n", dataframe.dtypes)
        print("\n\nCREATING NEW VARIABLE:\n\n\n")
        print(dataframe.head())
        print("\n\nBREAKDOWN:\n\n", breakdown)
        print("\n\ntop10renevue:\n\n",top10renevue)
        print("\n\ntop10order:\n\n", top10order,"\n\n")

    return breakdown, top10renevue, top10order

breakdown, top10renevue, top10order = preliminary(df, do_print=False)

df.head()
# TASK 2: Calculation of RFM Metrics

df["last_order_date"].max()
today_date = dt.datetime(2021, 6, 1)

rfm = df.groupby('master_id').agg({'last_order_date': lambda last_order_date: (today_date - last_order_date).astype('timedelta64[D]').astype(int),
                                    "total_order_number": sum,
                                    "total_spending": sum})
rfm.head()

rfm.columns = ['recency', 'frequency', 'monetary']
rfm.describe().T
rfm.shape
# TASK 3: Calculation of RFM Scores

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
# recency metrics divided 5 equal parts acoording to their sizes and
# labelled such a way that greatest recency got 1, the smallest recency got 5.

rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
# the problem in frequency is some numbers are too repetitive that
# qcut function can not label the same frequency number diffently
# rank method solves this problem by assigning the first comer number to first label.

rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))
# by RFM definition, string is created with recency and frequency score
# and formed final RFM Score
# monetary score is necessary for observation, but it is not used in forming RFM Score

# TASK 4: Scores to segments:

# regex
# RFM Naming (Pattern Matching)
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}
#  Basically the R-F table is coded using regex.

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
rfm.head()

# TASK 5: ACTION!:
    # 1. Examine the recency, frequency and monetary averages of the segments.
    segment_analysis = rfm.groupby('segment').agg({'recency': "mean",
                                                    "frequency": "mean",
                                                    "monetary": "mean",
                                                    "segment": "count"})
    segment_analysis.columns = ['recency(mean)', 'frequency(mean)', 'monetary(mean)', "count"]

    # 2. With RFM analysis, find the customers in the relevant profile for 2 cases and save the customer IDs to csv.

        # a. FLO includes a new women's shoe brand. The product prices of the brand it includes are above the general customer preferences.
        # For this reason, customers in the profile who will be interested in the promotion of the brand and product sales are requested to be contacted privately.
        # From their loyal customers(champions,loyal_customers), the customers who shop in the women category with an average of 250 TL or more will be contacted privately.
        # Import Id numbers of these customers to csv file and save it as new_brand_target_customer_id.cvs.

        # First solution:
        ###########################################################################################################################################

        # Category info and (segment and monetary) info are on different data frames.
        # Two lists of IDs will be found and their intersection is going to be extracted.

        loyals_over250_id = list(rfm[(((rfm['segment'] == "champions") | (rfm['segment'] == "loyal_customers")) & (rfm['monetary'] > 250 ))].index)
        len(loyals_over250_id)

        df["interested_in_categories_12"] = df["interested_in_categories_12"].astype(str)
        women = list(df[df["interested_in_categories_12"].str.contains("KADIN")]["master_id"])
        len(women)

        new_brand_target_customer_id = pd.DataFrame(list(set(loyals_over250_id).intersection(women)))
        new_brand_target_customer_id.columns = ["new_brand_target_customer_id"]
        new_brand_target_customer_id.shape

        df[df["master_id"] == "fc6cf7f6-9d72-11eb-9c47-000d3a38a36f"]
        rfm.loc["fc6cf7f6-9d72-11eb-9c47-000d3a38a36f"]
        # to check

        new_brand_target_customer_id.to_csv("new_brand_target_customer_id.csv")
        ###########################################################################################################################################
        # Second solution:

        rfm2 = df.groupby('master_id').agg({'last_order_date': lambda last_order_date: (today_date - last_order_date).astype('timedelta64[D]').astype(int),
                                            "total_order_number": sum,
                                            "total_spending": sum,
                                            "interested_in_categories_12": sum})

        rfm2.columns = ['recency', 'frequency', 'monetary', "interested_in_categories_12"]
        rfm2["recency_score"] = pd.qcut(rfm2['recency'], 5, labels=[5, 4, 3, 2, 1])
        rfm2["frequency_score"] = pd.qcut(rfm2['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
        rfm2["monetary_score"] = pd.qcut(rfm2['monetary'], 5, labels=[1, 2, 3, 4, 5])
        rfm2["RFM_SCORE"] = (rfm2['recency_score'].astype(str) +
                            rfm2['frequency_score'].astype(str))

        seg_map = {
            r'[1-2][1-2]': 'hibernating',
            r'[1-2][3-4]': 'at_Risk',
            r'[1-2]5': 'cant_loose',
            r'3[1-2]': 'about_to_sleep',
            r'33': 'need_attention',
            r'[3-4][4-5]': 'loyal_customers',
            r'41': 'promising',
            r'51': 'new_customers',
            r'[4-5][2-3]': 'potential_loyalists',
            r'5[4-5]': 'champions'
        }


        rfm2['segment'] = rfm2['RFM_SCORE'].replace(seg_map, regex=True)

        rfm2["interested_in_categories_12"] = rfm2["interested_in_categories_12"].astype(str)

        second_new_brand_target_customer_id = pd.DataFrame(list(rfm2[((rfm2['segment'] == "champions") | (rfm2['segment'] == "loyal_customers"))
                                              & (rfm2['monetary'] > 250 )
                                              & (rfm2["interested_in_categories_12"].str.contains("KADIN"))].index))

        second_new_brand_target_customer_id.to_csv("second_new_brand_target_customer_id.csv")
        second_new_brand_target_customer_id.shape
        ###########################################################################################################################################

        # b. Up to 40% discount is planned for Men's and Children's products. Customers related to this sale are can't loose customers,
        # those who are asleep and new customers. Enter the ids of the customers in the appropriate profile into the csv file as discount_target_customer_ids.csv

        ###########################################################################################################################################
        # First solution:
        target_segments_id = list(rfm[(rfm['segment'] == "at_Risk") | (rfm['segment'] == "hibernating") | (rfm['segment'] == 'cant_loose') | (rfm['segment'] == "new_customers")].index)
        len(target_segments_id)

        df["interested_in_categories_12"] = df["interested_in_categories_12"].astype(str)
        men_or_child = list(df[df["interested_in_categories_12"].str.contains("ERKEK") | df["interested_in_categories_12"].str.contains("COCUK")]["master_id"])
        len(men_or_child)

        discount_target_customer_ids = pd.DataFrame(list(set(target_segments_id).intersection(men_or_child)))
        discount_target_customer_ids.columns = ["discount_target_customer_ids"]
        discount_target_customer_ids.shape

        df[df["master_id"] == "6a8a8408-ee09-11e9-9346-000d3a38a36f"]
        rfm.loc["6a8a8408-ee09-11e9-9346-000d3a38a36f"]
        # to check

        discount_target_customer_ids.to_csv("discount_target_customer_ids.csv")
        ###########################################################################################################################################
        # Second solution:

        second_discount_target_customer_ids = pd.DataFrame(list(rfm2[((rfm2['segment'] == "at_Risk") | (rfm2['segment'] == "hibernating")
                                                                     | (rfm2['segment'] == 'cant_loose') | (rfm2['segment'] == "new_customers"))
                                                                     & ((rfm2["interested_in_categories_12"].str.contains("ERKEK"))
                                                                     | (rfm2["interested_in_categories_12"].str.contains("COCUK")))].index))

        second_discount_target_customer_ids.to_csv("second_discount_target_customer_ids.csv")
        second_discount_target_customer_ids.shape

        ###########################################################################################################################################

# TASK 6: Functionalization

def final(dataframe, csv=False):

    dataframe["total_order_number"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["total_spending"] = dataframe["customer_value_total_ever_online"] + dataframe["customer_value_total_ever_offline"]
    dataframe['first_order_date'] = pd.to_datetime(dataframe['first_order_date'])
    dataframe['last_order_date'] = pd.to_datetime(dataframe['last_order_date'])
    dataframe['last_order_date_online'] = pd.to_datetime(dataframe['last_order_date_online'])
    dataframe['last_order_date_offline'] = pd.to_datetime(dataframe['last_order_date_offline'])

    today_date = dt.datetime(2021, 6, 1)
    rfm2 = dataframe.groupby('master_id').agg(
        {'last_order_date': lambda last_order_date: (today_date - last_order_date).astype('timedelta64[D]').astype(int),
         "total_order_number": sum,
         "total_spending": sum,
         "interested_in_categories_12": sum})

    rfm2.columns = ['recency', 'frequency', 'monetary', "interested_in_categories_12"]
    rfm2["recency_score"] = pd.qcut(rfm2['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm2["frequency_score"] = pd.qcut(rfm2['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm2["monetary_score"] = pd.qcut(rfm2['monetary'], 5, labels=[1, 2, 3, 4, 5])
    rfm2["RFM_SCORE"] = (rfm2['recency_score'].astype(str) +
                         rfm2['frequency_score'].astype(str))
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }
    rfm2['segment'] = rfm2['RFM_SCORE'].replace(seg_map, regex=True)
    rfm2["interested_in_categories_12"] = rfm2["interested_in_categories_12"].astype(str)

    segment_analysis = rfm2.groupby('segment').agg({'recency': "mean",
                                                   "frequency": "mean",
                                                   "monetary": "mean",
                                                   "segment": "count"})
    segment_analysis.columns = ['recency(mean)', 'frequency(mean)', 'monetary(mean)', "count"]
    if csv:
        rfm2.to_csv("rfm.csv")

    return rfm2

final(df)