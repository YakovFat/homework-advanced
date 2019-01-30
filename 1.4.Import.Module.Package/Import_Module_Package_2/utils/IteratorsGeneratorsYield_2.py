import hashlib


def md5_file_1(file_in):
    with open(file_in, 'r', encoding='utf-8') as f:
        for line in f:
            h = hashlib.md5(line.encode())
            yield h.hexdigest()


if __name__ == '__main__':
    for i in md5_file_1('countries-wiki.txt'):
        print(i)
