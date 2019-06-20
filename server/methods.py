import datetime, json


def timestamp():
    template = '%FT%T+00:00'
    stamp = datetime.datetime.utcnow()
    return json.dumps({"datetime": stamp.strftime(template)})


if __name__ == '__main__':
    print(timestamp())
