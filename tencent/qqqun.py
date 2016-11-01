# /usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import random
import time
import sys


# 位图翻译(有人名字带表情)
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def login():
    # 随机小数
    random_string = random.uniform(0, 1)
    # 开启会话
    with requests.Session() as s:
        login_param = {
            'appid': '715030901',
            'daid': '73',
            'hide_close_icon': '1',
            'pt_no_auth': '1',
            's_url': 'http://qun.qq.com/member.html',
        }
        # 通用头信息
        s.headers.update({
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        })
        # 预登录header信息
        s.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Host': 'ui.ptlogin2.qq.com',
            'Referer': 'http://qun.qq.com/member.html'
        })
        # 预登录
        lreq = s.get('http://ui.ptlogin2.qq.com/cgi-bin/login', params=login_param, headers={'Upgrade-Insecure-Requests': '1'})
        # 获取验证码参数
        ptqr_param = {
            'appid': '715030901',
            'e': '2',
            'l': 'M',
            's': '3',
            'd': '72',
            'v': '4',
            't': random_string,
            'daid': '73'
        }
        # 获取验证码头
        s.headers.update({
            'Accept': 'image/webp,image/*,*/*;q=0.8',
            'Host': 'ptlogin2.qq.com',
            'Referer': 'http://ui.ptlogin2.qq.com/cgi-bin/login?appid=715030901&daid=73&hide_close_icon=1&pt_no_auth=1&s_url=http%3A%2F%2Fqun.qq.com%2Fmember.html'
        })
        # 获取验证码
        ptqr_req = s.get('http://ptlogin2.qq.com/ptqrshow', params=ptqr_param)
        # 二次获取验证码
        ptqr_req2 = s.get('http://ptlogin2.qq.com/ptqrshow', params=ptqr_param)
        # 保存至文件
        with open('ptqr.png', 'wb') as f:
            for chunk in ptqr_req2.iter_content(128):
                f.write(chunk)
        # 检查登录状态参数
        check_login_param = {
            'u1': 'http://qun.qq.com/member.html',
            'ptredirect': '1',
            'h': '1',
            't': '1',
            'g': '1',
            'from_ui': '1',
            'ptlang': '2052',
            'action': '0-0-1477380013232',
            'js_ver': '10178',
            'js_type': '1',
            'login_sig': s.cookies.get('pt_login_sig'),
            'pt_uistyle': '40',
            'aid': '715030901',
            'daid': '73',
        }
        # 检查登录头信息
        s.headers.update({
            'Accept': '*/*',
            'Host': 'ptlogin2.qq.com',
            'Referer': 'http://ui.ptlogin2.qq.com/cgi-bin/login?appid=715030901&daid=73&hide_close_icon=1&pt_no_auth=1&s_url=http%3A%2F%2Fqun.qq.com%2Fmember.html'
        })
        # 保存检查登录结果
        check_result = None
        # 检查登录
        while True:
            check_login_param['action'] = '0-0-' + str(int(time.time()*1000))
            clreq = s.get('http://ptlogin2.qq.com/ptqrlogin', params=check_login_param)
            check_result = eval(clreq.text.strip().replace(';',''))
            if check_result['expire']:
                print('二维码已过期, 请重新获取')
                break
            elif not check_result['expire'] and check_result['login']:
                print('登录成功, 欢迎: ' + check_result['user'])
                break;
            time.sleep(2)

        # 如果登录成功
        if check_result['login']:
            # checkSig, 获取登录信息 重定向
            s.headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Host': 'ptlogin4.qun.qq.com',
                'Referer': 'http://ui.ptlogin2.qq.com/cgi-bin/login?appid=715030901&daid=73&hide_close_icon=1&pt_no_auth=1&s_url=http%3A%2F%2Fqun.qq.com%2Fmember.html',
            })
            # checkSig, 设置cookies并且重定向至 http://qun.qq.com/member.html
            csreq = s.get(check_result['check_sig_url'], headers={'Upgrade-Insecure-Requests': '1'}, allow_redirects=False)
            print('检查sig, 响应码:', csreq.status_code, ', 重定向至:', csreq.headers.get('Location'))
            
            # pingd 参数
            pingd_param = {
                'dm': 'un.qq.com',
                'url': '/member.html',
                'rdm': 'ui.ptlogin2.qq.com',
                'rurl': '/cgi-bin/login',
                'rarg': 'appid=715030901&daid=73&hide_close_icon=1&pt_no_auth=1&s_url=http%3A%2F%2Fqun.qq.com%2Fmember.html',
                'pvid': s.cookies.get('pgv_pvid'),
                'scr': '1920x1080',
                'scl': '24-bit',
                'lang': 'zh-cn',
                'java': '0',
                'pf': 'Win32',
                'tz': '-8',
                'flash': '23.0 r0',
                'ct': '-',
                'column': '',
                'subject': '',
                'vs': 'tcss.3.1.5',
                'ext': 'tm=5;ch=2',
                'hurlcn': '',
                'rand': random.randint(10000, 99999),
                'reserved1': '-1',
                'tt': ''
            }
            s.headers.update({
                'Accept': 'image/webp,image/*,*/*;q=0.8',
                'Host': 'pingfore.qq.com',
                'Referer': 'http://qun.qq.com/member.html'
                
            })
            # 什么也不做
            pd_req = s.get('http://pingfore.qq.com/pingd', params=pingd_param, headers={'Proxy-Connection': 'keep-alive'})
            
            # 查询token
            query_token = getCSRFToken(s.cookies.get('skey'))
            
            # 用户选择如何操作
            while True:
                print('-------------------我是一条分割线---------------------')
                option = int(input('选择要进行的操作\n1.查看个人信息\n2.查询好友列表\n3.查询群列表\n4.退出\n'))
                if option == 1:
                    # 个人信息
                    jQueryCallback = 'jQuery1113023139232751655658_' + str(int(time.time()*1000))
                    exec('def ' + jQueryCallback + '(args):\n\treturn args')
                    my_info_param = {
                        'callback': jQueryCallback,
                        'ldw': query_token,
                        '_': str(int(time.time()*1000))
                    }
                    s.headers.update({
                        'Accept': '*/*',
                        'Host': 'cgi.find.qq.com'
                    })
                    mireq = s.get('http://cgi.find.qq.com/qqfind/myinfo', params=my_info_param, headers={'Proxy-Connection': 'keep-alive'})
                    info_result = eval(mireq.text.strip().replace(';', ''))
                    trans_my_info(info_result)
                    
                elif option == 2:
                    # 好友列表
                    friend_list_param = {'bkn': query_token}
                    s.headers.update({
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Host': 'qun.qq.com',
                    })
                    friend_list_header = {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Length': str(len(str(query_token)) + 4),
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    }
                    flreq = s.post('http://qun.qq.com/cgi-bin/qun_mgr/get_friend_list', data=friend_list_param, headers=friend_list_header)
                    trans_frient_list(flreq.text)
                    
                elif option == 3:
                    # 群列表
                    group_list_param = {'bkn': query_token}
                    s.headers.update({
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Host': 'qun.qq.com',
                    })
                    group_list_header = {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Length': str(len(str(query_token)) + 4),
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    }
                    glreq = s.post('http://qun.qq.com/cgi-bin/qun_mgr/get_group_list', data=group_list_param, headers=group_list_header)
                    group_list = trans_group_list(glreq.text)
                    # 如果有群, 就开始查看群成员
                    if len(group_list) > 0:
                        while True:
                            print('===================我是一条分割线=====================')
                            for i in range(len(group_list)):
                                print(i, ':', group_list[i]['gn'])
                            g_option = int(input('输入对应编号查询群成员:\n'))
                            if g_option < 0 or g_option > (len(group_list) - 1):
                                print('不在范围之内')
                                break
                            if group_list[g_option]:
                                
                                s.headers.update({
                                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                                    'Host': 'qun.qq.com',
                                })
                                group_mems_header = {
                                    'X-Requested-With': 'XMLHttpRequest',
                                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                                }
                                # 开始索引
                                start = 0
                                # 结束索引
                                end = 20
                                while True:
                                    print('start:', start, ',end:', end)
                                    group_mems_param = {
                                        'gc': group_list[g_option]['gc'],
                                        'st': start,
                                        'end': end,
                                        'sort': 0,
                                        'bkn': query_token
                                    }
                                    gmreq = s.post('http://qun.qq.com/cgi-bin/qun_mgr/search_group_members', data=group_mems_param, headers=group_mems_header)
                                    # 处理群成员显示
                                    count = trans_group_mems(gmreq.text)
                                    if end >= count:
                                        print('已达末尾')
                                        break
                                    c_option = int(input('输入0继续查看下20条, 输入1退出\n'))
                                    if 0 == c_option:
                                        start = end + 1
                                        end = start + 20
                                    else:
                                        break
                            else:
                                break
                                
                else:
                    print('bye!')
                    break






