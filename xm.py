import random
import json
import requests
import time
import datetime


def s():
    # 获取时间戳
    c = time.time()
    s = int(round(c * 1000))
    s = str(s)
    return s


def d(user, password):
    # 获取登录access
    url = "https://api-user.huami.com/registrations/+86" + user + "/tokens"
    host = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": "MiFit/4.10.0 (iPhone; iOS 14.4; Scale/3.00)",
        "callid": s(),
    }
    biao = {
        "client_id": "HuaMi",

        "password": password,

        "redirect_uri": "https://s3-us-west-2.amazonaws.com/hm-registration/successsignin.html",

        "token": "access",

    }
    fc = requests.post(url=url, headers=host, data=biao, allow_redirects=False)
    fx = fc.headers["Location"]
    access = fx[99:120]
    if access == "-1":   
        print("账号或密码错误")
        return "false"
    else:
        print( "登陆成功")
        # print(access)
        return access


def f(access):
    # 登录access返回token,id
    url = "https://account.huami.com/v2/client/login"

    host = {"User-Agent": "MiFit/4.10.0 (iPhone; iOS 14.4; Scale/3.00)"}

    biao = {
        "allow_registration": "false",
        "app_name": "com.xiaomi.hm.health",
        "app_version": "4.10.0",  # 小运动版本
        "code": access,  # 登录返回code
        "country_code": "CN",
        "device_id": "73681DC0-3B18-4252",
        "device_id_type": "uuid",
        "device_model": "phone",
        "grant_type": "access_token",
        "lang": "zh_CN",
        "os_version": "1.5.0",
        "source": "com.xiaomi.hm.health",
        "third_name": "huami_phone",
    }

    fh = requests.post(url, biao, host)

    fh = fh.json()
    token_info = fh["token_info"]

    app_token = token_info["app_token"]

    user_id = token_info["user_id"]

    return app_token, user_id


def bushu(app_token, user_id, bs):
    # 刷步数
    urls = "https://api-mifit-cn2.huami.com/v1/data/band_data.json?"

    s = int(time.time())

    hosts = {
        "User-Agent": "MiFit/4.10.0 (iPhone; iOS 14.4; Scale/3.00)",
        "apptoken": app_token,
    }

    sj = time.strftime("%Y-%m-%d", time.localtime())

    data_json = open("json.txt", "r")

    data = data_json.read()

    datas = data % (bs, sj)

    data_json.close()

    biaos = {
        "data_json": datas,
        "device_type": "2",
        "last_deviceid": "-1",
        "last_source": "7",
        "last_sync_data_time": s,
        "userid": user_id,
    }

    ss = requests.post(url=urls, headers=hosts, data=biaos)

    ss = ss.json()
    print(ss)


def mainc(client):
    print("小米运动刷步数同步到微信/支付宝")
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
    expireDate = client["expire"].strip()
    user = client["user"]
    if (len(expireDate) != 0) and (expireDate < nowDate):
        print("user"+user[7:]+"expired")
        return
    password = client["password"]
    bs = client["bs"]
    bs = random.randint(bs, bs+2000)

    access = d(user, password)
    if access == "false":
        print("账号或密码错误")
    else:
        cbc = f(access)
        app_token = cbc[0]
        user_id = cbc[1]
        bushu(app_token, user_id, bs)

clients=''
try:
    with open('./config.json','r') as fp:
        clients = json.load(fp)
except Exception as e:
        print(str(e))
for client in clients:
    mainc(client)
