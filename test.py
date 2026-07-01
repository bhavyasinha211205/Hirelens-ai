from models.resume_parser import parse_resume

with open("resume.txt", "r", encoding="utf-8") as f:
    text = f.read()

result = parse_resume(text)

print(result)