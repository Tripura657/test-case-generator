async function generate() {
  const prompt = document.getElementById("prompt").value;
  const output = document.getElementById("output");
  output.textContent = "Generating...";

  const res = await fetch("/generate", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ prompt })
  });

  const data = await res.json();
  output.textContent = data.result || data.detail;
}