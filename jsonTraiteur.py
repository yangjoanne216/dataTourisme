import json
import csv
import os

'''

with open('flux/index.json', 'r') as f:
    data = json.load(f)
print("this is nombre of entreprise" + len(data))  # 输出公司的数量
'''


# to do：输出更新的时间
def extract_info(json_file):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            addresses = data["isLocatedAt"][0]["schema:address"][0]["schema:streetAddress"] if "isLocatedAt" in data and "schema:address" in data["isLocatedAt"][0] and "schema:streetAddress" in data["isLocatedAt"][0]["schema:address"][0] else []
            address_1 = addresses[0] if len(addresses) > 0 else None
            address_2 = addresses[1] if len(addresses) > 1 else None
            telephones = data["hasContact"][0]["schema:telephone"] if "hasContact" in data and "schema:telephone" in data["hasContact"][0] else []
            telephone1 = telephones[0] if len(telephones) > 0 else None
            telephone2 = telephones[1] if len(telephones) > 1 else None

            # 提取需要的信息
            company_info = {
                "Afficher le nom ": data["rdfs:label"]["fr"][0],
                "Étiquettes": ", ".join(data["@type"]),
                "Rue 1": address_1,
                "Rue 2": address_2,
                "Ville": data["isLocatedAt"][0]["schema:address"][0]["hasAddressCity"]["rdfs:label"]["fr"][0],
                "État":
                    data["isLocatedAt"][0]["schema:address"][0]["hasAddressCity"]["isPartOfDepartment"]["rdfs:label"]["fr"][
                        0],
                "Pays":
                    data["isLocatedAt"][0]["schema:address"][0]["hasAddressCity"]["isPartOfDepartment"]["isPartOfRegion"][
                        "isPartOfCountry"]["rdfs:label"]["fr"][0],
                "Code postal": data["isLocatedAt"][0]["schema:address"][0]["schema:postalCode"],
                "Téléphone": telephone1,
                "Mobile": telephone2,
                "Site web": data["hasContact"][0]["foaf:homepage"][0] if "hasContact" in data and "foaf:homepage" in
                                                                     data["hasContact"][0] else None

            }

            return company_info
    except Exception as e:
        print(f"处理文件 {json_file} 时发生错误： {str(e)}")
        if "@id" in data :
            print(f"错误发生在 {data['@id']}")
        return None



# 遍历文件夹和子文件夹
root_dir = 'flux/objects'
with open('company_info.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Afficher le nom", "Étiquettes", "Rue 1", "Rue 2", "Ville",
        "État", "Pays", "Code postal", "Téléphone", "Mobile", "Site web"
    ])
    writer.writeheader()
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):  # 检查文件是否为json文件
                json_file = os.path.join(subdir, file)
                company_info = extract_info(json_file)
                writer.writerow(company_info)
