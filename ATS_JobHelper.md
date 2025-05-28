# ATS Resume Optimizer Chrome Extension

## 🚀 Mission
ATS Resume Optimizer empowers job seekers to maximize their chances of passing Applicant Tracking Systems (ATS) and landing interviews. It uses advanced AI to optimize resumes and generate tailored cover letters, ensuring your application is keyword-rich, relevant, and professionally formatted for each job.
Chorme Extension Link: Coming Soon!
---

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS, JavaScript (ES6+)
- **Chrome Extension Platform:** Manifest V3, Chrome Extension APIs
- **AI Integration:** Supports OpenAI, Groq, Claude, Gemini, DeepSeek, Mistral, and more (user provides API key)
- **Libraries:**
  - [mammoth.js](https://github.com/mwilliamson/mammoth.js) for .docx parsing
  - [pdf.js](https://mozilla.github.io/pdf.js/) for PDF parsing
  - [docx](https://github.com/dolanmiu/docx) for DOCX export
  - Google Fonts for modern typography

---

## ⚙️ Features
- **Resume Optimization:**
  - AI rewrites your resume to maximize keyword overlap with the job description
  - Only uses relevant, high-signal keywords (skills, responsibilities, mission)
  - Never fabricates experience or uses irrelevant terms
  - Output includes "Added Keywords" and "Suggested Keywords" sections
- **Cover Letter Generation:**
  - AI generates a tailored, professional cover letter for the job
- **Matching Score:**
  - Shows before/after keyword match percentage
- **File Upload:**
  - Upload your resume as .docx, .pdf, or .txt
  - Preserves formatting and parses content for editing
- **Editable Output:**
  - Edit the optimized resume or cover letter before downloading
- **Download as DOCX:**
  - Export your optimized resume as a .docx file
- **Multi-Model Support:**
  - Choose from OpenAI, Groq, Claude, Gemini, DeepSeek, Mistral, and more
  - User provides their own API key for privacy and flexibility
- **Settings Modal:**
  - Select model/service, enter API key, and choose model
- **Modern UI:**
  - Clean, card-based design with modern fonts and colors
  - Responsive and user-friendly

---

## 📝 Setup & Usage

1. **Clone or Download the Repository**
2. **Install Dependencies:** No build step required; all libraries are loaded via CDN.
3. **Load the Extension in Chrome:**
   - Go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the project folder
4. **Pin the Extension:** (optional)
   - Click the puzzle piece icon in Chrome and pin "ATS Resume Optimizer" for easy access
5. **Open the Extension:**
   - Click the extension icon in the Chrome toolbar
6. **Set Up Your API Key:**
   - Click the settings (gear) icon
   - Select your preferred AI service and model
   - Enter your API key and save
7. **Optimize Your Resume:**
   - Paste or upload your resume and the job description
   - Click "Generate ATS Resume" or "Generate Cover Letter"
   - Edit the output as needed
   - Download as DOCX if desired

---

## 🌟 Example Use Cases
- Job seekers tailoring resumes for each application
- Career coaches helping clients optimize for ATS
- Students and professionals seeking to improve their job search materials

---

## 💡 Why Use This Extension?
- **ATS-Ready:** Ensures your resume passes automated filters
- **AI-Powered:** Leverages the latest LLMs for best results
- **Customizable:** Supports multiple AI providers and models
- **Private:** Your API key and data stay on your device
- **User-Friendly:** Modern, intuitive interface
