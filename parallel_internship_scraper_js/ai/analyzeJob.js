const axios = require("axios");

async function analyzeJob(jobTitle) {

  const prompt = `
You are an AI career assistant.

From this internship title extract:

1. likely required skills
2. job category
3. difficulty level (easy, medium, hard)

Return JSON.

Job title:
${jobTitle}
`;

  const response = await axios.post(
    "http://localhost:11434/api/generate",
    {
      model: "phi3:mini",
      prompt: prompt,
      stream: false
    }
  );

  return response.data.response;
}

module.exports = { analyzeJob };