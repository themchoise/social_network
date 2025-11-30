// Static version of gamification.js moved from templates/components

/* Original content preserved */

class GamificationModal {
  constructor() {
    this.modalContainer = null;
    this.overlayContainer = null;
    this.currentTimeout = null;
  }
  init() {
    this.createContainers();
  }
  createContainers() {
    this.overlayContainer = document.createElement("div");
    this.overlayContainer.id = "points-overlay";
    this.overlayContainer.className = "points-modal-overlay";
    this.overlayContainer.style.display = "none";
    document.body.appendChild(this.overlayContainer);
    this.modalContainer = document.createElement("div");
    this.modalContainer.id = "points-modal";
    this.modalContainer.className = "points-modal";
    this.modalContainer.style.display = "none";
    document.body.appendChild(this.modalContainer);
    this.overlayContainer.addEventListener("click", () => this.hide());
  }
  show(data) {
    if (!this.modalContainer) {
      this.init();
    }
    if (this.currentTimeout) {
      clearTimeout(this.currentTimeout);
    }
    const {
      points = 0,
      source = "",
      total_points = 0,
      level = 1,
      level_up = false,
      description = "",
      achievements_unlocked = [],
    } = data;
    let html = `<div class="points-icon">${this.getSourceIcon(
      source
    )}</div><div class="points-amount">+${points}</div><div class="points-description">${
      description || this.getSourceDescription(source)
    }</div>`;
    if (level_up) {
      html += `<div class="level-up-badge">🎉 ¡LEVEL UP! Nivel ${level}</div>`;
    }
    if (achievements_unlocked && achievements_unlocked.length > 0) {
      achievements_unlocked.forEach((achievement) => {
        if (achievement.achievement) {
          const ach = achievement.achievement;
          html += `<div class="achievement-badge"><span class="achievement-badge-icon">${
            ach.icon || "🏆"
          }</span><span class="achievement-badge-name">${
            ach.name
          }</span></div>`;
        }
      });
    }
    html += `<div class="points-total">Total: <strong>${total_points}</strong> puntos</div>`;
    this.modalContainer.innerHTML = html;
    this.overlayContainer.style.display = "block";
    this.modalContainer.style.display = "block";
    this.modalContainer.classList.add("show");
    this.modalContainer.classList.remove("hide");
    this.createConfetti();
    this.currentTimeout = setTimeout(() => this.hide(), 3000);
  }
  hide() {
    if (!this.modalContainer) return;
    this.modalContainer.classList.add("hide");
    this.modalContainer.classList.remove("show");
    this.overlayContainer.classList.add("hide");
    setTimeout(() => {
      this.overlayContainer.style.display = "none";
      this.modalContainer.style.display = "none";
      this.overlayContainer.classList.remove("hide");
    }, 500);
  }
  getSourceIcon(source) {
    const icons = {
      post: "📝",
      comment: "💬",
      like_received: "❤️",
      note_shared: "📌",
      achievement: "🏆",
      login_streak: "🔥",
      help_others: "🤝",
      admin_bonus: "🎁",
    };
    return icons[source] || "⭐";
  }
  getSourceDescription(source) {
    const descriptions = {
      post: "¡Nuevo post creado!",
      comment: "¡Nuevo comentario!",
      like_received: "¡Te dieron un like!",
      note_shared: "¡Nota compartida!",
      achievement: "¡Logro desbloqueado!",
      login_streak: "¡Streak activo!",
      help_others: "¡Ayudaste a otros!",
      admin_bonus: "¡Bonificación del admin!",
    };
    return descriptions[source] || "Puntos obtenidos";
  }
  createConfetti() {
    const confettiPieces = 30;
    for (let i = 0; i < confettiPieces; i++) {
      const confetti = document.createElement("div");
      confetti.className = "confetti";
      confetti.textContent = ["🎉", "⭐", "✨", "🎊"][
        Math.floor(Math.random() * 4)
      ];
      const tx = (Math.random() - 0.5) * 300;
      const ty = Math.random() * 200 + 100;
      confetti.style.setProperty("--tx", `${tx}px`);
      confetti.style.setProperty("--ty", `${ty}px`);
      confetti.style.left = window.innerWidth / 2 + "px";
      confetti.style.top = window.innerHeight / 2 + "px";
      confetti.style.fontSize = Math.random() * 20 + 16 + "px";
      document.body.appendChild(confetti);
      setTimeout(() => confetti.remove(), 3000);
    }
  }
}
class PointsNotification {
  static show(message, points, icon = "⭐") {
    const n = document.createElement("div");
    n.className = "points-notification";
    n.innerHTML = `<div class="points-notification-title">${icon} +${points} puntos</div><div class="points-notification-message">${message}</div>`;
    document.body.appendChild(n);
    setTimeout(() => {
      n.classList.add("hide");
      setTimeout(() => n.remove(), 400);
    }, 3000);
  }
}
class GamificationAPI {
  static baseURL = "/api/";
  static async awardPoints(source, points = null, description = null) {
    try {
      const response = await fetch(`${this.baseURL}award-points/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": this.getCSRFToken(),
        },
        body: JSON.stringify({ source, points, description }),
      });
      if (!response.ok)
        throw new Error(`HTTP error! status: ${response.status}`);
      return await response.json();
    } catch (e) {
      console.error("Error awarding points:", e);
      throw e;
    }
  }
  static async getUserStats() {
    try {
      const r = await fetch(`${this.baseURL}user-stats/`);
      if (!r.ok) throw new Error(`HTTP error! status: ${r.status}`);
      return await r.json();
    } catch (e) {
      console.error("Error getting user stats:", e);
      throw e;
    }
  }
  static async getUserAchievements() {
    try {
      const r = await fetch(`${this.baseURL}user-achievements/`);
      if (!r.ok) throw new Error(`HTTP error! status: ${r.status}`);
      return await r.json();
    } catch (e) {
      console.error("Error getting achievements:", e);
      throw e;
    }
  }
  static async getPointsHistory(limit = 20) {
    try {
      const r = await fetch(`${this.baseURL}points-history/?limit=${limit}`);
      if (!r.ok) throw new Error(`HTTP error! status: ${r.status}`);
      return await r.json();
    } catch (e) {
      console.error("Error getting points history:", e);
      throw e;
    }
  }
  static async checkAchievements() {
    try {
      const r = await fetch(`${this.baseURL}check-achievements/`, {
        method: "POST",
        headers: { "X-CSRFToken": this.getCSRFToken() },
      });
      if (!r.ok) throw new Error(`HTTP error! status: ${r.status}`);
      return await r.json();
    } catch (e) {
      console.error("Error checking achievements:", e);
      throw e;
    }
  }
  static async getLeaderboard(limit = 50) {
    try {
      const r = await fetch(`${this.baseURL}leaderboard/?limit=${limit}`);
      if (!r.ok) throw new Error(`HTTP error! status: ${r.status}`);
      return await r.json();
    } catch (e) {
      console.error("Error getting leaderboard:", e);
      throw e;
    }
  }
  static getCSRFToken() {
    const token = document.querySelector("[name=csrfmiddlewaretoken]");
    if (token) return token.value;
    return (
      document
        .querySelector('meta[name="csrf-token"]')
        ?.getAttribute("content") || ""
    );
  }
}
class Leaderboard {
  constructor(sel = "#leaderboard") {
    this.container = document.querySelector(sel);
    this.data = null;
  }
  async load(limit = 50) {
    try {
      this.data = await GamificationAPI.getLeaderboard(limit);
      this.render();
    } catch (e) {
      console.error("Error loading leaderboard:", e);
      if (this.container) {
        this.container.innerHTML =
          '<p class="error">Error al cargar el ranking</p>';
      }
    }
  }
  render() {
    if (!this.container || !this.data) return;
    let html = '<div class="leaderboard-container">';
    this.data.leaderboard.forEach((user, index) => {
      const medal =
        index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : "•";
      html += `<div class="leaderboard-item"><div class="leaderboard-rank top-${
        index + 1
      }">${medal}</div><div class="leaderboard-info"><div class="leaderboard-username">${
        user.username
      }</div><div class="leaderboard-meta">${user.posts} posts • ${
        user.achievements
      } logros</div></div><div class="leaderboard-points"><div class="leaderboard-points-value">${
        user.total_points
      }</div><div class="leaderboard-level">Nivel ${
        user.level
      }</div></div></div>`;
    });
    html += "</div>";
    this.container.innerHTML = html;
  }
  async refresh(limit = 50) {
    await this.load(limit);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.gamificationModal = new GamificationModal();
  window.gamificationModal.init();
  window.gamificationAPI = GamificationAPI;
  window.PointsNotification = PointsNotification;
  window.Leaderboard = Leaderboard;
});

async function awardPoints(source, points = null, description = null) {
  try {
    const result = await GamificationAPI.awardPoints(
      source,
      points,
      description
    );
    if (result.success) {
      gamificationModal.show(result);
    } else {
      console.error("Error:", result.error);
    }
  } catch (e) {
    console.error("Error awarding points:", e);
  }
}
