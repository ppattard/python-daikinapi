import datetime


def _make_time(mins):
    return (datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0)) + datetime.timedelta(minutes=mins)).time()


def _make_mins(time):
    return time.hour * 60 + time.minute


class Schedule:
    def __init__(self):
        self.active = False
        self.powered = False
        self.time = _make_time(0)
        self.mode = None
        self.temp = None
        self.fan_rate = None

    def _set_from_device(self, data):
        # 11419.00420A----10
        # 10-----1260-------
        # 012345678901234567
        self.active = data[0] == '1'
        self.powered = data[1] == '1'
        self.time = _make_time(int(data[7:11]))
        if self.powered:
            self.mode = data[2]
            self.temp = float(data[3:7])
            self.fan_rate = data[11]
        else:
            self.mode = None
            self.temp = None
            self.fan_rate = None
        return self

    def to_str(self):
        if self.powered:
            return "{}1{}{}{:04}{}----10".format(
                '1' if self.active else '0',
                self.mode,
                "{:3.1f}".format(self.temp),
                _make_mins(self.time),
                self.fan_rate)
        else:
            return "{}0-----{:04}-------".format(
                '1' if self.active else '0',
                _make_mins(self.time))

    def __repr__(self):
        return "[active={active} powered={powered} time={time} mode={mode} temp={temp} fan_rate={fan_rate}]".format(**self.__dict__)



