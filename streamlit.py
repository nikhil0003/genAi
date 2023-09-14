# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 22:38:01 2023

@author: Arenelli nikhil kumar
"""

import streamlit as st
from PIL import Image
import requests
from bs4 import BeautifulSoup 

iconimg= Image.open('workmarket.png')
st.set_page_config(page_title="WorkMarket ZenDesk ", page_icon=iconimg, layout="wide")
st.image(iconimg)
st.title("WorkMarket ZenDesk Powder by GENAI")

text_search = st.text_input("Type your question here", value="")

zendeskurl = "https://workmarket.zendesk.com/hc/en-us/search?utf8=%E2%9C%93&query="
searchurl = (zendeskurl+text_search).replace(" ","+")
headers = {
			    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
				"Accept-Encoding": "gzip, deflate, br",
				"Accept-Language": "en-US,en;q=0.5",
				"Connection": "keep-alive",
				"Cookie": "__cfruid=54cb3857f64ae1b005880f838aaff0ad24a755ea-1694624130; _slvs=eb55ffec-bd38-43a9-964b-d2b9cc37708c; _slvlcl=en-US; cf_clearance=jP6KdBXEFUfWhTyHBI5QGp1WiilEXrCrfEgjVUEMB1E-1694630935-0-1-a65028e9.f511711a.f1517709-0.2.1694630935; _help_center_session=ODZGd3RUV2oybjA3RkdIOE4vY1JPVXFEZ3NWWWhCU1c1U1NMd3RKVm5Qb1dEMW5MSlIrNGVlQS9xaXNVUzBsZDA0Vzh0VlNuNlNPSXFUbDk4L2pJbkZ0MXBiUUZFZlplenVoSVpTaHAwdWlRTlEzcVFBTVhiYzlGanhpT09aYURIUVNkLzREazhQbGdIeTg2RlRhVXhxVkMxY0NsdHg3ZVFCN2R4V0VHSnZEOXR3cGNuNkRhd3g0cDdzWklaeWJMNnBmQ0RMbGdyK0szL2k4Z2xUSkRnZz09LS05R0d2cE9zS2pYVytPRmVyV0g4S0lRPT0%3D--73c5575e5b495f9d6b788b657ee4aff7eafcf8bd; _ga=GA1.2.579614414.1694624122; _gid=GA1.2.1395002351.1694624122; _ga_4EMZFKPZFQ=GS1.2.1694626997.2.1.1694631761.0.0.0; ajs_anonymous_id=38dde465-fbe6-4ed5-b35f-a4417674e22b; _pendo_visitorId.df3d609f-14a9-4a77-b441-73602a4aaab2=_PENDO_T_38dde465-fbe6-4ed5-b35f-a4417674e22b; _pendo_accountId.df3d609f-14a9-4a77-b441-73602a4aaab2=; _pendo_meta.df3d609f-14a9-4a77-b441-73602a4aaab2=1977288925; _pendo___sg__.df3d609f-14a9-4a77-b441-73602a4aaab2=%7B%7D; _pendo_guides_blocked.df3d609f-14a9-4a77-b441-73602a4aaab2=0; _slvddv=true; solvvySelectedPersona=worker; _zendesk_shared_session=-eFBwK2xlRlZWanl2aXFpUW9sSllLbmRVbjZKRjhKZVpEa0duN0RHZExYNzhmMFZWeHkrUXJrNmNFWUNTVWtCTzlQM3ppWXVQb055ZFBva3lQY3pDek1RUk1mMXZaVEhFTENNeDA3RjFrK3ZGaUI4dXZkdys0clRZbDlCUll1VXUtLXFxYUdvVjB4ZlNQc2FSUlM0Nyt1dUE9PQ%3D%3D--b22af1b93b5c0db9d12e372aaf1113f833e698ec; _zendesk_session=cBuoSXTWKhJBCAmljFyvXp6nzUTHvpNPqT3%2FFBdwSuFj0897okwA7HnPcSlK4HZxRuWFYlAGaGwh0TnjUlA280tzTY8GEJQDHBKis86nZ2ctQmqGkLOS7lZNmB8TT6qaw%2BVg%2BP4z42Qt9QrHHt2KG1eAQnA%2FG1eNyA40l2TQFkXH3TsvT5FsV%2B0vu9GF5luz8qqhbiGU3OsgQFa4FCyOfjX74QYA%2FSEj6FGS6Up8hknqwL3nP2qT2ABWYIh1awb7el3KDG6ZJWmFN%2BI%2FmQNymW6TdCFSjtvlaXXPsYefNG4qnjDH3ZDrzdkx1fYFGh6yjBf%2FJdClAi97WfL2TBVqqqLAaoKeXzyoNvhQDzODtzm8B3MrqkzbR3xZCY3alEtZraETmfC76Cz%2BnB%2Bu%2B%2BfskXeLohA%3D--mPHnysEyuSfz%2F7SI--ht%2B5DuvA28WPUisiSphZKQ%3D%3D; _zendesk_authenticated=1; _zendesk_cookie=BAhJIkx7ImRldmljZV90b2tlbnMiOnsiMTc1MDM5NDQ2NDAyNzkiOiJ4eG1FYXlrQndhQ2twUXVTSFhCWkdRZTVjZ2dQcnc1ViJ9fQY6BkVU--c8b06bc3ff49345f713bfd0e1666f72f3c380be6; _gat=1",
				"Host": "workmarket.zendesk.com",
				"If-None-Match": "W/\"f8ff4a12093bc8281717a2ee0ecbe57d\"",
				"Sec-Fetch-Dest": "document",
				"Sec-Fetch-Mode": "navigate",
				"Sec-Fetch-Site": "none",
				"Sec-Fetch-User": "?1",
				"TE": "trailers",
				"name": "Upgrade-Insecure-Requests",
				"Upgrade-Insecure-Requests": "1",
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
			}
page= requests.get(searchurl,headers=headers)

print(page)
#print(requests.get("https://workmarket.zendesk.com/hc/en-us"))

