import hashlib


def md5_file_1(file_in):
    start = 1
    f = open(file_in, 'r', encoding='utf-8')
    end = sum(1 for _ in f)
    f.close()
    with open(file_in, 'r', encoding='utf-8') as f:
        while start <= end:
            x = f.readline()
            h = hashlib.md5(x.encode())
            yield h.hexdigest()
            start += 1


def md5_file_2(start, end, file_in):
    f = open(file_in, 'r', encoding='utf-8')
    end_file = sum(1 for _ in f)
    f.close()
    with open(file_in, 'r', encoding='utf-8') as f:
        while start < end and start <= end_file:
            x = f.readline()
            h = hashlib.md5(x.encode())
            yield h.hexdigest()
            start += 1


for i in md5_file_1('countries-wiki.txt'):
    print(i)

print('___________________')

for i in md5_file_2(1, 100000, 'countries-wiki.txt'):
    print(i)

# проверка
ha = hashlib.md5(b'Afghanistan - https://en.wikipedia.org/wiki/Afghanistan\n')
print(ha.hexdigest())
