import pandas as pd

faq_data = {
    "Category": [
        "Program Overview",
        "Program Structure",
        "Program Structure",
        "Pricing & Fees",
        "Pricing & Fees",
        "Curriculum & Skills",
        "Curriculum & Skills",
        "Evaluation & Projects",
        "Career & Placement",
        "Leadership & Contact"
    ],

    "Question": [
        "What is the total duration and structure of the PragyanAI program?",
        "What happens in Phase 1 (First 6 Months)?",
        "What happens in Phase 2 (12 Months)?",
        "What is the fee structure for the Founding Batch?",
        "What is the salary potential after completing the program?",
        "What modules are covered in Months 1-3?",
        "What modules are covered in Months 4-6?",
        "How are students evaluated?",
        "What career tracks are available?",
        "Who leads PragyanAI?"
    ],

    "Answer": [
        "PragyanAI AI GenAI program is an 18-month journey with 6 months offline training followed by 12 months internship and placement support.",
        "Phase 1 includes offline classroom training, labs, projects, hackathons and technical seminars.",
        "Phase 2 includes internship, live projects, mock interviews, resume building and product development.",
        "Founding batch fee is ₹50,000 training fee plus ₹50,000 success fee after placement.",
        "AI Engineer packages range from ₹6-15 LPA, GenAI Engineer ₹8-18 LPA and Agentic AI Engineer ₹10-25 LPA.",
        "Python, Analytics, Data Science, BI Analytics and Machine Learning.",
        "Deep Learning, Computer Vision, NLP, Generative AI, RAG, LangChain and Agentic AI.",
        "Students are evaluated through seminars, projects and 48-hour hackathons.",
        "Data Analyst, Data Scientist, ML Engineer, AI Engineer, GenAI Engineer, Agentic AI Engineer.",
        "PragyanAI is led by Sateesh Ambesange."
    ]
}


df = pd.DataFrame(faq_data)

df.to_excel(
    "pragyan_faq_prices.xlsx",
    index=False
)

print("Excel file created successfully")
