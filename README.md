# Customer Segmentation with RFM

## **Business Problem**

An online shoe store (FLO) wants to segment their customers and define marketing strategies according to these segments.
For this purpose, behaviors of customers will be defined and groups will be formed according to clusters in behaviors.

## **Dataset Story**

Dataset includes information obtained from the past shopping behavior of OmniChannel
(both online and offline shoppers) customers whose last purchases was in 2020–2021.

- master_id: Unique customer ID
- order_channel : Code for the platform that is used for the purchase (Android, ios, Desktop, Mobile, Offline)
- last_order_channel : Code for the platform that is used for the last purchase
- first_order_date : Date of the first purchase
- last_order_date : Date of the last purchase
- last_order_date_online : Date of the last online purchase
- last_order_date_offline : Date of the last offline purchase
- order_num_total_ever_online : Total number of online purchases
- order_num_total_ever_offline : Total number of offline purchases
- customer_value_total_ever_offline : Total money spent on offline purchases
- customer_value_total_ever_online : Total money spent on online purchases
-# interested_in_categories_12 : Category list that the customer purchased from in the last 12 months

## **Problems:**

1. FLO includes a new women's shoe brand. The product prices of the brand it includes are above the general customer preferences.For this reason, customers in the profile who will be interested in the promotion of the brand and product sales are requested to be contacted privately.From their loyal customers (champions,loyal_customers), the customers who shop in the women category with an average of 250 TL or more will be contacted privately.Import Id numbers of these customers to csv file and save it as new_brand_target_customer_id.cvs.

2. Up to 40% discount is planned for Men's and Children's products. Customers related to this sale are can't loose customers, those who are asleep and new customers. Enter the ids of the customers in the appropriate profile into the csv file as discount_target_customer_ids.csv

