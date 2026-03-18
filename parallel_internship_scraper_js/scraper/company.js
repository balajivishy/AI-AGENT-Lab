const axios = require("axios");

async function scrapeCompany() {

  const url = "https://jobs.ashbyhq.com/scaleai"; // example startup jobs page

  const response = await axios.get(url);

  const jobs = [];

  const matches = response.data.match(/intern/gi);

  if (matches) {
    jobs.push({
      title: "Intern roles found (manual parse)",
      company: "Scale AI",
      source: "Company Page"
    });
  }

  return jobs;
}

module.exports = { scrapeCompany };