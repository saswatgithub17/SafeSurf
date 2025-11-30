// --- LOGIC 1: IGNORE IFRAMES ---
// Only run on the main page, not inside ads or invisible frames
if (window !== window.top) {
    throw new Error("Phishing Guard: Skipping iframe");
}

const currentUrl = window.location.href;
const hostname = window.location.hostname;

// --- LOGIC 2: IGNORE SEARCH ENGINES ---
// We don't want to block the user while they are just searching on Google/Bing
const safeSearchEngines = [
    "google.com",
    "www.google.com",
    "bing.com",
    "www.bing.com",
    "yahoo.com",
    "www.yahoo.com",
    "duckduckgo.com",
    "baidu.com"
];

// Check if the current site is a search engine
const isSearchEngine = safeSearchEngines.some(engine => hostname.includes(engine));

// Special check: If it's Google Forms or Drive, we MIGHT want to scan it (phishing happens there),
// so only skip if it's strictly the search engine part.
// For simplicity, if it is a generic search engine domain, we skip.
if (isSearchEngine) {
    console.log("Phishing Guard: Search Engine detected. Skipping scan.");
    // We simply stop the script here so no popup is created
    throw new Error("Phishing Guard: Skipping Search Engine");
}

// =========================================================
// IF WE PASSED THE CHECKS ABOVE, START THE BLOCKER
// =========================================================

// 1. Create the Blocking Overlay immediately
const overlay = document.createElement('div');
overlay.id = 'phishing-guard-overlay';
overlay.innerHTML = `
    <div class="guard-box">
        <div class="loader"></div>
        <div class="status-text">Analyzing Website Safety...</div>
        <p style="margin-top:10px; color:#666; font-size:12px;">Please wait while we scan this URL.</p>
    </div>
`;
document.documentElement.appendChild(overlay);

// 2. Send URL to our Local Python Server
fetch('http://127.0.0.1:5000/analyze', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url: currentUrl })
})
.then(response => response.json())
.then(data => {
    const statusText = overlay.querySelector('.status-text');
    const loader = overlay.querySelector('.loader');

    if (data.status === "SAFE") {
        // success animation
        statusText.innerText = "Website is Safe.";
        statusText.style.color = "green";
        loader.style.borderTop = "5px solid green";
        
        // Remove overlay fast
        setTimeout(() => {
            overlay.remove();
        }, 500); // 0.5 seconds
    } else {
        // BLOCK ACCESS
        statusText.innerText = "WARNING: PHISHING DETECTED!";
        statusText.style.color = "red";
        loader.style.display = "none";
        
        const msg = document.createElement('p');
        msg.innerText = "This site has been identified as a phishing scam. Access is blocked.";
        msg.style.color = "red";
        msg.style.marginTop = "10px";
        msg.style.fontWeight = "bold";
        document.querySelector('.guard-box').appendChild(msg);
        
        // Change background to red warning
        overlay.style.backgroundColor = "rgba(100, 0, 0, 0.95)";
    }
})
.catch(error => {
    console.error('Error connecting to analysis server:', error);
    // If server is down, decide if you want to block or let through.
    // Usually for safety, we let through with a warning or remove overlay.
    overlay.querySelector('.status-text').innerText = "Analysis Failed (Server Offline?)";
    setTimeout(() => {
        overlay.remove();
    }, 2000);
});