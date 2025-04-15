import json

import pandas as pd

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


if __name__ == '__main__':
    pass
