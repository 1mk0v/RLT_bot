from pymongo import cursor
from models import Response, Request
from datetime import datetime, time
from calendar import monthrange

class Aggregator:

    def __init__(
            self,
            data:cursor.Cursor,
            request:Request
    ) -> None:
        self.data = data
        self.request = request

    def __getDatetimeOfHour(self, date:datetime, countToPlus:int = None):
        if not countToPlus:
            return datetime.combine(date.date(), time(date.hour, 0, 0))
        if date.hour + countToPlus > 23:
            return self.__getDatetimeOfDay(date, 1)
        return datetime.combine(date.date(), time(date.hour + countToPlus, 0, 0))
    
    def __getDatetimeOfDay(self, date:datetime, countToPlus:int = None):
        if not countToPlus:
            return datetime.combine(date.date(), datetime.min.time())
        if date.day + countToPlus > monthrange(date.year, date.month)[1]:
            return self.__getDatetimeOfMonth(date, 1)
        return datetime(date.year, date.month, date.day+1, 0, 0, 0)

    def __getDatetimeOfMonth(self, date:datetime, countToPlus:int = None):
        if not countToPlus:
            return datetime(date.year, date.month, 1, 0, 0, 0)
        if date.month + countToPlus > 12:
            return datetime(date.year + 1, 1, 1, 0, 0, 0)
        return datetime(date.year, date.month+countToPlus, 1, 0, 0, 0)

    def __getDateConvertMethod(self) -> datetime:
        method = {
            "hour": self.__getDatetimeOfHour,
            "day": self.__getDatetimeOfDay,
            "month": self.__getDatetimeOfMonth
        }
        return method[self.request.group_type]

    def aggregation(self) -> str:
        convertMethod = self.__getDateConvertMethod()
        data = dict()
        currentDate = self.request.dt_from
        while currentDate <= self.request.dt_upto:
            data[currentDate] = 0    
            currentDate = convertMethod(currentDate, 1)
        local_count:int = 0 
        for element in self.data:
            if convertMethod(element['dt']) == datetime(2022, 12, 1, 0, 0, 0):
                local_count += 1 
            data[convertMethod(element['dt'])] += element['value']
        print(local_count)
        return Response(dataset=data.values(), labels=data.keys()).model_dump_json()