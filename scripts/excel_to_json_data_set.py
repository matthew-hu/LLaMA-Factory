import json
import random
import requests
import pandas as pd
from time import sleep


file_path = '/Users/bytedance/Downloads/GiraffeTrainingData.xlsx'
sheet_dict = [
    {
        "sheet_name": 'English Data With Thought',
        "output_file_path": '../data/giraffe_web_ui_with_thought_en.json',
    },
    {
        "sheet_name": 'WebUI Data With Thought',
        "output_file_path": '../data/giraffe_web_ui_with_thought.json',
    },
    {
        "sheet_name": 'WebUI 代码解释',
        "output_file_path": '../data/giraffe_web_ui_with_describe.json',
    },
    {
        "sheet_name": 'WebUI 编写FAQ',
        "output_file_path": '../data/giraffe_web_ui_with_faq.json',
    },
]

for sheet in sheet_dict:
    df = pd.read_excel(file_path, sheet_name=sheet['sheet_name'])
    output_file_path = sheet['output_file_path']

    instruction = None

    res = []

    for index, row in df.iterrows():
        _input, _output = row['input'], row['output']

        # 如果当前行的instruction不为空，则更新instruction的值
        if pd.notna(row['instruction']):
            instruction = row['instruction'].lstrip().rstrip()

        print("instruction:\n", instruction)
        print("input:\n", _input)
        print("output:\n", _output)
        print("=========================")

        data = {
            # "system": instruction,
            "instruction": instruction,
            "input": _input,
            # "output": "```robotframework\n" + _output + "\n```"
            "output": _output
        }

        if pd.isna(_input) or pd.isna(_output):
            continue

        if instruction and _input and _output:
            res.append(data)

    with open(output_file_path, 'w') as outfile:
        json.dump(res, outfile, ensure_ascii=False, indent=4)
        # for item in res:
        #     outfile.write(json.dumps(item, ensure_ascii=False) + '\n')


# 数据集扩充, 1/2 1/3 


def augment_dataset(sheet_name='WebUI Data With Thought', ratio=2):
    """
    每 ratio 条中取一条数据, 并对数据的顺序随机乱序
    :param sheet_name:
    :param ratio:
    """
    for sheet in sheet_dict:
        if sheet['sheet_name'] != sheet_name:
            continue
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        output_file_path = sheet['output_file_path'].replace('.json', '') + str(ratio) + '.json'

        instruction = None
        res = []
        cnt = 0
        for index, row in df.iterrows():
            cnt += 1
            if cnt % ratio != 0:
                continue

            print("====== cnt {} ======".format(cnt))
            _input, _output = row['input'], row['output']

            # 如果当前行的instruction不为空，则更新instruction的值
            if pd.notna(row['instruction']):
                instruction = row['instruction'].lstrip().rstrip()

            print("instruction:\n", instruction)
            print("input:\n", _input)
            print("output:\n", _output)
            print("=========================")

            data = {
                "instruction": instruction,
                "input": _input,
                "output": _output
            }

            if pd.isna(_input) or pd.isna(_output):
                print("xxxxxxxxx")
                continue

            if instruction and _input and _output:
                print("yyyyyyyyy")
                res.append(data)

        print("cnt: ", cnt)
        print("len(res): ", len(res))

        with open(output_file_path, 'w') as outfile:
            # 随机乱序
            random.shuffle(res)
            json.dump(res, outfile, ensure_ascii=False, indent=4)


# 每 2、3 条取一条
# augment_dataset(ratio=2)
# augment_dataset(ratio=3)


# 从 DB 拉取训练数据并合并到 thought 数据集中
def prepare_similar_data(system_prompt):
    """

    """
    result = []
    base_url = 'https://nbq2u6x6.fn.bytedance.net/query_train_data'
    for i in range(100):
        url = base_url + f'?page={i+1}' + '&limit=100'
        resp = requests.get(url).json()
        resp_data = resp['data']
        if resp_data:
            for item in resp_data:
                result.append({
                    "instruction": system_prompt,
                    "input": item['question'],
                    "output": item['answer']
                })
        else:
            break
        sleep(1)
    return result


similar_data = prepare_similar_data('使用RobotFramework标准库和EasyUILib编写或重构WebUI自动化脚本')
print(similar_data[0])

# 合并 thought 数据集
for one_file in ['giraffe_web_ui_with_thought.json', 'giraffe_web_ui_with_thought_en.json']:
    with open('../data/' + one_file, encoding='utf-8') as f:
        records = json.load(f)
        similar_data.extend(records)
    sleep(1)

# 打乱顺序
random.shuffle(similar_data)
print(len(similar_data))
print(similar_data[0])

with open('../data/giraffe_web_ui_with_thought_all.json', 'w') as outfile:
    json.dump(similar_data, outfile, ensure_ascii=False, indent=4)


# 将现有格式数据转换成推理形式
with (open('../data/giraffe_web_ui_with_reason_all.json', 'w') as reason_file):
    for item in similar_data:
        item['output'] = item['output'].replace(
            '<thought>', '<think>').replace(
            '</thought>', '</think>').replace(
            '<code_block>', '```robot').replace(
            '</code_block>', '```')
    json.dump(similar_data, reason_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    pass
