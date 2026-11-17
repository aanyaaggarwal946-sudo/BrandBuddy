import streamlit as st
from google import genai
from google.genai import types
from knowledge_base import MANUAL

st.set_page_config(page_title="BrandBuddy | AI Marketing Consultant", page_icon="📈", layout="centered")

SYSTEM_INSTRUCTION = """
You are BrandBuddy, an intelligent and professional AI Digital Marketing Consultant
for small businesses, startups, entrepreneurs and marketing students.

Use the supplied BrandBuddy knowledge base as your primary source. Give accurate,
simple, practical and actionable advice. Explain technical terms, use examples,
and apply frameworks such as SWOT, STP, AIDA, SMART and the 4Ps when relevant.

For business problems, consider the business type, target audience, objective and
budget. Ask a short follow-up only if an essential detail is missing.

For campaign requests, include objectives, audience, platforms, content ideas,
budget allocation, implementation steps and KPIs where relevant.

Answer digital-marketing questions using the supplied manual. If a question is
unrelated or the manual lacks enough information, say so politely. Do not invent
statistics, research findings or campaign results. Clearly label assumptions and
illustrative examples.

Be friendly, professional, creative, analytical and solution-oriented.
"""

st.title("📈 BrandBuddy")
st.subheader("Your AI-powered digital marketing consultant")
st.write("Practical guidance on SEO, branding, social media, advertising, customer segmentation and campaign planning.")

with st.sidebar:
    st.header("About BrandBuddy")
    st.write("A Gemini-powered marketing assistant for small businesses, startups and students.")
    st.divider()
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.caption("Tip: Include your business, target audience, goal and budget.")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    api_key = ""

if not api_key or api_key == "PASTE_YOUR_NEW_GEMINI_API_KEY_HERE":
    st.error("Gemini API key not configured. Add it to .streamlit/secrets.toml and restart the app.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask BrandBuddy a marketing question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("BrandBuddy is thinking..."):
            try:
                client = genai.Client(api_key=api_key)
                recent = st.session_state.messages[-12:]
                conversation = "\n\n".join(
                    f'{m["role"].upper()}: {m["content"]}' for m in recent
                )

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=(
                        "BRANDBUDDY KNOWLEDGE BASE:\n" + MANUAL
                        + "\n\nCONVERSATION:\n" + conversation
                        + "\n\nAnswer the latest user message."
                    ),
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.5,
                    ),
                )
                answer = response.text or "I couldn't generate a response. Please try again."
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as exc:
                st.error("Could not connect to Gemini. Check your API key, internet connection and model access.")
                st.caption(f"Technical details: {exc}")
