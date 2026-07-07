import re
import html

html_file = r"C:\Users\Sergio\.gemini\antigravity-cli\brain\a2883a1a-4e73-450c-b78a-3c67325ae1a7\.system_generated\steps\4\content.md"

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

content = html.unescape(content)

# The Astro island props usually contains a dictionary of parties. Let's look for something like "parties" or party properties.
# Maybe "name":[0,"Fuerza Popular"]
parties_pattern = r'"id":\[0,(\d+)\],"name":\[0,"(.*?)"\],"logoUrl":\[0,"(.*?)"\]'
matches = re.findall(parties_pattern, content)
if matches:
    print("Found exact party dict:")
    for m in matches:
        print(f"{m[0]}: {m[1]}")
else:
    print("Trying wider regex")
    wider = re.findall(r'"(\d+)":\[[01],\{(.*?)\}\]', content)
    for m in wider[:10]:
        print(m[0], m[1][:100])
