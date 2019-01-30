import datetime


def param_decor(path):
    def decor(old_function):
        def new_function(*args, **kwargs):
            with open(path, 'w', encoding='utf-8') as f:
                data_time = 'Function start date and time: ' + str(datetime.datetime.now())
                name = 'Function name: ' + old_function.__name__
                args_func = 'Function argument: ' + str([x for x in args])
                kwargs_func = 'Named function arguments: ' + str({key: value for key, value in kwargs.items()})
                data = old_function(*args, **kwargs)
                values = 'Return:' + str(data)
                f.write(data_time + '\n' + name + '\n' + args_func + '\n' + kwargs_func + '\n' + values)
            return data
        return new_function
    return decor
