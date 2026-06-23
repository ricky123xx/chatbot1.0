/* ═════════════════════════════════════════
   OIBSIP — Nova AI Chatbot  |  script.js
═════════════════════════════════════════ */
"use strict";

/* ── REFS ── */
const messagesEl  = document.getElementById("messages");
const inputEl     = document.getElementById("user-input");
const sendBtn     = document.getElementById("send-btn");
const clearBtn    = document.getElementById("clear-btn");
const typingBar   = document.getElementById("typing-bar");
const charCount   = document.getElementById("char-count");
const themeToggle = document.getElementById("theme-toggle");
const themeIcon   = document.getElementById("theme-icon");
const html        = document.documentElement;

/* ── THEME ── */
const savedTheme = localStorage.getItem("nova-theme") || "dark";
html.setAttribute("data-theme", savedTheme);
themeIcon.textContent = savedTheme === "dark" ? "☀️" : "🌙";

themeToggle.addEventListener("click", () => {
  const current = html.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  html.setAttribute("data-theme", next);
  themeIcon.textContent = next === "dark" ? "☀️" : "🌙";
  localStorage.setItem("nova-theme", next);
});

/* ── PARTICLE BACKGROUND ── */
(function initParticles() {
  const canvas = document.getElementById("particles");
  const ctx    = canvas.getContext("2d");
  let W, H, particles;

  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }

  function createParticles(n) {
    return Array.from({ length: n }, () => ({
      x:  Math.random() * W,
      y:  Math.random() * H,
      r:  Math.random() * 1.5 + 0.5,
      dx: (Math.random() - 0.5) * 0.25,
      dy: (Math.random() - 0.5) * 0.25,
      o:  Math.random() * 0.5 + 0.1,
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    particles.forEach((p) => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(99,102,241,${p.o})`;
      ctx.fill();
      p.x += p.dx;
      p.y += p.dy;
      if (p.x < 0 || p.x > W) p.dx *= -1;
      if (p.y < 0 || p.y > H) p.dy *= -1;
    });
    requestAnimationFrame(draw);
  }

  resize();
  particles = createParticles(80);
  draw();
  window.addEventListener("resize", () => { resize(); particles = createParticles(80); });
})();

/* ── WELCOME MESSAGE ── */
function showWelcome() {
  messagesEl.innerHTML = `
    <div class="welcome-msg">
      <span class="w-icon">🤖</span>
      <p><strong>Hi! I'm Nova</strong> — your AI assistant.</p>
      <p class="w-hint">Try: "Tell me a joke" · "What is Python?" · "Calculate 12 * 8"</p>
    </div>`;
}
showWelcome();

/* ── RENDER MARKDOWN-LITE (bold **text**) ── */
function renderText(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
    .replace(/`(.+?)`/g, '<code>$1</code>');
}

/* ── ADD A MESSAGE BUBBLE ── */
function addMessage(text, role, time) {
  // Remove welcome card if present
  const welcome = messagesEl.querySelector(".welcome-msg");
  if (welcome) welcome.remove();

  const row = document.createElement("div");
  row.className = `msg-row ${role}`;

  const avatarLetter = role === "bot" ? "N" : "A";
  const avatarClass  = role === "bot" ? "bot-av" : "user-av";
  const bubbleClass  = role === "bot" ? "bot"    : "user";

  row.innerHTML = `
    <div class="msg-avatar ${avatarClass}">${avatarLetter}</div>
    <div class="msg-body">
      <div class="bubble ${bubbleClass}">
        ${renderText(text)}
        <button class="copy-bubble-btn" title="Copy">Copy</button>
      </div>
      <div class="msg-time">${time || nowTime()}</div>
    </div>`;

  // Copy button
  row.querySelector(".copy-bubble-btn").addEventListener("click", function () {
    navigator.clipboard.writeText(text).then(() => {
      this.textContent = "✓ Copied";
      setTimeout(() => { this.textContent = "Copy"; }, 1800);
    });
  });

  messagesEl.appendChild(row);
  scrollBottom();
}

/* ── SCROLL TO BOTTOM ── */
function scrollBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

/* ── CURRENT TIME ── */
function nowTime() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

/* ── SEND MESSAGE ── */
async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;

  addMessage(text, "user");
  inputEl.value = "";
  inputEl.style.height = "auto";
  charCount.textContent = "0 / 500";
  sendBtn.disabled = true;

  // Show typing indicator
  typingBar.style.display = "flex";
  scrollBottom();

  // Simulate realistic typing delay
  const delay = Math.min(600 + text.length * 12, 2200);

  try {
    const res  = await fetch("/chat", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ message: text }),
    });
    const data = await res.json();

    await new Promise((r) => setTimeout(r, delay));
    typingBar.style.display = "none";

    if (res.ok) {
      addMessage(data.response, "bot", data.timestamp);
    } else {
      addMessage(data.error || "Something went wrong. Please try again.", "bot");
    }
  } catch {
    await new Promise((r) => setTimeout(r, 600));
    typingBar.style.display = "none";
    addMessage("⚠️ Connection error — make sure the Flask server is running.", "bot");
  } finally {
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

/* ── QUICK CHIP SEND (from hero) ── */
window.sendQuick = function (text) {
  document.getElementById("chat").scrollIntoView({ behavior: "smooth" });
  setTimeout(() => {
    inputEl.value = text;
    charCount.textContent = `${text.length} / 500`;
    sendMessage();
  }, 400);
};

/* ── CLEAR CHAT ── */
clearBtn.addEventListener("click", async () => {
  try { await fetch("/clear", { method: "POST" }); } catch { /* ignore */ }
  showWelcome();
});

/* ── SEND ON BUTTON / ENTER ── */
sendBtn.addEventListener("click", sendMessage);

inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

/* ── AUTO-RESIZE TEXTAREA + CHAR COUNT ── */
inputEl.addEventListener("input", () => {
  inputEl.style.height = "auto";
  inputEl.style.height = Math.min(inputEl.scrollHeight, 120) + "px";
  charCount.textContent = `${inputEl.value.length} / 500`;
  charCount.style.color = inputEl.value.length > 450
    ? "var(--red)" : "var(--dimmed)";
});

/* ── FOCUS INPUT ON LOAD ── */
inputEl.focus();
