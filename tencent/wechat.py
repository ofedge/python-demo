import requests, time, re, xml.dom.minidom, random, json, gzip, sys

def get_code(text):
    text = text.replace(' ', '')
    return re.findall(r'code=(\d+)', text)[0]


def get_uuid(text):
    text = text.replace(' ', '')
    return re.findall(r'uuid="(.+?)"', text)[0]


def get_avatar(text):
    text = text.replace(' ', '')
    return re.findall(r'userAvatar=\'(.+?)\'', text)[0]


def get_redirect_uri(text):
    text = text.replace(' ', '')
    return re.findall(r'redirect_uri="(.+?)"', text)[0]


def get_unix_time():
    return str(int(time.time() * 1000))


def get_device_id():
    return 'e' + str(random.randint(100000000000000,999999999999999))


def get_sync_key(L):
    sync_key = ''
    for i in range(len(L)):
        sync_key += '|' + str(L[i]['Key']) + '_' + str(L[i]['Val'])
    return sync_key[1:]


def get_sync_result(text):
    text = text.replace(' ', '')
    retcode = re.findall(r'retcode:"(\d+)"', text)[0]
    selector = re.findall(r'selector:"(\d+)"', text)[0]
    return retcode, selector
    


# 验证证书
cert_verify = True
# 响应码对应状态 
CODE_STATUS = {
    '200': 'OK',
    '201': '认证中',
    '408': '超时'
}


# 开始执行
def weixin():
    with requests.Session() as s:
        # 请求头
        s.headers.update({
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'DNT': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Host': 'wx.qq.com'
        })
        # 访问下首页
        s.get('https://wx.qq.com', headers={'Upgrade-Insecure-Requests': '1'}, verify=cert_verify)
        print('首页访问成功\n')
        s.headers.update({
            'Accept': '*/*',
            'Host': 'login.wx.qq.com',
            'Referer': 'https://wx.qq.com/',
        })
        jslogin_param = {
            'appid': 'wx782c26e4c19acffb',
            'redirect_uri': 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage',
            'fun': 'new',
            'lang': 'zh_CN',
            '_': get_unix_time()
        }
        # 获取uuid
        jslreq = s.get('https://login.wx.qq.com/jslogin', params=jslogin_param, verify=cert_verify)
        code = get_code(jslreq.text)
        uuid = get_uuid(jslreq.text)
        print('响应: ' + str(code) + '(' + CODE_STATUS[code] + '), uuid: ' + uuid + '\n')
        s.headers.update({
            'Accept': 'image/webp,image/*,*/*;q=0.8',
            'Host': 'pingtas.qq.com',
            'Referer': 'https://wx.qq.com/'
        })
        
        pingd_param = {
            'dm': 'wx.qq.com',
            'pvi': s.cookies.get('pgv_pvi'),
            'si': s.cookies.get('pgv_si'),
            'url': '/',
            'arg': '',
            'ty': '1',
            'rdm': 'wx.qq.com',
            'rurl': '/',
            'rarg': '',
            'adt': '',
            'r2': '43209744',
            'r3': '-1',
            'r4': '1',
            'fl': '23.0',
            'src': '1920x1080',
            'scl': '24-bit',
            'lg': 'zh-cn',
            'jv': '',
            'tz': '-8',
            'ct': '',
            'ext': 'adid=',
            'pf': '',
            'random': get_unix_time()
        }
        # 什么也不做
        s.get('https://pingtas.qq.com/pingd', params=pingd_param, verify=cert_verify)
        get_ptqr(s, uuid)


# 获取验证码
def get_ptqr(s, uuid):
    print('---------------开始获取验证码--------------------\n')
    ptqr_header = {
        'Accept':'image/webp,image/*,*/*;q=0.8',
        'Host': 'login.weixin.qq.com'
    }
    ptqr_req = s.get('https://login.weixin.qq.com/qrcode/' + uuid, headers=ptqr_header, verify=cert_verify)
    with open('ptqr.png', 'wb') as f:
        for chunk in ptqr_req.iter_content(128):
            f.write(chunk)
    print('-------------------验证码获取成功---------------------\n')
    do_login(s, uuid)


