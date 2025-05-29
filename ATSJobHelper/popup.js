
document.getElementById("generateResume").addEventListener("click", async () => {
  const jobDescription = document.getElementById("jobInput").value;
  const resumeText = document.getElementById("resumeInput").value;
  const response = await fetch("https://api.groq.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": "Bearer YOUR_GROQ_OR_OPENAI_API_KEY",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "llama3-70b-8192",
      messages: [{
        role: "system",
        content: "You are an ATS resume optimizer that improves formatting, keyword match, and ATS readability while preserving the original structure."
      }, {
        role: "user",
        content: `Here is the job description:\n${jobDescription}\n\nHere is the original resume:\n${resumeText}\n\nReturn an optimized version ready for ATS.`
      }]
    })
  });
  const data = await response.json();
  document.getElementById("outputArea").value = data.choices[0].message.content;
});

document.getElementById("generateCoverLetter").addEventListener("click", async () => {
  const jobDescription = document.getElementById("jobInput").value;
  const resumeText = document.getElementById("resumeInput").value;
  const response = await fetch("https://api.groq.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": "Bearer YOUR_GROQ_OR_OPENAI_API_KEY",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "llama3-70b-8192",
      messages: [{
        role: "system",
        content: "You are a professional cover letter writer using best practices, UCSC’s formatting guide, and keyword tailoring."
      }, {
        role: "user",
        content: `Write a tailored cover letter for this job:\n${jobDescription}\n\nUsing this resume:\n${resumeText}`
      }]
    })
  });
  const data = await response.json();
  document.getElementById("outputArea").value = data.choices[0].message.content;
});
