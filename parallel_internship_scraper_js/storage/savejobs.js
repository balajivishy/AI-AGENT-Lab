const fs = require("fs");

function saveJobs(jobs) {

  fs.writeFileSync(
    "jobs.json",
    JSON.stringify(jobs, null, 2)
  );

  console.log("Jobs saved to jobs.json");

}

module.exports = { saveJobs };