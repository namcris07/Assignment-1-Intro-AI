const CELL_SIZE = 70;
const GRID_SIZE = 5;
const BOARD_SIZE = CELL_SIZE * GRID_SIZE;
const DIRS = { 0: [1, 0], 90: [0, 1], 180: [-1, 0], 270: [0, -1] };

const canvas = document.getElementById("board");
const ctx = canvas.getContext("2d");

let levels = [];
let solvedPath = [];
let currentStep = 0;
let initialState = null;

// --- Vẽ bảng ---
function getAngles(pipeType, heading) {
  if (pipeType === 1) return [heading];
  if (pipeType === 2) return [heading, (heading + 180) % 360];
  if (pipeType === 3) return [heading, (heading + 90) % 360];
  if (pipeType === 4) return [(heading - 90 + 360) % 360, heading, (heading + 90) % 360];
}

function drawBoard(stateMatrix) {
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, BOARD_SIZE, BOARD_SIZE);
  drawGrid();
  for (let r = 0; r < GRID_SIZE; r++) {
    for (let c = 0; c < GRID_SIZE; c++) {
      drawPipe(r, c, stateMatrix[r][c]);
    }
  }
}

function drawGrid() {
  ctx.strokeStyle = "#e2e8f0";
  ctx.setLineDash([2, 2]);
  ctx.lineWidth = 1;
  for (let i = 0; i <= GRID_SIZE; i++) {
    const pos = i * CELL_SIZE;
    ctx.beginPath();
    ctx.moveTo(pos, 0);
    ctx.lineTo(pos, BOARD_SIZE);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(0, pos);
    ctx.lineTo(BOARD_SIZE, pos);
    ctx.stroke();
  }
  ctx.setLineDash([]);
}

