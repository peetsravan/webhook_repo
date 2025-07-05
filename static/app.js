const feed = document.getElementById("feed");

function fmt(d) {
  /* ISO → "1 Apr 2021 - 09:30 PM UTC" */
  const date = new Date(d);
  return date.toLocaleString("en-GB", { timeZone: "UTC", hour12: true }) + " UTC";
}

function renderItem(evt) {
  switch (evt.type) {
    case "push":
      return `${evt.author} pushed to ${evt.to_branch} on ${fmt(evt.timestamp)}`;
    case "pull_request":
      return `${evt.author} submitted a pull request from ${evt.from_branch} to ${evt.to_branch} on ${fmt(evt.timestamp)}`;
    case "merge":
      return `${evt.author} merged branch ${evt.from_branch} to ${evt.to_branch} on ${fmt(evt.timestamp)}`;
  }
}

async function refresh() {
  const res  = await fetch("/events");
  const data = await res.json();
  feed.innerHTML = data.map(e => `<li>${renderItem(e)}</li>`).join("");
}

refresh();                     // initial load
setInterval(refresh, 15000);    // every 15 s
