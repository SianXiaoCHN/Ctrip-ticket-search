import datetime
import json

import requests
from prettytable import PrettyTable

with open('Domestic Airports.json', 'r', encoding='utf-8') as f:
    city = json.load(f)


def flyapi(dcity: str, acity: str, date: str):
    date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Content-Type": "application/json",  # 声明文本类型为 json 格式,
        'Cookie': '_ga=GA1.2.1422723313.1585102199; _abtest_userid=1c296dde-d639-424f-a007-cad9975fd8d5; _gac_UA-3748357-1=1.1585220211.Cj0KCQjwpfHzBRCiARIsAHHzyZooiSyIMjmJ_FcCpRlSJuF8h1guzQ2LWkDVHs9kewmqkaawfORabUwaAtx5EALw_wcB; _RSG=Hv4Xpi9jTt51tuATq36Hm8; _RDG=28329d014ec74124741c6df88a04cc43e6; _RGUID=5dddb49b-3384-4e51-8c11-183d1d2b8dc1; _gcl_aw=GCL.1585220214.Cj0KCQjwpfHzBRCiARIsAHHzyZooiSyIMjmJ_FcCpRlSJuF8h1guzQ2LWkDVHs9kewmqkaawfORabUwaAtx5EALw_wcB; _gcl_dc=GCL.1585220214.Cj0KCQjwpfHzBRCiARIsAHHzyZooiSyIMjmJ_FcCpRlSJuF8h1guzQ2LWkDVHs9kewmqkaawfORabUwaAtx5EALw_wcB; MKT_CKID=1585220215050.q49s4.k99w; GUID=09031038111353360416; _abtest_userid=19bf1f22-d393-4415-a4c6-66ef5a7a952d; _RF1=163.125.73.52; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&createtime=1589199056&Expires=1589803855549; MKT_CKID_LMT=1589199055579; _gid=GA1.2.1657496412.1589199056; MKT_Pagesource=PC; FD_SearchHistorty={"type":"S","data":"S%24%u5929%u6D25%28TSN%29%24TSN%242020-05-11%24%u6DF1%u5733%28SZX%29%24SZX%24%24%24"}; _gat=1; _jzqco=%7C%7C%7C%7C%7C1.1408634404.1585220215042.1589199055588.1589199119649.1589199055588.1589199119649.0.0.0.9.9; __zpspc=9.4.1589199055.1589199119.2%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _bfa=1.1585102198351.9o303i.1.1586776655945.1589199052742.5.13.214073; _bfs=1.4; _bfi=p1%3D10320673302%26p2%3D10320673302%26v1%3D13%26v2%3D12'}

    global city

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
    try:
        routeList = json.loads(response)["data"].get('routeList')
    except KeyError:
        print("\n=========未查询到航班数据！============")
        return
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
