class TsetmcStock:
    def __init__(self, data_str):
        data = data_str.split(',')
        if len(data) <= 18:
            for i in range(len(data)):
                setattr(self, f'prop{i + 1}', data[i])
