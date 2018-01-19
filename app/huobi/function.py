import time,json


def timestampToDate(timestamp, combine):
    timestamp = int(timestamp)
    if combine:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp))
    else:
        return {'date': time.strftime("%Y-%m-%d", time.gmtime(timestamp)),
                'time': time.strftime("%H:%M:%S", time.gmtime(timestamp))}

def subscript(ws,cp,type='ticker'):
    if type == 'ticker':
        text = {"sub": "market.{}.detail".format(cp),"id": "id10"}
    elif type == 'trader':
        text = {"sub": "market.{}.depth.step0".format(cp), "id": "id10"}
    ws.send(json.dumps(text))
    #print(json.dumps(text))  # TickerEvent