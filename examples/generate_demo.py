from pathlib import Path
import zipfile
root=Path(__file__).parent/'demo_evidence';root.mkdir(exist_ok=True)
(root/'report.txt').write_text('TRACE demonstration evidence. Created for a controlled local test case.\n',encoding='utf-8')
(root/'notes.txt').write_text('A second ordinary file for timeline/hash demonstration.\n',encoding='utf-8')
with zipfile.ZipFile(root/'bundle.zip','w') as z:z.write(root/'report.txt','report.txt');z.write(root/'notes.txt','notes.txt')
print(root.resolve())
