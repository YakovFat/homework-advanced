
import re
import csv
with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pop = contacts_list.pop([0][0])
# TODO 1: выполните пункты 1-3 ДЗ
for contact in contacts_list:
    new_contact = ','.join(contact)
    telephone = "(\+7|8)(\s*)(\(*)(\d{3})(\)*)(\s*)(-*)(\d{3})(-*)(\d{2})(-*)" \
              "(\d+)(\s*)(\(*)([а-яёА-ЯЁ]{3}.)*(\s*)(\d{4})*(\)*)"
    result_1 = re.sub(telephone, r"+7(\4)\8-\10-\12\13\15\17", new_contact)
    pattern_2 = "^([а-яёА-ЯЁ]+)(\s|\W)([а-яёА-ЯЁ]+)(\s|\W)([а-яёА-ЯЁ]+)*(,+)([а-яёА-ЯЁ]+)*(,+)"
    result_2 = re.sub(pattern_2, r"\1,\3,\5,\7,", result_1)
    print(result_2)





# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
# with open("phonebook.csv", "w") as f:
#     datawriter = csv.writer(f, delimiter=',')
#     # Вместо contacts_list подставьте свой список
#     datawriter.writerows(contacts_list)

# lastname,firstname,surname
# ^([а-яёА-ЯЁ]+)(\s|\W)([а-яёА-ЯЁ]+)(\s|\W)([а-яёА-ЯЁ]+)*(\W)
# $1 $3 $5,



# telephone (\+7|8)(\s*)(\(*)(\d{3})(\)*)(\s*)(-*)(\d{3})(-*)(\d{2})(-*)(\d+)(\s*)(\(*)([а-яёА-ЯЁ]{3}.)*(\s*)(\d{4})*(\)*)
# +7(\4)\8-\10-\12\13\15\17

# email
# [a-zA-Z.]+.[a-zA-Z]+|\d+@