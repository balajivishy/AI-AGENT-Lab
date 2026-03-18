const fs = require("fs");

const jobs = JSON.parse(fs.readFileSync("jobs.json"));

const pythonJobs = jobs.filter(job => {

  if (!job.analysis) return false;

  return job.analysis.toLowerCase().includes("python");

});

console.log("Python-related internships found:", pythonJobs.length);

pythonJobs.forEach(job => {
  console.log("\n---------------------------");
  console.log("Title:", job.title);
  console.log("Company:", job.company);
  console.log("Source:", job.source);
});