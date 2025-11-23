/**
 * Sistema de Gamificación - Modal de Puntos
 * Maneja la visualización de puntos obtenidos y logros desbloqueados
 */

class GamificationModal {
  constructor() {
    this.modalContainer = null;
    this.overlayContainer = null;
    this.currentTimeout = null;
  }

  /**
   * Inicializa el sistema de gamificación
   */
  init() {
    this.createContainers();
    console.log("Sistema de gamificación inicializado");
  }

  /**
   * Crea los contenedores del modal y overlay
   */
  createContainers() {
    // Crear overlay
    this.overlayContainer = document.createElement("div");
    this.overlayContainer.id = "points-overlay";
    this.overlayContainer.className = "points-modal-overlay";
    this.overlayContainer.style.display = "none";
    document.body.appendChild(this.overlayContainer);

    // Crear modal
    this.modalContainer = document.createElement("div");
    this.modalContainer.id = "points-modal";
    this.modalContainer.className = "points-modal";
    this.modalContainer.style.display = "none";
    document.body.appendChild(this.modalContainer);

    // Cerrar al hacer click en overlay
    this.overlayContainer.addEventListener("click", () => this.hide());
  }

  /**
   * Muestra el modal con la información de puntos
   * @param {Object} data - Datos de puntos y logros
   */
  show(data) {
    if (!this.modalContainer) {
      this.init();
    }

    // Limpiar timeout anterior
    if (this.currentTimeout) {
      clearTimeout(this.currentTimeout);
    }

    const {
      points = 0,
      source = "",
      total_points = 0,
      level = 1,
      level_up = false,
      level_change = 0,
      description = "",
      achievements_unlocked = [],
    } = data;

    let html = `
            <div class="points-icon">
                ${this.getSourceIcon(source)}
            </div>
            <div class="points-amount">+${points}</div>
            <div class="points-description">${
              description || this.getSourceDescription(source)
            }</div>
        `;

    if (level_up) {
      html += `
                <div class="level-up-badge">
                    🎉 ¡LEVEL UP! Nivel ${level}
                </div>
            `;
    }

    if (achievements_unlocked && achievements_unlocked.length > 0) {
      achievements_unlocked.forEach((achievement) => {
        if (achievement.achievement) {
          const ach = achievement.achievement;
          html += `
                        <div class="achievement-badge">
                            <span class="achievement-badge-icon">${
                              ach.icon || "🏆"
                            }</span>
                            <span class="achievement-badge-name">${
                              ach.name
                            }</span>
                        </div>
                    `;
        }
      });
    }

    html += `
            <div class="points-total">
                Total: <strong>${total_points}</strong> puntos
            </div>
        `;

    this.modalContainer.innerHTML = html;
    this.overlayContainer.style.display = "block";
    this.modalContainer.style.display = "block";

    this.modalContainer.classList.add("show");
    this.modalContainer.classList.remove("hide");

    // Crear confeti
    this.createConfetti();

    // Auto cerrar después de 3 segundos
    this.currentTimeout = setTimeout(() => this.hide(), 3000);
  }

  /**
   * Cierra el modal
   */
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

  /**
   * Obtiene el ícono según la fuente de puntos
   * @param {string} source - Fuente de puntos
   * @returns {string} HTML del ícono
   */
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

  /**
   * Obtiene la descripción según la fuente
   * @param {string} source - Fuente de puntos
   * @returns {string} Descripción
   */
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

  /**
   * Crea animación de confeti
   */
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

/**
 * Clase para mostrar notificaciones flotantes de puntos
 */
class PointsNotification {
  static show(message, points, icon = "⭐") {
    const notification = document.createElement("div");
    notification.className = "points-notification";
    notification.innerHTML = `
            <div class="points-notification-title">${icon} +${points} puntos</div>
            <div class="points-notification-message">${message}</div>
        `;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.classList.add("hide");
      setTimeout(() => notification.remove(), 400);
    }, 3000);
  }
}

/**
 * Clase para gestionar llamadas a la API de gamificación
 */
class GamificationAPI {
  static baseURL = "/api/";