function drawPipe(row, col, pipeData) {
  const pipeType = pipeData.type;
  const heading = pipeData.heading;
  const isBump = pipeData.bump || false;
  const renderRow = (GRID_SIZE - 1) - row;
  const cx = col * CELL_SIZE + CELL_SIZE / 2;
  const cy = renderRow * CELL_SIZE + CELL_SIZE / 2;
  const pipeColor = isBump ? "#22d3ee" : "#f1f5f9";
  const outlineColor = "#475569";
  const pipeWidth = 16;
  const outlineWidth = 24;
  const rDot = Math.floor(outlineWidth / 1.5);
  const angles = getAngles(pipeType, heading);

  for (const a of angles) {
    const [dx, dy] = DIRS[a];
    const ex = cx + dx * (CELL_SIZE / 2);
    const ey = cy + dy * (CELL_SIZE / 2);
    ctx.strokeStyle = outlineColor;
    ctx.lineWidth = outlineWidth;
    ctx.lineCap = "butt";
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(ex, ey);
    ctx.stroke();
  }
  if (angles.length >= 2) {
    const rOut = outlineWidth / 2;
    ctx.fillStyle = outlineColor;
    ctx.fillRect(cx - rOut, cy - rOut, outlineWidth, outlineWidth);
  }
  if (isBump) {
    ctx.shadowColor = "rgba(34, 211, 238, 0.6)";
    ctx.shadowBlur = 6;
  }
  for (const a of angles) {
    const [dx, dy] = DIRS[a];
    const ex = cx + dx * (CELL_SIZE / 2);
    const ey = cy + dy * (CELL_SIZE / 2);
    ctx.strokeStyle = pipeColor;
    ctx.lineWidth = pipeWidth;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(ex, ey);
    ctx.stroke();
  }
  ctx.shadowBlur = 0;
  if (angles.length >= 2) {
    const rIn = pipeWidth / 2;
    ctx.fillStyle = pipeColor;
    ctx.fillRect(cx - rIn, cy - rIn, pipeWidth, pipeWidth);
  }
  if (pipeType === 1) {
    ctx.fillStyle = pipeColor;
    ctx.strokeStyle = outlineColor;
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.arc(cx, cy, rDot, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  }
  if (row === 2 && col === 2) {
    ctx.shadowBlur = 0;
    ctx.shadowColor = "rgba(244, 63, 94, 0.5)";
    ctx.shadowBlur = 8;
    ctx.fillStyle = "#f43f5e";
    ctx.strokeStyle = "#e11d48";
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.arc(cx, cy, rDot, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.shadowBlur = 0;
  }
}

// --- API ---
async function loadLevels() {
  const res = await fetch("/api/levels");
  levels = await res.json();
  const sel = document.getElementById("level");
  sel.innerHTML = levels.map(l => `<option value="${l}">${l}</option>`).join("");
}

async function loadInitial() {
  const level = document.getElementById("level").value;
  const res = await fetch(`/api/initial/${encodeURIComponent(level)}`);
  if (!res.ok) return;
  initialState = await res.json();
  drawBoard(initialState);
}

async function solve() {
  const level = document.getElementById("level").value;
  const algorithm = document.getElementById("algo").value;
  setStatus("Đang giải...", "running");
  document.getElementById("btn-solve").disabled = true;
  document.getElementById("nodes-info").textContent = "—";
  document.getElementById("time-info").textContent = "—";
  document.getElementById("memory-info").textContent = "—";

  try {
    const res = await fetch("/api/solve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ level, algorithm }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Lỗi API");

    document.getElementById("nodes-info").textContent = data.states_explored;
    document.getElementById("time-info").textContent = data.time_ms.toFixed(2) + " ms";
    document.getElementById("memory-info").textContent = data.memory_mb.toFixed(4) + " MB";

    if (data.success && data.path && data.path.length > 0) {
      solvedPath = data.path;
      currentStep = 0;
      document.getElementById("step-info").textContent = `0 / ${solvedPath.length - 1}`;
      document.getElementById("btn-prev").disabled = true;
      document.getElementById("btn-next").disabled = solvedPath.length <= 1;

      const animate = document.getElementById("animate").checked;
      const speed = parseInt(document.getElementById("speed").value);

      if (animate) {
        animatePath(0, speed);
      } else {
        drawBoard(solvedPath[solvedPath.length - 1]);
        document.getElementById("step-info").textContent = `${solvedPath.length - 1} / ${solvedPath.length - 1}`;
        document.getElementById("btn-prev").disabled = false;
        document.getElementById("btn-next").disabled = true;
        setStatus("Hoàn thành!", "done");
      }
    } else {
      drawBoard(initialState);
      setStatus("Không tìm thấy lời giải", "error");
    }
  } catch (e) {
    setStatus("Lỗi: " + e.message, "error");
    if (initialState) drawBoard(initialState);
  } finally {
    document.getElementById("btn-solve").disabled = false;
  }
}

function animatePath(index, speed) {
  if (index >= solvedPath.length) {
    document.getElementById("btn-next").disabled = true;
    setStatus("Hoàn thành!", "done");
    return;
  }
  currentStep = index;
  drawBoard(solvedPath[index]);
  document.getElementById("step-info").textContent = `${index} / ${solvedPath.length - 1}`;
  document.getElementById("btn-prev").disabled = index <= 0;
  document.getElementById("btn-next").disabled = index >= solvedPath.length - 1;
  setTimeout(() => animatePath(index + 1, speed), speed);
}

function setStatus(text, cls) {
  const pill = document.getElementById("status");
  const textEl = pill.querySelector(".status-text");
  if (textEl) textEl.textContent = text;
  pill.className = "status-pill " + (cls || "ready");
}

function prevStep() {
  if (!solvedPath.length || currentStep <= 0) return;
  currentStep--;
  drawBoard(solvedPath[currentStep]);
  document.getElementById("step-info").textContent = `${currentStep} / ${solvedPath.length - 1}`;
  document.getElementById("btn-prev").disabled = currentStep <= 0;
  document.getElementById("btn-next").disabled = false;
}

function nextStep() {
  if (!solvedPath.length || currentStep >= solvedPath.length - 1) return;
  currentStep++;
  drawBoard(solvedPath[currentStep]);
  document.getElementById("step-info").textContent = `${currentStep} / ${solvedPath.length - 1}`;
  document.getElementById("btn-prev").disabled = false;
  document.getElementById("btn-next").disabled = currentStep >= solvedPath.length - 1;
}

function reset() {
  solvedPath = [];
  currentStep = 0;
  document.getElementById("step-info").textContent = "0 / 0";
  document.getElementById("nodes-info").textContent = "—";
  document.getElementById("time-info").textContent = "—";
  document.getElementById("memory-info").textContent = "—";
  document.getElementById("btn-prev").disabled = true;
  document.getElementById("btn-next").disabled = true;
  loadInitial().catch(() => {});
  setStatus("Sẵn sàng", "ready");
}

// --- Init ---
document.getElementById("btn-solve").addEventListener("click", solve);
document.getElementById("btn-reset").addEventListener("click", reset);
document.getElementById("btn-prev").addEventListener("click", prevStep);
document.getElementById("btn-next").addEventListener("click", nextStep);
document.getElementById("level").addEventListener("change", reset);
document.getElementById("speed").addEventListener("input", e => {
  document.getElementById("speed-val").textContent = e.target.value;
});

loadLevels().then(() => {
  loadInitial();
});
