import requests

from encry import AESCipher


def get_api_result(_id):
    """get json from api"""
    url = f"https://yyets.dmesg.app/api/resource?id={_id}"
    c = AESCipher("40595")
    en_str = c.encrypt(f"/api/resource?id={_id}")

    headers = {
        "ne1": en_str.decode('utf-8'),
        "referer": f"https://yyets.dmesg.app/resource.html?id={_id}",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }

    resp = requests.get(url, timeout=10, headers=headers).json()
    print(resp)
    if not resp['info'] == 'OK':
        print("some error!")
        return
    info = resp['data']['info']
    print(f"To Download: {info['cnname']}")
    resource_list = resp['data']['list']
    indexs = {r['season_num']: r['season_cn'] for r in resource_list}
    items = {r['season_num']: r['items'] for r in resource_list}
    print("*"*20)
    for k,v in indexs.items():
        print(f"[{k}]{v}") 
    print("*" * 20)
    num = None
    while True:
        num = input("Please Input Index[*]:")
        num = num.strip()
        if num in indexs.keys():
            break
    print(f"Selected Num: {indexs.get(num)}")
    item = items.get(num)
    print("*" * 20)
    for i, v in enumerate(item.keys()):
        print(f"[{i}]{v}")
    format_num = None
    while True:
        format_num = input("Please Input Format Index[*]:")
        format_num = format_num.strip()
        if format_num in [str(i) for i in range(len(item.keys()))]:
            break
    
    format_name = list(item.keys())[int(format_num)]
    print(f"Selected Format: {format_name}")
    item_list = item.get(format_name)
    magenets = []
    for f in item_list:
        files = f['files']
        for m in files:
            if m['way_cn'] == "磁力":
                magenets.append(m['address'])
    
    print("*** All Magnet Urls ***")
    for k in magenets:
        print(k)
    print("*** Done ***")


def crawler(url):
    """"crawler of the https://yyets.dmesg.app/ """
    print(f"source url: {url}")
    _, r_id = url.split("=")
    print(f"resource id: {r_id}")
    get_api_result(r_id)


if __name__=="__main__":
    resource = input("Please Input Id: ")
    # https://yyets.dmesg.app/resource.html?id=36232
    get_api_result(resource.strip())