# 检查登录参数
def ptuiCB(*args):
    res = {'expire': False, 'login': False, 'check_sig_url': '', 'user': ''}
    if '66' == args[0] or '67' == args[0]:
        print(args[4])
    elif '65' == args[0]:
        res['expire'] = True
    elif '0' == args[0]:
        res['login'] = True
        res['check_sig_url'] = args[2]
        res['user'] = args[5]
    return res


# 获取查询token
def getCSRFToken(skey):
    if skey:
        r = 5381
        n = 0
        o = len(skey)
        while(len(skey) > n):
            r += (r<<5) + ord(skey[n]);
            n = n + 1
        return 2147483647&r


# 翻译个人信息
def trans_my_info(args):
    arg = eval(str(args).translate(non_bmp_map))['result']
    print('-------------------我是一条分割线---------------------')
    print('昵称:',arg['nick'], ', 性别:', {'male':'男','female':'女'}[arg['gender']])
    print('手机:', arg['phone'] + ', 电话:', arg['mobile'])
    print('血型:', ['','A','B','O','AB'][arg['blood']], ', 生肖',['','鼠','牛','虎','兔','龙','蛇','马','羊','猴','鸡','狗','猪'][arg['shengxiao']])
    print('个人说明:', arg['personal'])
    print('生日:', arg['birthday']['year'], '-', arg['birthday']['month'], '-', arg['birthday']['day'])
    print('所在地:', arg['country'], '-', arg['province'], '-', arg['city'])
    print('故乡:', arg['h_country'], '-', arg['h_province'] + '-', arg['h_city'])
    print('学校:', arg['college'], ', 主页:', arg['homepage'])
    print('登录坐标: (', arg['longitude'], ', ', arg['latitude'], ')')
    print('登录地址:', arg['lbs_addr_detail']['name'], ',' + arg['lbs_addr_detail']['town'], ',' + arg['lbs_addr_detail']['village'], ',' + arg['lbs_addr_detail']['street'])
    
