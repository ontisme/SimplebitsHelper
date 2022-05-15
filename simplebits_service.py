import requests


class SimpleBitsHelper():
    def __init__(self, _cookie):
        self.host = "https://simplebits.io/"
        self.ses = requests.session()
        self.cookie = _cookie
        self.headers = {
            'cookie': f'{self.cookie}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39'
        }

    # 取得用戶資訊
    def get_user(self):
        try:
            url = self.host + "api/user"
            ret = self.ses.get(url, headers=self.headers)
            if ret:
                return ret.json()['data']
            else:
                return None
        except:
            return None

    # 取得短連結所有網址
    def get_shortlinks(self):
        try:
            url = self.host + "api/pages/shortlinks"
            ret = self.ses.get(url, headers=self.headers)
            if ret:
                return ret.json()
            else:
                return None
        except:
            return None

    # 取得有效的短連結網址
    def get_valid_shortlinks(self):
        try:
            shortlinks = self.get_shortlinks()
            # 取出 shortlinks completed < max_claims 的項目
            valid_shortlinks = [
                shortlink for shortlink in shortlinks if shortlink['completed'] < shortlink['max_claims']
            ]
            return valid_shortlinks
        except:
            return None


    # 生成短網址
    def generate_shortlink(self, id):
        try:
            url = self.host + "api/shortlinks/generate"
            data = {
                'short_id': id
            }
            ret = self.ses.post(url, headers=self.headers, json=data)
            if ret:
                return ret.json()
            else:
                return None
        except:
            return None

    # 生成所有短網址
    def generate_shortlink_all(self):
        try:
            link_arr = []
            valid_shortlinks = self.get_valid_shortlinks()
            for shortlink in valid_shortlinks:
                ret = self.generate_shortlink(shortlink['id'])
                link_arr.append(str(ret).replace(" ","").replace('\n',"").replace('\r',"").replace('\t',""))

            if len(link_arr) > 0:
                return link_arr
        except:
            return None


    # 取得PTC網址
    def get_ptc_link(self):
        try:
            url = self.host + "api/pages/ptc"
            ret = self.ses.get(url, headers=self.headers)
            if ret:
                return ret.json()
            else:
                return None
        except:
            return None

    def get_valid_ptc_link(self):
        try:
            ptc_link = self.get_ptc_link()
            links = []
            # 從 ptc_link 取得 status 為 Incomplete 的項目
            for link in ptc_link:
                if link['status'] == 'Incomplete':
                    links.append(link["ad_link"])
            return links
        except:
            return None

    def generate_ptc_adid(self, adid):
        try:
            url = self.host + "api/ptc/"
            data = {
                'ad_id': adid
            }
            ret = self.ses.post(url, headers=self.headers, json=data)
            if ret:
                return ret.json()
            else:
                return None
        except:
            return None


if __name__ == '__main__':
    a = SimpleBitsHelper('_cookie')
