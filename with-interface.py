import gradio as gr
import openai
import os

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize a list to keep track of summaries history
summary_history = []

# Function to add a summary to the history and prepare a context message
def add_summary_to_history(summary):
    """Adds a given summary to the summary history."""
    summary_history.append({"role": "system", "content": f"Summary: {summary}"})

# all  part of  business plan
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

# Demo company information for showcasing - A profit-focused fashion startup
demo_company_info = {
    "name": "TechWear Innovations",
    "industry": "Functional Fashion",
    "products": "High-tech, durable clothing lines integrating smart technology for urban lifestyles",
    "market": "Tech-savvy consumers looking for functional yet stylish clothing solutions",
    "goals": "To dominate the functional fashion market by introducing innovative products that blend technology with style",
    "challenges": "Differentiating from competitors, managing production costs, and staying ahead in tech advancements"
}

def generate_business_plan_part(part, company_info):
    """Generates content for a given part of the business plan using the company information."""
    # Format the company_info for inclusion in the prompt
    company_info_str = ', '.join([f"{k}: {v}" for k, v in company_info.items()])

    # Generate the main content using the specified model
    full_response = openai.ChatCompletion.create(
        model="gpt-4",  # Specify the GPT-4 chat model identifier
        messages=[
            *summary_history,  # Include previous summaries as context
            {"role": "user", "content": f"{part['prompt']} Here is the company information: {company_info_str}. Note: Generating Markdown file segment for {part['title']} generate a 300-word professionally written paragraph"}
        ]
    )
    content = full_response.choices[0].message['content']

    # Generate a summary using a different model for brevity
    summary_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use an appropriate model for summarization
        messages=[
            {"role": "user", "content": f"Summarize the following in 100 words or less: {content}"}
        ]
    )
    summary = summary_response.choices[0].message['content'].strip()

    # Print and add the summary to the history for future context
    add_summary_to_history(summary)
    # Return only the main content for inclusion in the Markdown file
    return content


def generate_business_plan(mode, company_name="", industry="", products="", market="", goals="", challenges=""):
    if mode == "Demo":
        company_info = demo_company_info  # Use the demo_company_info dictionary
    else:
        company_info = {
            "name": company_name,
            "industry": industry,
            "products": products,
            "market": market,
            "goals": goals,
            "challenges": challenges
        }
    
    markdown_content = f"# Business Plan for {company_info['name']}\n"
    
    for part in business_plan_parts:
        content = generate_business_plan_part(part, company_info)  # This function needs to be adapted to work with placeholders
        markdown_content += f"## {part['title']}\n{content}\n\n"
    
    return markdown_content

# Define Gradio interface
def setup_gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Business Plan Generator")
        mode = gr.Radio(choices=["Demo", "Custom"], label="Select Mode", value="Demo")
        company_name = gr.Textbox(label="Company Name", visible=False)
        industry = gr.Textbox(label="Industry", visible=False)
        products = gr.Textbox(label="Products/Services", visible=False)
        market = gr.Textbox(label="Target Market", visible=False)
        goals = gr.Textbox(label="Goals", visible=False)
        challenges = gr.Textbox(label="Challenges", visible=False)
        generate_button = gr.Button("Generate Business Plan")
        output_markdown = gr.Markdown()

        def update_mode(value):
            visibility = value == "Custom"
            company_name.visible = visibility
            industry.visible = visibility
            products.visible = visibility
            market.visible = visibility
            goals.visible = visibility
            challenges.visible = visibility

        mode.change(update_mode, inputs=[mode], outputs=[company_name, industry, products, market, goals, challenges])

        def generate_plan(mode, company_name, industry, products, market, goals, challenges):
            return generate_business_plan(mode, company_name, industry, products, market, goals, challenges)

        generate_button.click(
            generate_plan,
            inputs=[mode, company_name, industry, products, market, goals, challenges],
            outputs=[output_markdown]
        )

    demo.launch()

if __name__ == "__main__":
    setup_gradio_interface()
