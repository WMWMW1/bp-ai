import openai
import os

# 设置 OpenAI API 密钥
openai.api_key = os.getenv("OPENAI_API_KEY")
summary_history = []

# Function to add a summary to the history and create a context message
def add_summary_to_history(summary):
    summary_history.append({"role": "system", "content": f"Summary: {summary}"})

# 更新后的商业计划部分
business_plan_parts = [
    {"title": "Executive Summary", "prompt": "Provide a concise overview of the company's mission, products, target market, and key financial highlights."},
    {"title": "Company Description", "prompt": "Describe the company's history, ownership structure, and the main business activities."},
    {"title": "Market Analysis", "prompt": "Conduct an analysis of market trends, target market characteristics, and competitive landscape."},
    {"title": "Operational Plan", "prompt": "Outline the operational workflow, including production, inventory management, and suppliers."},
    {"title": "Products and Services", "prompt": "Detail the company's product lines, unique selling propositions, and development roadmap."},
    {"title": "Marketing and Sales Strategy", "prompt": "Describe the marketing strategy, sales tactics, and customer engagement plans."},
    {"title": "Financial Plan and Projections", "prompt": "Provide financial projections, including profit and loss forecasts, cash flow analysis, and capital expenditure budgets."},
    {"title": "Growth Strategy", "prompt": "Explain the company's future growth plans, including potential markets, products, or partnerships."}
]

# 演示模式下的公司信息 - 专注于盈利的时尚创业公司
demo_company_info = {
    "name": "TechWear Innovations",
    "industry": "Functional Fashion",
    "products": "High-tech, durable clothing lines integrating smart technology for urban lifestyles",
    "market": "Tech-savvy consumers looking for functional yet stylish clothing solutions",
    "goals": "To dominate the functional fashion market by introducing innovative products that blend technology with style",
    "challenges": "Differentiating from competitors, managing production costs, and staying ahead in tech advancements"
}

# 函数来获取用户输入或使用演示数据
def get_company_info(demo_mode=False):
    if demo_mode:
        user_info= demo_company_info
    else:
        user_info = {
            "name": input("Enter company name: "),
            "industry": input("Enter industry: "),
            "products": input("Describe your main products or services: "),
            "market": input("Describe your target market: "),
            "goals": input("What are your short-term and long-term goals? "),
            "challenges": input("What are the main challenges you face? ")
        }
    print_company_info(user_info)  # 美化打印公司信息
    return user_info
def print_company_info(company_info):
    print("\nCompany Information:\n")
    for key, value in company_info.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    print("\n" + "="*50 + "\n")

def generate_business_plan_part(part, company_info):
    # Ensure company_info is formatted correctly for inclusion in the prompt
    company_info_str = ', '.join([f"{k}: {v}" for k, v in company_info.items()])

    # Generate the main content using GPT-4 chat model
    full_response = openai.ChatCompletion.create(
        model="gpt-4",  # Adjust with the correct GPT-4 chat model identifier
        messages=[
            *summary_history,  # Include previous summaries as part of the context
            {"role": "user", "content": f"{part['prompt']} Here is the company information: {company_info_str}.Note: Generating Markdown file segment for {part['title']} generate a 300 word profesionally writed paragraph"}
        ]
    )
    content = full_response.choices[0].message['content']

    # Generate the summary using GPT-3.5 chat model
    summary_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the appropriate model for GPT-3.5
        messages=[
            {"role": "user", "content": f"Summarize the following in 100 words or less: {content}"}
        ]
    )
    summary = summary_response.choices[0].message['content'].strip()

    # Print and add the summary to the history
    print_summary(part['title'], summary)
    add_summary_to_history(summary)
    print(content)
    # Return only the content, not the summary, for inclusion in the Markdown file
    return content


# Function to print the summary
def print_summary(title, summary):
    print(f"### Summary for {title} ###\n{summary}\n\n" + "-"*50 + "\n")

# Main function to drive the script
def main():
    mode = input("Enter mode (demo/non-demo): ").strip().lower()
    demo_mode = mode == "demo" or mode == ""
    company_info = get_company_info(demo_mode=demo_mode)

    markdown_content = f"# Business Plan for {company_info['name']}\n"

    for part in business_plan_parts:
        content = generate_business_plan_part(part, company_info)
        markdown_content += f"## {part['title']}\n{content}\n\n"

    file_path = "business_plan.md"
    with open(file_path, "w") as file:
        file.write(markdown_content)

    print(f"Business plan saved to {file_path}")

if __name__ == "__main__":
    main()