  /**
   * Otorga puntos a través de la API
   * @param {string} source - Fuente de puntos
   * @param {number} points - Cantidad de puntos (opcional)
   * @param {string} description - Descripción (opcional)
   * @returns {Promise}
   */
  static async awardPoints(source, points = null, description = null) {
    try {
      const response = await fetch(`${this.baseURL}award-points/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": this.getCSRFToken(),
        },
        body: JSON.stringify({
          source,
          points,
          description,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error("Error awarding points:", error);
      throw error;
    }
  }

  /**
   * Obtiene estadísticas del usuario
   * @returns {Promise}
   */
  static async getUserStats() {
    try {
      const response = await fetch(`${this.baseURL}user-stats/`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Error getting user stats:", error);
      throw error;
    }
  }

  /**
   * Obtiene logros del usuario
   * @returns {Promise}
   */
  static async getUserAchievements() {
    try {
      const response = await fetch(`${this.baseURL}user-achievements/`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Error getting achievements:", error);
      throw error;
    }
  }

  /**
   * Obtiene historial de puntos
   * @param {number} limit - Cantidad máxima de registros
   * @returns {Promise}
   */
  static async getPointsHistory(limit = 20) {
    try {
      const response = await fetch(
        `${this.baseURL}points-history/?limit=${limit}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Error getting points history:", error);
      throw error;
    }
  }

  /**
   * Verifica y desbloquea logros
   * @returns {Promise}
   */
  static async checkAchievements() {
    try {
      const response = await fetch(`${this.baseURL}check-achievements/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": this.getCSRFToken(),
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Error checking achievements:", error);
      throw error;
    }
  }

  /**
   * Obtiene el ranking de usuarios
   * @param {number} limit - Cantidad máxima de usuarios
   * @returns {Promise}
   */
  static async getLeaderboard(limit = 50) {
    try {
      const response = await fetch(
        `${this.baseURL}leaderboard/?limit=${limit}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Error getting leaderboard:", error);
      throw error;
    }
  }

  /**
   * Obtiene el token CSRF del DOM
   * @returns {string}
   */
  static getCSRFToken() {
    const token = document.querySelector("[name=csrfmiddlewaretoken]");
    if (token) {
      return token.value;
    }
    return (
      document
        .querySelector('meta[name="csrf-token"]')
        ?.getAttribute("content") || ""
    );
  }
}

/**
 * Clase para mostrar el leaderboard
 */
class Leaderboard {
  constructor(containerSelector = "#leaderboard") {
    this.container = document.querySelector(containerSelector);
    this.data = null;
  }

  /**
   * Carga y muestra el leaderboard
   * @param {number} limit - Cantidad máxima de usuarios
   */
  async load(limit = 50) {
    try {
      this.data = await GamificationAPI.getLeaderboard(limit);
      this.render();
    } catch (error) {
      console.error("Error loading leaderboard:", error);
      if (this.container) {
        this.container.innerHTML =
          '<p class="error">Error al cargar el ranking</p>';
      }
    }
  }

  /**
   * Renderiza el leaderboard
   */
  render() {
    if (!this.container || !this.data) return;

    let html = '<div class="leaderboard-container">';

    this.data.leaderboard.forEach((user, index) => {
      const medalEmoji =
        index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : "•";
      html += `
                <div class="leaderboard-item">
                    <div class="leaderboard-rank top-${
                      index + 1
                    }">${medalEmoji}</div>
                    <div class="leaderboard-info">
                        <div class="leaderboard-username">${user.username}</div>
                        <div class="leaderboard-meta">
                            ${user.posts} posts • ${user.achievements} logros
                        </div>
                    </div>
                    <div class="leaderboard-points">
                        <div class="leaderboard-points-value">${
                          user.total_points
                        }</div>
                        <div class="leaderboard-level">Nivel ${user.level}</div>
                    </div>
                </div>
            `;
    });

    html += "</div>";
    this.container.innerHTML = html;
  }

  /**
   * Actualiza el leaderboard
   */
  async refresh(limit = 50) {
    await this.load(limit);
  }
}

/**
 * Inicialización global
 */
document.addEventListener("DOMContentLoaded", () => {
  // Crear instancia global del modal
  window.gamificationModal = new GamificationModal();
  window.gamificationModal.init();

  // Hacer disponible la API globalmente
  window.gamificationAPI = GamificationAPI;
  window.PointsNotification = PointsNotification;
  window.Leaderboard = Leaderboard;
});

/**
 * Función auxiliar para otorgar puntos (uso simplificado)
 * @param {string} source - Fuente de puntos
 * @param {number} points - Cantidad de puntos (opcional)
 * @param {string} description - Descripción (opcional)
 */
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
  } catch (error) {
    console.error("Error awarding points:", error);
  }
}
