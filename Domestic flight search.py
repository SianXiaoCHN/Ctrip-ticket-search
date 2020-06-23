import datetime
import json

import requests
from prettytable import PrettyTable


def flyapi(dcity: str, acity: str, date: str):
    date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Content-Type": "application/json",  # 声明文本类型为 json 格式,
        'Cookie': '_ga=GA1.2.1422723313.1585102199; _abtest_userid=1c296dde-d639-424f-a007-cad9975fd8d5; _gac_UA-3748357-1=1.1585220211.Cj0KCQjwpfHzBRCiARIsAHHzyZooiSyIMjmJ_FcCpRlSJuF8h1guzQ2LWkDVHs9kewmqkaawfORabUwaAtx5EALw_wcB; _RSG=Hv4Xpi9jTt51tuATq36Hm8; _RDG=28329d014ec74124741c6df88a04cc43e6; _RGUID=5dddb49b-3384-4e51-8c11-183d1d2b8dc1; _gcl_aw=GCL.1585220214.Cj0KCQjwpfHzBRCiARIsAHHzyZooiSyIMjmJ_FcCpRlSJuF8h1guzQ2LWkDVHs9kewmqkaawfORabUwaAtx5EALw_wcB; _gcl_dc=GCL.1585220214.Cj0KCQjwpfHzBRCiARIsAHHzyZooiSyIMjmJ_FcCpRlSJuF8h1guzQ2LWkDVHs9kewmqkaawfORabUwaAtx5EALw_wcB; MKT_CKID=1585220215050.q49s4.k99w; GUID=09031038111353360416; _abtest_userid=19bf1f22-d393-4415-a4c6-66ef5a7a952d; _RF1=163.125.73.52; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&createtime=1589199056&Expires=1589803855549; MKT_CKID_LMT=1589199055579; _gid=GA1.2.1657496412.1589199056; MKT_Pagesource=PC; FD_SearchHistorty={"type":"S","data":"S%24%u5929%u6D25%28TSN%29%24TSN%242020-05-11%24%u6DF1%u5733%28SZX%29%24SZX%24%24%24"}; _gat=1; _jzqco=%7C%7C%7C%7C%7C1.1408634404.1585220215042.1589199055588.1589199119649.1589199055588.1589199119649.0.0.0.9.9; __zpspc=9.4.1589199055.1589199119.2%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _bfa=1.1585102198351.9o303i.1.1586776655945.1589199052742.5.13.214073; _bfs=1.4; _bfi=p1%3D10320673302%26p2%3D10320673302%26v1%3D13%26v2%3D12'}

    city = {'阿尔山': 'YIE', '阿克苏': 'AKU', '阿拉善右旗': 'RHT', '阿拉善左旗': 'AXF', '阿勒泰': 'AAT', '阿里': 'NGQ', '澳门': 'MFM',
            '安庆': 'AQG', '安顺': 'AVA', '鞍山': 'AOG', '巴彦淖尔': 'RLK', '百色': 'AEB', '包头': 'BAV', '保山': 'BSD', '北海': 'BHY',
            '北京': 'BJS', '白城': 'DBC', '白山': 'NBS', '毕节': 'BFJ', '博乐': 'BPL', '重庆': 'CKG', '昌都': 'BPX', '常德': 'CGD',
            '常州': 'CZX', '朝阳': 'CHG', '成都': 'CTU', '池州': 'JUH', '赤峰': 'CIF', '揭阳': 'SWA', '长春': 'CGQ', '长沙': 'CSX',
            '长治': 'CIH', '承德': 'CDE', '沧源': 'CWJ', '达县': 'DAX', '大理': 'DLU', '大连': 'DLC', '大庆': 'DQA', '大同': 'DAT',
            '丹东': 'DDG', '稻城': 'DCY', '东营': 'DOY', '敦煌': 'DNH', '芒市': 'LUM', '额济纳旗': 'EJN', '鄂尔多斯': 'DSN', '恩施': 'ENH',
            '二连浩特': 'ERL', '佛山': 'FUO', '福州': 'FOC', '抚远': 'FYJ', '阜阳': 'FUG', '赣州': 'KOW', '格尔木': 'GOQ', '固原': 'GYU',
            '广元': 'GYS', '广州': 'CAN', '贵阳': 'KWE', '桂林': 'KWL', '哈尔滨': 'HRB', '哈密': 'HMI', '海口': 'HAK', '海拉尔': 'HLD',
            '邯郸': 'HDG', '汉中': 'HZG', '杭州': 'HGH', '合肥': 'HFE', '和田': 'HTN', '黑河': 'HEK', '呼和浩特': 'HET', '淮安': 'HIA',
            '怀化': 'HJJ', '黄山': 'TXN', '惠州': 'HUZ', '鸡西': 'JXA', '济南': 'TNA', '济宁': 'JNG', '加格达奇': 'JGD', '佳木斯': 'JMU',
            '嘉峪关': 'JGN', '金昌': 'JIC', '金门': 'KNH', '锦州': 'JNZ', '嘉义': 'CYI', '西双版纳': 'JHG', '建三江': 'JSJ', '晋江': 'JJN',
            '井冈山': 'JGS', '景德镇': 'JDZ', '九江': 'JIU', '九寨沟': 'JZH', '喀什': 'KHG', '凯里': 'KJH', '康定': 'KGT', '克拉玛依': 'KRY',
            '库车': 'KCA', '库尔勒': 'KRL', '昆明': 'KMG', '拉萨': 'LXA', '兰州': 'LHW', '黎平': 'HZH', '丽江': 'LJG', '荔波': 'LLB',
            '连云港': 'LYG', '六盘水': 'LPF', '临汾': 'LFQ', '林芝': 'LZY', '临沧': 'LNJ', '临沂': 'LYI', '柳州': 'LZH', '泸州': 'LZO',
            '洛阳': 'LYA', '吕梁': 'LLV', '澜沧': 'JMJ', '龙岩': 'LCX', '满洲里': 'NZH', '梅州': 'MXZ', '绵阳': 'MIG', '漠河': 'OHE',
            '牡丹江': 'MDG', '马祖': 'MFK', '南昌': 'KHN', '南充': 'NAO', '南京': 'NKG', '南宁': 'NNG', '南通': 'NTG', '南阳': 'NNY',
            '宁波': 'NGB', '宁蒗': 'NLH', '攀枝花': 'PZI', '普洱': 'SYM', '齐齐哈尔': 'NDG', '黔江': 'JIQ', '且末': 'IQM', '秦皇岛': 'BPE',
            '青岛': 'TAO', '庆阳': 'IQN', '衢州': 'JUZ', '日喀则': 'RKZ', '日照': 'RIZ', '三亚': 'SYX', '厦门': 'XMN', '上海': 'SHA',
            '深圳': 'SZX', '神农架': 'HPG', '沈阳': 'SHE', '石家庄': 'SJW', '塔城': 'TCG', '台州': 'HYN', '太原': 'TYN', '扬州': 'YTY',
            '唐山': 'TVS', '腾冲': 'TCZ', '天津': 'TSN', '天水': 'THQ', '通辽': 'TGO', '铜仁': 'TEN', '吐鲁番': 'TLQ', '万州': 'WXN',
            '威海': 'WEH', '潍坊': 'WEF', '温州': 'WNZ', '文山': 'WNH', '乌海': 'WUA', '乌兰浩特': 'HLH', '乌鲁木齐': 'URC', '无锡': 'WUX',
            '梧州': 'WUZ', '武汉': 'WUH', '武夷山': 'WUS', '西安': 'SIA', '西昌': 'XIC', '西宁': 'XNN', '锡林浩特': 'XIL',
            '香格里拉(迪庆)': 'DIG', '襄阳': 'XFN', '兴义': 'ACX', '徐州': 'XUZ', '香港': 'HKG', '烟台': 'YNT', '延安': 'ENY',
            '延吉': 'YNJ', '盐城': 'YNZ', '伊春': 'LDS', '伊宁': 'YIN', '宜宾': 'YBP', '宜昌': 'YIH', '宜春': 'YIC', '义乌': 'YIW', '银川': 'INC', '永州': 'LLF',
            '榆林': 'UYN', '玉树': 'YUS', '运城': 'YCU', '湛江': 'ZHA', '张家界': 'DYG', '张家口': 'ZQZ', '张掖': 'YZY', '昭通': 'ZAT', '郑州': 'CGO',
            '中卫': 'ZHY', '舟山': 'HSN', '珠海': 'ZUH', '遵义(茅台)': 'WMT', '遵义(新舟)': 'ZYI'}

    dcity_code = city.get(dcity, None)
    acity_code = city.get(acity, None)
    if dcity_code is None:
        print("\n=========未查询到出发城市机场！============")
        return
    if dcity_code is None:
        print("\n=========未查询到目的城市机场！============")
        return

    url = 'https://flights.ctrip.com/itinerary/api/12808/products'
    request_payload = {"flightWay": "Oneway",
                       "army": "false",
                       "classType": "ALL",
                       "hasChild": 'false',
                       "hasBaby": 'false',
                       "searchIndex": 1,
                       "token": "c91cf603fd7191a9c762fcc27b4cbf29",
                       "airportParams": [{"dcity": dcity_code, "acity": acity_code, "dcityname": dcity, "acityname": acity, "date": date}]}

    # 这里传进去的参数必须为 json 格式
    response = requests.post(url, data=json.dumps(
        request_payload), headers=headers).text
    # 获取json文件
    routeList = json.loads(response)["data"].get('routeList')
    # 建立表格输出数据
    table = PrettyTable(["航空公司", "航班", "机型", "起飞时间-->到达时间", "准点率", "最低价格"])
    table.padding_width = 1
    # 无航班
    if routeList is None:
        print("\n=========未查询到航班数据！============")
        return
    for route in routeList:
        if len(route.get('legs')) == 1:
            info = {}
            # 可对应json文件寻找所需信息
            legs = route.get('legs')[0]
            flight = legs.get('flight')
            # 航空公司
            if flight.get("sharedFlightNumber") is not None and flight.get("sharedFlightNumber").strip() != '':
                info['Airline'] = flight.get('airlineName') + "(共享)"
            else:
                info['Airline'] = flight.get('airlineName')
            # 航班号
            info['FlightNumber'] = flight.get('flightNumber')
            # 机型
            info['CraftType'] = flight.get('craftTypeName')
            # 飞行时间
            info['Date'] = flight.get(
                'departureDate')[-8:-3] + "-->" + flight.get('arrivalDate')[-8:-3]
            # 准点率
            info['PunctualityRate'] = flight.get('punctualityRate')
            # 最低价格
            info['Price'] = legs.get('characteristic').get('lowestPrice')
            table.add_row(list(info.values()))
    print(dcity, '------->', acity, date)
    print(table)


def proc1():
    while True:
        dcity = input('请输入起点（北京）： ')
        acity = input('请输入终点（上海）： ')
        date1 = input('请输入起始日期（20200202）： ')
        date2 = input('请输入结束日期（20200204）： ')
        # dcity = '天津'
        # acity = '深圳'
        # date = '20190928'

        begin = datetime.date(int(date1[0:4]), int(
            date1[4:6]), int(date1[6:8]))
        end = datetime.date(int(date2[0:4]), int(date2[4:6]), int(date2[6:8]))
        for i in range((end - begin).days+1):
            day = begin + datetime.timedelta(days=i)
            flyapi(dcity, acity, day.isoformat().replace('-', ''))


def proc2():
    while True:
        dcity = input('请输入起点（北京）： ')
        acity = input('请输入终点（上海）： ')
        date1 = input('请输入去程日期（20200202）： ')
        date2 = input('请输入返程日期（20200204）： ')
        # dcity = '天津'
        # acity = '深圳'
        # date = '20190928'
        flyapi(dcity, acity, date1)
        flyapi(acity, dcity, date2)


if __name__ == "__main__":
    print('1: 一段时间内单程票价')
    print('2: 往返两日票价')
    eval('proc'+input('请输入需求：')+'()')
