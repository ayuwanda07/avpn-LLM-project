# 🎓 ScholarPrep AI

ScholarPrep AI adalah asisten virtual berbasis LLM yang dirancang khusus untuk membantu mahasiswa dan *fresh graduate* dalam mempersiapkan pendaftaran beasiswa studi lanjut (khususnya S2 ke luar negeri). Aplikasi ini dibangun menggunakan antarmuka **Streamlit** dan diintegrasikan dengan **LangChain** serta **Groq API** untuk pemrosesan bahasa alami yang cepat dan responsif.

## ✨ Fitur Utama

Aplikasi ini memiliki dua mode utama yang dapat dipilih melalui *sidebar*:

1. **Scholarship Interviewer**
   * Mode simulasi wawancara interaktif dalam bahasa Inggris.
   * Bot akan bertindak sebagai komite seleksi beasiswa (misal: LPDP, AAS, Chevening).
   * Memberikan *feedback* tata bahasa (*grammar*) dan struktur jawaban secara langsung sebelum melanjutkan ke pertanyaan wawancara berikutnya.

2. **Academic Document Reviewer**
   * Mode evaluasi dokumen pendaftaran akademik.
   * Mendukung unggah dokumen dalam format PDF atau TXT.
   * Bot akan menganalisis tata bahasa, kejelasan, *tone* profesional, dan memberikan saran perbaikan untuk *Curriculum Vitae* (CV) atau *Motivation Letter* agar memenuhi standar internasional.

## 🛠️ Teknologi yang Digunakan
* **Python**
* **Streamlit** (User Interface)
* **LangChain** (LLM Framework & Memory Management)
* **Groq API** (Inference Engine)
* **PyPDF** (PDF Text Extraction)

## 🚀 Cara Instalasi & Menjalankan Aplikasi

1. **Clone repositori ini:**
   ```bash
   git clone [https://github.com/username-kamu/scholarprep-ai.git](https://github.com/username-kamu/scholarprep-ai.git)
   cd scholarprep-ai