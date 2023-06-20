import requests as rq
from bs4 import BeautifulSoup
import pandas as pd

table_data = pd.DataFrame()

url = "https://etherscan.io/dextracker_txns?q=0x5adebafbf2fd0d6808a7a1e823759de2df1df39e"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
r = rq.get(url,headers=headers)

soap = BeautifulSoup(r.content,'html5lib')

total_page = soap.find_all({"span" : 'page-link text-nowrap'})[7].text.split()
first_page = int(total_page[1])+1
last_page = int(total_page[-1])

main_table = soap.find("tbody")

for table in main_table.find_all('tr'):
        temp_df = pd.DataFrame()
        td = table.find_all('td')  
        txn_hash = td[1].find('span').text
        age = td[2].find('span').text
        action = td[5].find('span').text
        token_amount_out = td[6].text
        token_out = td[6].text.split(' ')[1]
        token_amount_in = td[7].text
        temp_df['txn_hash'] = [txn_hash.strip()]
        temp_df['age'] = [age]
        temp_df['action'] = [action]
        temp_df['token_amount_out'] = [token_amount_out]
        temp_df['token_out'] = [token_out]
        temp_df['token_amunt_in'] = [token_amount_in]
        table_data = pd.concat([table_data,temp_df],axis=0)
    
for page_no in range(first_page,last_page+1,1) :
    url = "https://etherscan.io/dextracker_txns?q=0x5adebafbf2fd0d6808a7a1e823759de2df1df39e&p="+str(page_no)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = rq.get(url,headers=headers)
    soap = BeautifulSoup(r.content,'html5lib')
    main_table = soap.find("tbody")
    print(url , '------>', page_no)
    page_df = pd.DataFrame()
    aaa = 0
    for table in main_table.find_all('tr'):
        temp_df = pd.DataFrame()
        td = table.find_all('td')  
        txn_hash = td[1].find('span').text
        age = td[2].find('span').text
        action = td[5].find('span').text
        token_amount_out = td[6].text
        token_out = td[6].text.split(' ')[1]
        token_amount_in = td[7].text
        temp_df['txn_hash'] = [txn_hash.strip()]
        temp_df['age'] = [age]
        temp_df['action'] = [action]
        temp_df['token_amount_out'] = [token_amount_out]
        temp_df['token_out'] = [token_out]
        temp_df['token_amunt_in'] = [token_amount_in]
        page_df = pd.concat([page_df,temp_df],axis=0)

    table_data = pd.concat([table_data,page_df],axis=0)

        
table_data.to_csv('Final.csv',index=False)