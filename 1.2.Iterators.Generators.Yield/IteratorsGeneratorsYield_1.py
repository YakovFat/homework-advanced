import json


class Countries:
    def __init__(self, start, end, file_in, file_out):
        self.start, self.end = start - 1, end
        self.file_in = file_in
        self.file_out = file_out

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.file_in, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.start += 1
        if self.start == self.end:
            raise StopIteration
        try:
            country = data[self.start]['name']['common']
            country_link = country.replace(' ', '_')
            with open(self.file_out, 'a', encoding='utf-8') as f:
                f.write(f'{country} - https://en.wikipedia.org/wiki/{country_link}\n')
            return f'{country} - https://en.wikipedia.org/wiki/{country_link}'
        except IndexError:
            exit(0)


for i in Countries(1, 1000000000, 'countries.json', 'countries-wiki.txt'):
    print(i)
