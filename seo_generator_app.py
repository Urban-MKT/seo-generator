import streamlit as st
from fpdf import FPDF
import tempfile
import random

# --- SEO Content Generator ---
def generate_seo_content(focus_key_phrase, business_name, service):
    # Title options (≤ 60 characters)
    title_templates = [
        f"{focus_key_phrase} | {business_name}",
        f"{business_name}: {focus_key_phrase} Pros",
        f"{focus_key_phrase} Experts - {business_name}",
        f"{focus_key_phrase} Services | {business_name}",
    ]
    title = random.choice(title_templates)
    if len(title) > 60:
        title = title[:57] + "..."

    # Meta description options (≤ 160 characters)
    meta_templates = [
        f"{business_name} offers top-rated {service} using expert {focus_key_phrase}. Call today!",
        f"Need {focus_key_phrase}? {business_name} provides affordable {service} solutions.",
        f"{focus_key_phrase} made easy with {business_name}'s proven {service} services.",
        f"Choose {business_name} for {focus_key_phrase} in your {service} strategy.",
    ]
    meta_description = random.choice(meta_templates)
    if len(meta_description) > 160:
        meta_description = meta_description[:157] + "..."

    # H1 & H2
    h1 = f"{focus_key_phrase} Services by {business_name}"
    h2_1 = f"Why {focus_key_phrase} Matters in {service}"
    h2_2 = f"How {business_name} Helps with {focus_key_phrase}"

    # Paragraph
    paragraph_templates = [
        f"At {business_name}, we specialize in {focus_key_phrase} for {service}. Our approach helps businesses grow with real results.",
        f"{focus_key_phrase} is key to successful {service}. {business_name} uses smart strategies to deliver value and visibility.",
        f"With {business_name}, your {service} gets the benefit of expert-level {focus_key_phrase}, tailored to your market.",
    ]
    paragraph = random.choice(paragraph_templates)

    return {
        "SEO Title": title,
        "Meta Description": meta_description,
        "H1 Tag": h1,
        "H2 Tags": [h2_1, h2_2],
        "Paragraph": paragraph
    }

# --- PDF Export ---
def create_pdf(content_dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "SEO Content Generator", ln=True, align='C')
    pdf.set_font("Arial", "", 12)

    for key, value in content_dict.items():
        pdf.ln(8)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, f"{key}:", ln=True)
        pdf.set_font("Arial", "", 12)
        if isinstance(value, list):
            for item in value:
                pdf.multi_cell(0, 10, item)
        else:
            pdf.multi_cell(0, 10, value)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_file.name)
    return tmp_file.name

# --- Streamlit App ---
st.title("🔍 SEO Content Generator")

# Persist input values in session state
with st.form("seo_form"):
    focus_key_phrase = st.text_input("Enter your Focus Key Phrase", st.session_state.get("focus_key_phrase", ""))
    business_name = st.text_input("Enter your Business Name", st.session_state.get("business_name", ""))
    service = st.text_input("Describe Your Service", st.session_state.get("service", ""))
    submitted = st.form_submit_button("Generate SEO Content")

# Store inputs in session
if submitted and focus_key_phrase and business_name and service:
    st.session_state.focus_key_phrase = focus_key_phrase
    st.session_state.business_name = business_name
    st.session_state.service = service
    st.session_state.content = generate_seo_content(focus_key_phrase, business_name, service)

# Show results
if "content" in st.session_state and st.session_state.content:
    content = st.session_state.content
    st.subheader("Generated SEO Content")
    for key, value in content.items():
        if isinstance(value, list):
            for i, item in enumerate(value, 1):
                st.markdown(f"**{key} {i}:** {item}")
        else:
            st.markdown(f"**{key}:** {value}")

    # Regenerate button
    if st.button("🔁 Regenerate"):
        st.session_state.content = generate_seo_content(
            st.session_state.focus_key_phrase,
            st.session_state.business_name,
            st.session_state.service
        )
        st.rerun()

    # PDF Download
    pdf_path = create_pdf(content)
    with open(pdf_path, "rb") as f:
        st.download_button("📄 Download as PDF", f, file_name="seo_content.pdf")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
