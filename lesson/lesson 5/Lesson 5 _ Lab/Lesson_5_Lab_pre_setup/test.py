# test_connect.py
# import thư viện bigquery
from google.cloud import bigquery

# tự đọc GOOGLE_APPLICATION_CREDENTIALS
# tạo client bigquery
client = bigquery.Client()

# thực thi query kết nối bằng mail
df1 = client.query("SELECT 1 AS ok")\
         .to_dataframe()
print(df1)

# thực thi query lấy bằng thông qua key của gg cloud
# df2 = client.query("select * from `project-9d3c9d87-4adc-4d3b-ac1.banking_clean.dim_merchant`")\
#          .to_dataframe()
# print(df2)