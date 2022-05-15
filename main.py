import json
import time

from pywebio import start_server, config
from pywebio.input import *
from pywebio.output import *
from pywebio.platform.tornado import start_server
import simplebits_service


# 讀取 Config
def load_config():
    with open('config.json') as f:
        data = json.load(f)
    return data

@config(theme="dark")
def main():
    app = simplebits_service.SimpleBitsHelper(user_config)
    user_data = app.get_user()
    put_markdown(f"`操作帳號：{user_data['user']['username']}　LV：{user_data['stats']['level']} [{user_data['stats']['current_exp']}/{user_data['stats']['next_exp']}]`")
    put_markdown(f"`當前綠電：[{user_data['stats']['energy']}/{user_data['stats']['max_energy']}]`")
    put_markdown(f"`當前紫電：[{user_data['stats']['dom']}/{user_data['stats']['max_dom']}]`")

    # PTC
    r = app.get_valid_ptc_link()
    put_markdown(f"# 有 {len(r)} 個可點的PTC連結")
    urls = []
    for i in r:
        urls.append([f"[{i}]"])
    put_table(header=['Link'], tdata=urls)

    # SHORTLINK
    r = app.generate_shortlink_all()
    put_markdown(f"# 有 {len(r)} 個可點的短連結")
    urls = []
    for i in r:
        urls.append([put_markdown(f"{i}")])
    put_table(header=['Link'], tdata=urls)





user_config = load_config()
start_server(main, debug=True, port=8080, host="0.0.0.0")

while(True):
    time.sleep(1)