const axios = require("axios");
const cheerio = require("cheerio");

async function scrapeInternshala() {

  const url = "https://internshala.com/internships/software-development-internship/";

  const response = await axios.get(url);

  const $ = cheerio.load(response.data);

  const jobs = [];

  $(".individual_internship").each((i, el) => {

    const title =
      $(el).find(".job-title-href").text().trim() ||
      $(el).find("h3").text().trim();

    const company =
      $(el).find(".company-name").text().trim() ||
      $(el).find(".company_name").text().trim();

    if (title && company) {
      jobs.push({
        title: title,
        company: company,
        source: "Internshala"
      });
    }

  });

  return jobs;
}

module.exports = { scrapeInternshala };