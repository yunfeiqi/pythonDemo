import xlrd
import datetime
import time
import json

book = xlrd.open_workbook('/Users/mlamp/Library/Containers/com.tencent.WeWorkMac/Data/Library/Application Support/WXWork/Data/1688853915012790/Cache/File/2021-03/气味图书馆20210302.xlsx')
sheet1 = book.sheets()[0]
nrows = sheet1.nrows

map_id = {
    "乔艺":"wo0SfLCgAAX4WV1zDTneJWTQFwQiz09g",
    "张阳":"69a5d1a3a8724f01a93a7a897a5d2522",
    "李思科":"wm0SfLCgAAF_6BV5YCskMlm_J_p6Kemw",
    "王萌":"b29daf60e7f54a72852610f5630d2f22"
}

max_row = 236
max_col = 5
rows = [58,61,64,115,117,126,131,141,183,192,197,201,216,230,234,235]

with open('qwtsg-dl.json','w',encoding='utf-8') as f:
    for row_idx in rows:
        template = {
                        "app":"sfa",
                        "source": "workWeixin",
                        "dataType": "chatData",
                        "data": {
                            "roomid": "",
                            "content": [{
                                "uniqueId": "0",
                                "text": "我叫付骁弈，是明略科技的算法工程师,邮箱是 xumeng@mininglamp.com,手机号是15801333104工作地点在北京金汉王科技大厦",
                                "sendTime": 1547087894783,
                                "from": "f66935628eff7f9a2fd8ec42f01f5ff9",
                                "tolist": ["tangguangfa@mininglamp.com"]
                            }]
                        }
                    }
        for col_idx in range(1,max_col):
            cell_value = sheet1.cell(row_idx,col_idx).value
            if col_idx == 3:
                cell_value = xlrd.xldate_as_tuple(cell_value, book.datemode)
                date_value = datetime.date(*cell_value[:3])
                # date_format = date_value.strftime('%Y/%m/%d')
                t = date_value.timetuple()
                timeStamp = int(time.mktime(t))
                template["data"]["content"][0]["sendTime"] = timeStamp
            else:
                items = cell_value.split(":")
                value = "".join(items[1:])

                if col_idx == 4:
                    template["data"]["content"][0]["text"] = value
                if col_idx == 1:
                    template["data"]["content"][0]["from"] = map_id[value]
                if col_idx == 2:
                    template["data"]["content"][0]["tolist"] = [map_id[value]]

        
        f.write(json.dumps(template))


