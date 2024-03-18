import markdown
import pdfkit

# 读取Markdown文件
with open('business_plan.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 将Markdown转换为HTML
html = markdown.markdown(text)

# 将HTML转换为PDF
pdfkit.from_string(html, 'output.pdf')
