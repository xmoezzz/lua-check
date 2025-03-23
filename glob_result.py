import glob
from llm import LocalModel

files = glob.glob('result/*.ref.txt')

results = {}

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    results[filepath] = content


name_set = set()
for name, content in results.items():
    content = content.strip()
    content = content.splitlines()
    if len(content) == 0:
        continue
    file_name = content[0]
    if file_name.startswith('./crashes_in/'):
        file_name = file_name[13:]
    name_set.add(file_name)


all_names = "\n".join(name_set)
print(all_names)

prompt = """
I have the following lua scripts:
""" + all_names + """

I want to know their corresponding roles in the IoT firmware.
Uses json format for the answer, for example:
{
    "script1": "role1",
    "script2": "role2",
}
"""

print("🥺prompt: {}".format(prompt))

output = LocalModel().ask(prompt)
print("🤖output: {}".format(output))
