import requests


def get_data(keywords: str, count: int, title: str, price: str, template_ids: list):
    try:
        os.makedirs('./ori_image/' + keywords)
    except:
        pass
    try:
        os.makedirs('./output_image/' + keywords)
    except:
        pass
    cut_len = int(count/100) + 1
    image_list = []
    headers = {
        'Host': 'pic.sogou.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'

    }
    for i in range(cut_len):
        params = {
            'mode': 6,
            'start': i*100+1,
            'xml_len': 100,
            'query': keywords

        }
        result = requests.get('https://pic.sogou.com/napi/pc/searchList', params=params, headers=headers)
        try:
            for item in result.json()['data']['items']:
                ori_pic_url = item['oriPicUrl']
                if ori_pic_url != '':
                    image_list.append(ori_pic_url)
        except:
            pass
    image_set = set(image_list)
    i = 0
    for url in image_set:
        try:
            response = requests.get(url, timeout=10)
            if int(response.headers['content-length']) > 1000:
                img = response.content
                content_type = response.headers['content-type'].split('/')[-1]
                if content_type in ['jpg', 'png', 'jpeg', 'webp']:
                    with open('./ori_image/' + keywords + '/' + str(i) + '.' + content_type, 'wb') as f:
                        f.write(img)
                        i = i+1
                    img = Image.open('./ori_image/' + keywords + '/' + str(i) + '.' + content_type)
                    if img.size[0] < 300 or img.size[1] < 300:
                        os.remove('./ori_image/' + keywords + '/' + str(i) + '.' + content_type)
            return 
        except Exception as e:
            return None
