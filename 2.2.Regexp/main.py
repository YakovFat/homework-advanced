import re
import csv
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pop = contacts_list.pop([0][0])
people_dict = {}
for contact in contacts_list:
    fio = re.split("\s+", contact[0] + " " + contact[1] + " " + contact[2])
    if "" in fio:
        fio.remove("")
    fio = tuple(fio)
    empty_dict = {"organization": "", "position": "", "phone": "", "email": ""}
    people_dict.setdefault(fio, empty_dict)
    if len(people_dict[fio]["organization"]) == 0:
        people_dict[fio]["organization"] = contact[3]
    people_dict[fio]["position"] = (
        lambda var: var if len(var) > 0 else people_dict[fio]["position"])(
        contact[4])
    pattern = "(\+7|8)(\s*)(\(*)(\d{3})(\)*)(\s*)(-*)(\d{3})(-*)(\d{2})(-*)" \
              "(\d+)(\s*)(\(*)([а-яёА-ЯЁ]{3}.)*(\s*)(\d{4})*(\)*)"
    contact[5] = re.sub(pattern, r"+7(\4)\8-\10-\12\13\15\17", contact[5])
    people_dict[fio]["phone"] = (
        lambda var: var if len(var) > 0 else people_dict[fio]["phone"])(
        contact[5])
    people_dict[fio]["email"] = (
        lambda var: var if len(var) > 0 else people_dict[fio]["email"])(
        contact[6])

for k in people_dict.keys():
    if len(k) < 3:
        for k2 in people_dict.keys():
            if k[0] == k2[0] and len(k2) == 3:
                for i in people_dict[k]:
                    if people_dict[k][i] != '':
                        people_dict[k2][i] = people_dict[k][i]
                new_people_dict = people_dict.copy()
                del new_people_dict[k]

pprint(new_people_dict)
final_people_csv = []
final_people_csv.append(pop)
for i in new_people_dict:
    final_people_csv.append([*i, new_people_dict[i]['organization'],
                             new_people_dict[i]['position'],
                             new_people_dict[i]['phone'],
                             new_people_dict[i]['email']])

print(final_people_csv)
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_people_csv)
