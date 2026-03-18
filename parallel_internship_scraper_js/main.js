const { scrapeInternshala } = require("./scraper/internshala");
const { scrapeYCJobs } = require("./scraper/ycjobs");
const { scrapeCompany } = require("./scraper/company")
const { saveJobs } = require("./storage/savejobs");
const { analyzeJob } = require("./ai/analyzejob");
async function run() {

  console.log("Starting parallel scraping...");

  const results = await Promise.all([
    scrapeInternshala(),
    scrapeYCJobs(),
    scrapeCompany()
  ]);

  const jobs = results.flat();

  console.log("Total jobs collected:", jobs.length);

  const jobsToAnalyze = jobs.slice(0, 10);

for (const job of jobsToAnalyze) {

  try {

    const analysis = await analyzeJob(job.title);
    job.analysis = analysis;

  } catch (err) {

    job.analysis = "analysis_failed";

  }

}
saveJobs(jobs);

}

run();