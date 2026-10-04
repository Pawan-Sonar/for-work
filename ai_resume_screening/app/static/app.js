const result = document.querySelector("#result");
const resumeSelect = document.querySelector("#resume-select");
const jobSelect = document.querySelector("#job-select");

async function request(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error((await response.json()).detail || "Request failed");
  return response.json();
}

function populate(select, items, label) {
  select.innerHTML = items.map(item => `<option value="${item.id}">${label(item)}</option>`).join("");
}

async function refreshLists() {
  const [resumes, jobs] = await Promise.all([request("/resumes"), request("/jobs")]);
  populate(resumeSelect, resumes.filter(r => r.status === "ready"), r => `${r.filename} (${r.extracted_skills.join(", ") || "no skills found"})`);
  populate(jobSelect, jobs, j => `${j.title} (${j.extracted_skills.join(", ") || "no skills found"})`);
}

document.querySelector("#job-form").addEventListener("submit", async event => {
  event.preventDefault();
  try {
    await request("/jobs", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ title: document.querySelector("#job-title").value, description: document.querySelector("#job-description").value }) });
    event.target.reset();
    await refreshLists();
    result.textContent = "Job description added.";
  } catch (error) { result.textContent = error.message; }
});

document.querySelector("#resume-form").addEventListener("submit", async event => {
  event.preventDefault();
  try {
    const form = new FormData();
    form.append("file", document.querySelector("#resume-file").files[0]);
    await request("/resumes", { method: "POST", body: form });
    event.target.reset();
    result.textContent = "Resume uploaded. Wait a few seconds, then refresh the page to compare it.";
  } catch (error) { result.textContent = error.message; }
});

document.querySelector("#match-button").addEventListener("click", async () => {
  try {
    const match = await request(`/matches?resume_id=${resumeSelect.value}&job_id=${jobSelect.value}`, { method: "POST" });
    result.textContent = `Similarity score: ${match.similarity_score}%\n\nMatched skills: ${match.matched_skills.join(", ") || "None"}\nMissing skills: ${match.missing_skills.join(", ") || "None"}\n\nInterview questions:\n${match.interview_questions.map(q => `• ${q}`).join("\n")}`;
  } catch (error) { result.textContent = error.message; }
});

refreshLists().catch(error => result.textContent = error.message);
