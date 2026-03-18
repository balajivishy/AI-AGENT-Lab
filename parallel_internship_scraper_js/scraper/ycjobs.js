const axios = require("axios");
const cheerio = require("cheerio");

async function scrapeYCJobs() {

  const url = "https://www.ycombinator.com/jobs";

  const response = await axios.get(url);

  const $ = cheerio.load(response.data);

  const jobs = [];

  $("a").each((i, el) => {

    const title = $(el).text().trim();

    if (title.toLowerCase().includes("intern")) {

      jobs.push({
        title: title,
        company: "YC Startup",
        source: "YC Jobs"
      });

    }

  });

  return jobs;
}

module.exports = { scrapeYCJobs };