# 翻译好友列表
def trans_frient_list(args):
    arg = eval(str(args).translate(non_bmp_map))['result']
    print('-------------------我是一条分割线---------------------')
    for key in arg.keys():
        print('组名称:', arg[key]['gname'])
        mems = arg[key]['mems']
        for i in range(len(mems)):
            print('\tQQ:', mems[i]['uin'], ', 备注:', mems[i]['name'])


# 翻译群列表, 返回一个群列表
def trans_group_list(args):
    arg = eval(str(args).translate(non_bmp_map))
    group_list = []
    print('-------------------我是一条分割线---------------------')
    print('我创建的')
    for c in range(len(arg['create'])):
        print('群号:', arg['create'][c]['gc'], ', 群名称:', arg['create'][c]['gn'], ', 创建者:', arg['create'][c]['owner'])
        group_list.append({'gc': arg['create'][c]['gc'], 'gn': arg['create'][c]['gn']})
    print('我管理的')
    for m in range(len(arg['manage'])):
        print('群号:', arg['manage'][m]['gc'], ', 群名称:', arg['manage'][m]['gn'], ', 创建者:', arg['manage'][m]['owner'])
        group_list.append({'gc': arg['manage'][m]['gc'], 'gn': arg['manage'][m]['gn']})
    print('我加入的')
    for j in range(len(arg['join'])):
        print('群号:', arg['join'][j]['gc'], ', 群名称:', arg['join'][j]['gn'], ', 创建者:', arg['join'][j]['owner'])
        group_list.append({'gc': arg['join'][j]['gc'], 'gn': arg['join'][j]['gn']})
    return group_list


# 翻译群成员, 返回成员总数
def trans_group_mems(args):
    arg = eval(str(args).translate(non_bmp_map))
    print('++++++++++++++++++我是一条分割线+++++++++++++++++++++++')
    levelname = arg.get('levelname', {})
    mems = arg['mems']
    print('群成员人数:', arg['count'], '/', arg['max_count'], ', 管理员人数:', arg['adm_num'], '/', arg['adm_max'])
    for i in range(len(mems)):
        print('昵称:', mems[i]['nick'], ', 群名片:', mems[i]['card'], ', QQ号:', mems[i]['uin'],
              ', 性别:', {0:'男', 1:'女', 255: '未知'}[mems[i]['g']], ', QQ龄:', mems[i]['qage'], ', 入群时间:', trans_time(mems[i]['join_time']),
              ', 最后发言:', trans_time(mems[i]['last_speak_time']), ', 等级(积分):', levelname.get(str(mems[i]['lv']['level']),''),
              '(', mems[i]['lv']['point'], '), 角色: ', ['创建者','管理员','成员'][mems[i]['role']])
    return arg['count']



# 时间戳翻译为时间
def trans_time(arg):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(arg)))


if __name__ == '__main__':
    login()
