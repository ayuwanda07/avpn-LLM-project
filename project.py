import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import pypdf 

st.set_page_config(page_title="ScholarPrep Assistant", page_icon="🎓")

st.title("🎓 ScholarPrep Assistant")
st.markdown("Teman simulasi wawancara beasiswa & reviewer dokumen akademik.")
# --- CUSTOM CSS (MINIMALIST UI) ---
st.markdown("""
<style>
    /* Sembunyikan default header, footer, dan menu Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Ubah padding top agar lebih rapat ke atas */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPTS = {
    "Scholarship Interviewer": (
        "You are an experienced interviewer for prestigious international scholarships. "
        "Ask ONE question at a time. Always provide brief grammar/structure feedback on the candidate's previous answer BEFORE asking the next question."
    ),
    "Academic Document Reviewer": (
        "You are an expert academic editor. The user will provide a document (Motivation Letter, CV, etc.). "
        "Review it for grammar, tone, clarity, and vocabulary choice. Provide concrete corrections and actionable advice."
    )
}

with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.expander("🔑 Setup API Key", expanded=not st.session_state.get("api_key")):
        api_key_input = st.text_input("Groq API Key", type="password", value=st.session_state.get("api_key", ""))
        if api_key_input:
            st.session_state["api_key"] = api_key_input
            
    st.divider()

    selected_mode = st.selectbox("Pilih Mode:", options=list(SYSTEM_PROMPTS.keys()), index=0)


    if "current_mode" not in st.session_state:
        st.session_state["current_mode"] = selected_mode

    if st.button("🗑️ Clear / Reset Chat", use_container_width=True):
        st.session_state["chat_history"] = [SystemMessage(SYSTEM_PROMPTS[selected_mode])]
        st.rerun()

    document_prompt = None
    if selected_mode == "Academic Document Reviewer":
        st.divider()
        st.subheader("📁 Upload Dokumen")
        st.markdown("Upload CV / Motivation Letter kamu untuk di-review.")
        
        uploaded_file = st.file_uploader("Format didukung: PDF, TXT", type=["pdf", "txt"])
        submit_file = st.button("Kirim Dokumen", use_container_width=True)
        
        if uploaded_file and submit_file:
            extracted_text = ""
            try:
                if uploaded_file.name.endswith(".pdf"):
                    pdf_reader = pypdf.PdfReader(uploaded_file)
                    extracted_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
                else:
                    extracted_text = uploaded_file.getvalue().decode("utf-8")

                document_prompt = f"Tolong review dokumen ini:\n\n{extracted_text}"
            except Exception as e:
                st.error(f"Gagal membaca file: {e}")

if not st.session_state.get("api_key"):
    st.info("💡 Silakan masukkan Groq API Key di sidebar.")
    st.stop()

if st.session_state["current_mode"] != selected_mode or "chat_history" not in st.session_state:
    st.session_state["current_mode"] = selected_mode
    st.session_state["chat_history"] = [SystemMessage(SYSTEM_PROMPTS[selected_mode])]

client = ChatGroq(model="openai/gpt-oss-120b", api_key=st.session_state["api_key"])
chat_history = st.session_state["chat_history"]

for chat_msg in chat_history:
    if isinstance(chat_msg, HumanMessage):
        with st.chat_message("User"):
            st.markdown(chat_msg.content)
    elif isinstance(chat_msg, AIMessage):
        with st.chat_message("AI"):
            st.markdown(chat_msg.content)

if len(chat_history) == 1:
    st.info("👋 **Siap untuk mulai?**\n\nKetik 'Hello' untuk memulai wawancara, atau gunakan fitur *Upload Dokumen* di sidebar jika kamu berada di mode Reviewer.")

text_prompt = st.chat_input("Ketik balasan/pertanyaan kamu di sini...")

final_prompt = text_prompt or document_prompt

if final_prompt:
    chat_history.append(HumanMessage(final_prompt))
    with st.chat_message("User"):
        if document_prompt:
            st.markdown(f"*(User mengunggah dokumen: {uploaded_file.name})*")
            with st.expander("Lihat isi dokumen"):
                st.markdown(final_prompt)
        else:
            st.markdown(final_prompt)

    with st.chat_message("AI"):
        with st.spinner("Membaca dan menganalisis..."):
            response = client.invoke(chat_history)
            st.markdown(response.content)
    
    chat_history.append(response)