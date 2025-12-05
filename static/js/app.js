// Aplicación principal
console.log("[app.js] archivo cargado");
document.addEventListener("DOMContentLoaded", function () {
  console.log("Red Social IFTS cargada!");
  initializeApp();
  initToasts();
  forceRestoreOpacity();
  setTimeout(forceRestoreOpacity, 500);
  setTimeout(forceRestoreOpacity, 1500);
});

function initializeApp() {
  // Configurar enlaces activos en sidebar
  setActiveSidebarLink();

  // Configurar auto-hide de mensajes
  autoHideMessages();

  // Configurar formularios AJAX
  setupAjaxForms();
}

function initToasts() {
  const toasts = document.querySelectorAll("[data-toast]");
  toasts.forEach((t) => {
    t.classList.add("fade-in");
    setTimeout(() => {
      t.style.transition = "opacity .5s";
      t.style.opacity = "0";
      setTimeout(() => t.remove(), 500);
    }, 5000);
  });
}

function setActiveSidebarLink() {
  const currentPath = window.location.pathname;
  const sidebarLinks = document.querySelectorAll(".sidebar-link");

  sidebarLinks.forEach((link) => {
    link.classList.remove("active");
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
    }
  });
}

function autoHideMessages() {
  const messages = document.querySelectorAll(".flash-message");
  messages.forEach((message) => {
    if (message.textContent.trim()) {
      // Usar clases para animación en vez de inline opacity masiva
      setTimeout(() => {
        message.classList.add("flash-fade-out");
        setTimeout(() => message.remove(), 500);
      }, 5000);
    }
  });
}

function setupAjaxForms() {
  // Configurar formularios que no requieren recarga de página
  const ajaxForms = document.querySelectorAll('[data-ajax="true"]');

  ajaxForms.forEach((form) => {
    form.addEventListener("submit", handleAjaxSubmit);
  });
}

function handleAjaxSubmit(event) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);
  const url = form.action || window.location.pathname;

  fetch(url, {
    method: "POST",
    body: formData,
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        showNotification("Operación exitosa", "success");
        if (data.reload) {
          window.location.reload();
        }
      } else {
        showNotification(data.error || "Error en la operación", "error");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      showNotification("Error de conexión", "error");
    });
}

function showNotification(message, type = "info") {
  const notification = document.createElement("div");
  notification.className = `fixed top-20 right-4 p-4 rounded-md shadow-lg z-50 ${getNotificationClasses(
    type
  )}`;
  notification.textContent = message;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.transition = "opacity 0.5s, transform 0.5s";
    notification.style.opacity = "0";
    notification.style.transform = "translateX(100%)";
    setTimeout(() => notification.remove(), 500);
  }, 3000);
}

function getNotificationClasses(type) {
  const classes = {
    success: "bg-green-50 text-green-700 border border-green-200",
    error: "bg-red-50 text-red-700 border border-red-200",
    warning: "bg-yellow-50 text-yellow-700 border border-yellow-200",
    info: "bg-blue-50 text-blue-700 border border-blue-200",
  };
  return classes[type] || classes.info;
}

// Fuerza restaurar opacidad si algún script externo dejó elementos invisibles
function forceRestoreOpacity() {
  try {
    const root = document.documentElement;
    if (root && root.style.opacity === "0") {
      console.warn("[app.js] Root tenía opacity 0. Restaurando a 1");
      root.style.opacity = "1";
      root.style.transition = "none";
    }
    const hiddenByOpacity = document.querySelectorAll('[style*="opacity: 0"]');
    hiddenByOpacity.forEach((el) => {
      // Evitar tocar overlays que sí deben ocultarse (modal gamificación cuando está cerrado)
      if (!el.id || (el.id !== "points-overlay" && el.id !== "points-modal")) {
        // Solo si no hay animación en curso (heurística simple)
        if (el.style.opacity === "0") {
          el.style.opacity = "1";
          el.style.transition = "none";
          el.dataset.restoredOpacity = "true";
        }
      }
    });
    ensureObserver();
  } catch (e) {
    console.error("[app.js] Error restaurando opacidad", e);
  }
}

// Observa cambios futuros que intenten poner opacity:0
let opacityObserver;
function ensureObserver() {
  if (opacityObserver) return;
  const captured = new WeakSet();
  opacityObserver = new MutationObserver((mutations) => {
    mutations.forEach((m) => {
      if (m.type === "attributes" && m.attributeName === "style") {
        const el = m.target;
        const styleAttr = el.getAttribute("style") || "";
        if (/opacity:\s*0(?!\d)/.test(styleAttr)) {
          if (
            !el.id ||
            (el.id !== "points-overlay" && el.id !== "points-modal")
          ) {
            const firstTime = !captured.has(el);
            console.warn(
              "[app.js] Interceptado opacity:0 en",
              el.tagName,
              "(id=",
              el.id || "-",
              ") -> forzando 1"
            );
            if (firstTime) {
              captured.add(el);
              try {
                console.groupCollapsed("[app.js] Stack origen opacity:0");
                console.trace();
                // Inspección heurística de scripts externos
                const scripts = Array.from(document.scripts)
                  .map((s) => s.src)
                  .filter(Boolean);
                console.log("Scripts cargados:", scripts);
                console.groupEnd();
              } catch (err) {
                console.error("[app.js] Error capturando stack", err);
              }
            }
            el.style.opacity = "1";
            // Eliminar transición si forma parte del problema
            if (/transition:\s*opacity/.test(styleAttr)) {
              el.style.transition = "none";
            }
            // Saneo extra: si es HTML o MAIN, quitamos completamente el atributo style para evitar re-aplicaciones encadenadas
            const tag = el.tagName.toLowerCase();
            if (
              (tag === "html" || tag === "main") &&
              el.hasAttribute("style")
            ) {
              el.removeAttribute("style");
              el.setAttribute("data-fade-blocked", "true");
              console.info(
                "[app.js] style removido de",
                tag,
                "para bloquear futuros fades"
              );
            }
          }
        }
      }
    });
  });
  opacityObserver.observe(document.documentElement, {
    attributes: true,
    subtree: true,
    attributeFilter: ["style"],
  });
}

// Funciones globales para componentes
window.toggleUserMenu = function () {
  const menu = document.getElementById("user-menu");
  menu.classList.toggle("hidden");
};

window.toggleMobileSidebar = function () {
  const sidebar = document.getElementById("mobile-sidebar");
  sidebar.classList.toggle("hidden");
};

// Quick validation for feedback (non-model form)
window.validateFeedback = function (form) {
  const msg = form.querySelector('[name="mensaje"]');
  if (msg && msg.value.trim().length < 10) {
    showNotification("Message must be at least 10 characters", "warning");
    return false;
  }
  return true;
};

// Close dropdowns when clicking outside
document.addEventListener("click", function (event) {
  // Close user menu
  const userButton = document.getElementById("user-menu-button");
  const userMenu = document.getElementById("user-menu");

  if (
    userButton &&
    userMenu &&
    !userButton.contains(event.target) &&
    !userMenu.contains(event.target)
  ) {
    userMenu.classList.add("hidden");
  }
});