# 检测登录
def do_login(s, uuid):
    print('-------------------开始检测登录------------------------\n')
    login_header = {
        'Accept': '*/*',
        'Host': 'login.wx.qq.com'
    }
    login_param = {
        'loginicon': 'true',
        'uuid': uuid,
        'tip': '1',
        'r': '-172443120',
        '_': get_unix_time()
    }
    i = 0
    while i <= 10:
        print('第' + str(i + 1) + '次获取登录状态\n')
        if i > 0:
            login_param['tip'] = '0'
            login_param['_'] = str(int(time.time()*1000))
            login_param['r'] = '???'
        login_req = s.get('https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login', params=login_param, headers=login_header, verify=cert_verify)
        login_code = get_code(login_req.text)
        print('登录状态码: ' + login_code + '(' + CODE_STATUS[login_code] + ')\n')
        if '201' == login_code:
            # 获取用户头像
            '''
            avatar = get_avatar(login_req.text)
            with open('avatar.html', 'w') as f:
                f.write('<img src="' + avatar + '">')
            print('用户头像获取成功, 保存在avatar.html\n')
            '''
        if '200' == login_code:
            redirect_uri = get_redirect_uri(login_req.text)
            print('登录成功\n')
            wx_init(s, redirect_uri)
            break
        i += 1
    print('----------------------检测登录结束--------------\n')


# 处理登录成功后初始化微信
def wx_init(s, url):
    print('------------------初始化微信信息---------------------\n')
    s.headers.update({
        'Accept': 'application/json, text/plain, */*',
        'Host': 'wx.qq.com',
        'Referer': 'https://wx.qq.com/'
    })
    init_res = s.get(url + '&fun=new&version=v2', verify=cert_verify)
    res_xml = xml.dom.minidom.parseString(init_res.text)
    # 存放公用变量
    common_param = {}
    dom_error = res_xml.getElementsByTagName('error')[0]
    common_param['skey'] = dom_error.getElementsByTagName('skey')[0].childNodes[0].data
    common_param['wxsid'] = dom_error.getElementsByTagName('wxsid')[0].childNodes[0].data
    common_param['wxuin'] = dom_error.getElementsByTagName('wxuin')[0].childNodes[0].data
    common_param['pass_ticket'] = dom_error.getElementsByTagName('pass_ticket')[0].childNodes[0].data
    # 初始化
    post_body = {
        'BaseRequest': {
            'Uin': common_param['wxuin'],
            'Sid': common_param['wxsid'],
            'Skey': common_param['skey'],
            'DeviceID': get_device_id()
        }
    }
    init_param = {
        'r': get_unix_time(),
        'pass_ticket': common_param['pass_ticket']
    }
    init_res = s.post('https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit', params=init_param, data=json.dumps(post_body), verify=True)
    common_param['sync_key_dict'] = eval(init_res.text)['SyncKey']
    common_param['sync_key'] = get_sync_key(common_param['sync_key_dict']['List'])
    common_param['current_user'] = eval(init_res.content)['User']
    print('-----------------初始化微信信息结束-------------------\n')
    status_notify(s, common_param)


# 开启状态通知, 获取好友列表
def status_notify(s, common_param):
    print('-------------开启状态通知, 获取好友列表----------------\n')
    # body json
    post_body = {
        'BaseRequest':{
            'Uin': common_param['wxuin'],
            'Sid': common_param['wxsid'],
            'Skey': common_param['skey'],
            'DeviceID': get_device_id()
        },
        'Code':3,
        'FromUser': common_param['current_user']['UserName'],
        'ClientMsgId': get_unix_time(),
        'ToUserName': common_param['current_user']['UserName'],
    }
    sn_param = {'pass_ticket': common_param['pass_ticket']}
    sn_res = s.post('https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxstatusnotify', params=sn_param, data=json.dumps(post_body), verify=True)
    print('状态通知结果:', sn_res.text, '\n')
    print('开始获取好友列表\n')
    gc_param = {
        'pass_ticket': common_param['pass_ticket'],
        'r': get_unix_time(),
        'seq': '0',
        'skey': common_param['skey']
    }
    gc_res = s.get('https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact', params=gc_param, verify=True)
    # 开始筛选好友
    contacts = eval(gc_res.content)['MemberList']
    contacts_dict={}
    for i in range(len(contacts)):
        contact = contacts[i]
        # 个人帐号
        if contact['VerifyFlag'] == 0:
            if '@@' in contact['UserName']:
                contacts_dict[contact['UserName']] = {
                    'NickName': contact['NickName'],
                    'class': '群聊'
                }
            elif '@' not in contact['UserName']:
                contacts_dict[contact['UserName']] = {
                    'NickName': contact['NickName'],
                    'class': '服务号'
                }
            else:
                contacts_dict[contact['UserName']] = {
                    'NickName': contact['NickName'],
                    'class': '好友'
                }
        else:
            contacts_dict[contact['UserName']] = {
                'NickName': contact['NickName'],
                'class': '订阅号'
            }
    contacts_dict[common_param['current_user']['UserName']] = {'NickName':common_param['current_user']['NickName'], 'class':'自己'}
    print('共', len(contacts_dict), '个好友, 包含订阅号\n')
    common_param['contacts'] = contacts_dict
    '''
    with open('contacts.log', 'wb') as f:
        for key in contacts_dict:
            f.write(b'UserName: ')
            f.write(key.encode())
            f.write(b', NickName: ')
            f.write(contacts_dict[key]['NickName'].encode())
            f.write(b', class: ')
            f.write(contacts_dict[key]['class'].encode())
            f.write(b'\n')
    '''
    print('---------------- 好友列表获取结束---------------------\n')
    sync_check(s, common_param)

    
