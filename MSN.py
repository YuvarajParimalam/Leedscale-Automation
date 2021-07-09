import requests
from bs4 import BeautifulSoup as soup
from urllib.parse import quote
import os
import pandas as pd
import time

headers = {
    'authority': 'www.bing.com',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-full-version': '"91.0.4472.124"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0"',
    'sec-ch-ua-model': '""',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.bing.com/?toWww=1&redig=928B412FB95946F0AEEBDDC7F7672265',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'MUID=0EE696265F4C6A4408B586385E846B1E; MUIDB=0EE696265F4C6A4408B586385E846B1E; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=694E67801C404E51AC18D99358997271&dmnchg=1; BFBUSR=BAWAS=1&BAWFS=1; BFB=AhDvg_EBRoj4OrOLX7Y8nk_IZLr5p8Dj5wEEleutlrzYZxNf-SCpiUpkJBrlLl9603Cl7hMBfev8Kk44hBhPlSgMi_9Eu6gaVZzwtKV3Dvn2K5eDd46EDf4hijt_PzWi4rKjvzXy2te4Dj5reTYBwOywUtkEqz9uKSK6zkAiLS1cPQ; SRCHUSR=DOB=20210428&T=1619601240000&TPC=1624942439000; _SS=SID=08910F4310416A4F0FFD1F2D11EC6BDA; _HPVN=CS=eyJQbiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMS0wNy0wOFQwMDowMDowMFoiLCJJb3RkIjowLCJEZnQiOm51bGwsIk12cyI6MCwiRmx0IjowLCJJbXAiOjR9; OID=AhCAXF3NyAWH5hj1CGUjeMh37vujcQ_1HaLXWIi4AwEoreXDQVUgJHDG-827QTXyeRj0tTdwvMMGLCnoR6TqilEky9JzbkHIZcECcVZzWCutCfnC27PyNcHuNfH6fuuhdCCVq_y-2Cp8spmHzhdFgCfO; OIDI=ghAGG0VUekUab42Hx0pfBjoSHnpz45YflEiH5Znjw2Qq066htmynAPCl46bEg62fyWbAdX3sR0syh9I1CB-fzogsynK3HCQumeIk_pAC2v58450EAYGGSPH-guSDE5Y-Ao9T-eKRIMPEQwIab5IxNiYQnqyEnjzdh-WH4kk5P5wzjqjNNtzBr_sF82limaMBIryBFFCXk-ussnoHrDvzzY0rsQxFYfyfbzzt5LzcbNQFa-F58X9axa4AFxGM-FxJtNCkehRV3Bm0MuNYn0igTCMqGIswuBYgjq5raxjnso_J6WunGJyowDdG1aHKhhmBpovrcBeBb-fv7GtnK59tHZaP8yqKGnUyKEWdpqgt1PU9iTUjTZzWejAQsXrrT2NHVzaDVLZRuoPtLVybtDRuWY348XoPmzQWI_y62el_2xpJu2xos6xA8BagdKkDZ5ne7gCD81yU31OlxTycIFYlMobfNZMuQDAwwfMhWfthwtz50oKnYK8kIFZ4q11l2WZm8Vh6AqWiTV8qEpwY7ME-0Q_CKi9Q071QwWslB7UmQ0ynS2towfN2MHqkOULdCCcaI0KYTEHTiX8ekZnaJmAn7Ln_pX7sDKOj9iW4OYcP_7g7n5tHDs1NAJFEdSCLhyEXtCYf-hpxgeCZACQUdjmUdPlCnPOM0iTm0pEJVShJW_6ref9zASqyIEnI3ShEE3dIGuuHUQ3wnh8luLqn3ekBuoP2m0rqi-5dp9aN4_iZrPGd_gZg6c57tkiojjnalE7wNROEp_2rD2MuhNzdtLcvhcL4S4NDZnqRzRmXEIA7mgY9j-oGjILSGScmYw6X_DqnAWZIvQsymBJBigLP7rc37fcupB1Kw862wQmrPfnRUxC7G2KycEgDGFcIkCPtz7r4WKb26Wkalg4PKOJCj6O_Bds9FDP8jzoqjY22tY8aWXmhxJxBajP44JbDAN-AS8CFO34k44Z-5hMysHD8KGsRuuFYYYKb8X5ZJWJ4wh4BrHufAVf4IOv4TT4eLVRA_1qSFw0DIbuHvcHzBErJ1lMnnFMcnib66nSUTQX5cFbawlf6S6eDjZOQHKM0iUOLewwiP2G9ywgWNL3xSCudjiJVjD2A00Hhat4Uxh2w7EjeVDDrTIOBKicml_JnWmxPU6SdWFOQ98pctInYSdQ7hlO8YHMw3z6ojj_JqVI4-YxxUl_BscJbtfRSpuE3AmYvcznSwDSznHiWPEjCfGvq4raH-0lTpWXQ_Ckch7yM2z-JVGpSGmcTJKc20MldQA8BtpTJPKhUwh5ghpubYFclYZ3lPEZBrUS_3L7n4EjbuR5zgPWZ3i8XeS9w8wEkG2QH7JM1BmNli7G42KUMd6doKem0oFBsbmbDvMA4E2YVSgJqGwY7SG0sd8D8bOXmsA6iDhQ8c7hgXH2QS78g6XCzuN0lYS_5TH3f-JBd6mYxXUNoXOgecTgPMgytjmWPtV6AcA2I1hzMO5w2c5ckQ7UnpMI3ELupj3ZiTxN-2J5tmy1M6dKvTgdgWR5_IPK0tM2xu_kbFE79cmlHehgQw_oHYYi19pjPSo_rLrcybpmUe3SPIZ62yrb4KJbRDiVCeEXa1TmGVyjkecZOOLObbvJDZyucqXUEudxNdcL_sG_-xiUeK8k9zBGk58S6V9p-IpZHnasp4M1th9TuIRN-z4GoRGHKGoRDfk9mtJzJfPfZDr4JxQLuuSkBhxQk49pZ0DXw1mL1I5UWCDSmB3qoGjSumVkSzydwV77nT_gZguKktFT4Ldpdha0hCs1JJ8DsTJtpwLLtm6dZFlM77kvQ2n7BtwgEAWxQVgGQ9Nbh4rvC4hnIcoz4egCLItpl2aAphPDWW49epThM2Xfns2W5bQ1SUClfxvUlYNFmZsRO61pfWFa6UoQVKU7Rnf052EaTEKkDXx7_g2w; OIDR=ghDWmywkB1d-g4e5vggGrTO4RVgqYE9K-EhdvRqKbkngxy-14HJXOrf8OMxNdzdslTpav6_wJlFYdr-ZNfs_QnZuOdKcERgIa0dyQoDXJDQdI_bseJoTMWfzG69XqAzMR3dPTAl6YZ-h5cVirXevR4i06I54VYpUVJdYsbDSyuFm5Gez689o3BY4DcG7euh38HgxXqviRqqfVFby1rK2N0B4XlXMfXe9iwAL8Y6kzqyUREJ3RxVk8W_WrCp-NQdLiB7Z1N5RfWbpG_nB04farw-l8EmFrNeq-JjrZPiKXjQRKHuEJX1LE33yiiRhL4-rLU2_gk72kNQmww4T0vRCGIUG5tWzk3bzyjeiUvDc_eQieMfu-oJQYmH5Wo2hXxK2y7AvmQX6K-J0UIIeP3aywTzckfyUYuhMW5E7l4-Ln5v-d_diDHbXRezZF_X4lAs9-uCKk_6Epsse-IlmHPXofzGB7fhqbnIl28eKMffxhk34RGxtRPoGiIFfDuN9maYXWe6iXYEvzJqKfHvwKNHN3YRL8R8G0B5RebVFUmUyFpbjzarig_WMYEwZx-BbB26fee8b_RKDZJ7qf8T6ueyO0Rx780rJfvT0fNNZ5jNgRFAXsMS38VOCgScqbupvQxqoXlyZkQFzVAqyW19RXHwc960wsh2AR2c8WNTWViUlM-3l5_zvY535sZM9ccIU7QliwVKhCxu8bNbSzcvavI0fqmf3kLCxnlpJpFtt3hGX8wMyC6w3FSsJ8LLo7f4SjUWsRQV7lmMN47VUEuySVQhxUEbXL8ExvJUkX7wI-0hVrRCy_1rnu7yXHLsm4TyECBRelIbBjwDdi0Cmr6sBukeHGmoPFfeaw7zGp3FQ2q0nmrstgVHli8H4npM9A8TmObu73RzGfSc1Es9SaI5JrQdZsRrZwxOQn_GE_mbBdiSEQ2zRjTsBuOw4EF2ft7jwiB1kJjOdxERFdS1j5hgCdoDw1v0azBb_aEY5AEqBeqrW0LwSM3qMAAtb2399PKobUcypFl0wk37R3c3NjOJPmYDa0t9WUERvWd5NZi_k-PuT0NKmQbDFS-sLjlQ9YjeujN8cty0SeKvjNriCa2etY7vtDtBDeayV-wh5oFaXHaZLSPWjytj3cW3FkBKQjjGqUShYicK1b_PMU9ur9zi1wBy6ygVrRal4X-TsB6SubW8nbHtNz3GHO2btmfWL9KIIxr5cIVq1GSclYk_Ddp3J1LpJtQWlU3P1H_m5jj2O4TlSBLr7qA; ipv6=hit=1625748655102&t=4; SRCHHPGUSR=SRCHLANGV2=en&BRW=W&BRH=S&CW=1366&CH=272&DPR=1&UTC=330&DM=0&HV=1625745056&WTS=63755198040&SRCHLANG=en; _EDGE_S=SID=08910F4310416A4F0FFD1F2D11EC6BDA&mkt=en-in',
}


def MSN_Scraper(company,Domain):
    company=company+' '+Domain
    query=quote(company)
    response = requests.get('https://www.bing.com/search?q={}'.format(str(query)), headers=headers)
    time.sleep(2)
    data=soup(response.text,'html.parser')
    try:
        url=data.find('h2').find('a')['href']
    except:
        url=''
    return url
