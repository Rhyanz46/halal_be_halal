from datetime import date, datetime
from flask import abort
from core import result


class ValueChecker:
    def __init__(self, data_request):
        self.data_request = data_request
        self.type = type(data_request)
        self.__parsed = {}

    def parse(self, field, field_type, nullable=False, length=float("inf"), enum=None):
        is_dict = self.type == dict

        data_request = self.data_request
        if isinstance(None, self.type):
            if not nullable:
                msg = {
                    "message": 'you have to set a data'
                }
                abort(result(msg, 400))
            return self.__parsed.update({field: None})

        if enum != None and type(enum) != list:
            raise ValueError("enum must be list, for '{}' field".format(field))

        if is_dict:
            value = data_request.get(field)
            if enum:
                if value not in enum:
                    msg = {
                        "message": 'value error for field {}'.format(field)
                    }
                    abort(result(msg, 400))
            if not nullable:
                if isinstance(None, type(value)):
                    msg = {
                        "message": 'field {} it\'s can\'t be null'.format(field)
                    }
                    abort(result(msg, 400))
            else:
                if isinstance(None, type(value)):
                    return self.__parsed.update({field: value})
            if field_type == date:
                try:
                    value = datetime.strptime(value, "%d-%m-%Y").date()
                    wrong_type = False
                    wrong_len = False
                except:
                    msg = {
                        "message": 'for field {} date type format must be  : dd-mm-yyyy'.format(field)
                    }
                    abort(result(msg, 400))
            else:
                wrong_type = type(value) != field_type
                wrong_len = len(str(value)) > length

            if wrong_type:
                msg = {
                    "message": 'field {} it\'s must be {}'.format(field, field_type)
                }
                abort(result(msg, 400))
            if wrong_len:
                msg = {
                    "message": 'length of filed {} can\'t over {}'.format(field, length)
                }
                abort(result(msg, 400))
            self.__parsed.update({field: value})

    def get_parsed(self):
        return self.__parsed