# 检测消息
def sync_check(s, common_param):
    print('----------------开始检查消息---------------\n')
    n = 0
    while True:
        n += 1
        sync_check_param = {
            'r': get_unix_time(),
            'skey': common_param['skey'],
            'sid': common_param['wxsid'],
            'uin': common_param['wxuin'],
            'deviceid': get_device_id(),
            'synckey': common_param['sync_key'],
            '_': get_unix_time()
        }
        s.headers.update({
            'Accept': '*/*',
            'Host': 'webpush.wx.qq.com'
        })
        sync_check_res = s.get('https://webpush.wx.qq.com/cgi-bin/mmwebwx-bin/synccheck', params=sync_check_param, verify=True)
        retcode, selector = get_sync_result(sync_check_res.text)
        print('第', n , '次检查结果, retcode:', retcode, ', selector:', selector, '\n')
        if retcode == '1101':
            print('你已在其他地方登录微信, bye!\n')
            break
        if selector != '0':
            print('selector:', selector, ', 开始获取消息\n')
            sync_param = {
                'sid': common_param['wxsid'],
                'skey': common_param['skey'],
                'pass_ticket': common_param['pass_ticket']
            }
            s.headers.update({
                'Accept': 'application/json, text/plain, */*',
                'Host': 'wx.qq.com',
                'Origin': 'https://wx.qq.com'
            })
            post_body = {
                'BaseRequest':{
                    'Uin': common_param['wxuin'],
                    'Sid': common_param['wxsid'],
                    'Skey': common_param['skey'],
                    'DeviceID': get_device_id()
                },
                'SyncKey': common_param['sync_key_dict'],
                'rr': get_unix_time()
            }
            sync_res = s.post('https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsync', params=sync_param, data=json.dumps(post_body), verify=True)
            message_res = eval(sync_res.content)
            if message_res['AddMsgCount'] > 0:
                for i in range(message_res['AddMsgCount']):
                    msg = message_res['AddMsgList'][i]
                    handle_msg(msg, common_param)
            common_param['sync_key_dict'] = message_res['SyncKey']
            common_param['sync_key'] = get_sync_key(common_param['sync_key_dict']['List'])
        time.sleep(1)
    print('-------------------检查消息结束-----------------------\n')


def handle_msg(msg, common_param):
    msg_type = msg['MsgType']
    try:
        print('***** Msg Type: ' + str(msg_type) + ', 来自: ' + str(common_param['contacts'].get(msg['FromUserName'],'')) + '(' + msg['FromUserName'] + ')*****\n')
    except Exception as err:
        print(err)
        print('***** Msg Type: ' + str(msg_type) + ', 来自: ' + msg['FromUserName'] + '(此人名字有乱码)*****\n')
    if msg_type == 51:
        print('接收到聊天窗口通知\n')
        print(msg['Content'], '\n')
    elif msg_type == 1:
        print('接收到文本消息\n')
        try:
            print(msg['Content'], '\n')
        except Exception as err:
            print('不支持的消息类型, 请在手机上查看\n')
    elif msg_type == 3:
        print('接收到图片消息, 请在手机上查看\n')
        print(msg['Content'], '\n')
    elif msg_type == 47:
        print('接收到表情, 请在手机上查看\n')
    elif msg_type == 49:
        print('接收到订阅号消息, 请在手机上查看\n')
    elif msg_type == 10000:
        print('接收到红包, 请在手机上查看\n')
    else:
        print('未知\n')
        try:
            print(msg, '\n')
        except Exception as err:
            print('打印不出来\n')


if __name__ == '__main__':
    weixin()
