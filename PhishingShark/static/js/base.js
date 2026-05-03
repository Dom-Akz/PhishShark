function initDarkMode() {
  const themeToggle = document.getElementById("themeToggle");
  const sunIcon = document.querySelector(".sun-icon");
  const moonIcon = document.querySelector(".moon-icon");

  // Check for saved theme preference
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
    if (sunIcon && moonIcon) {
      sunIcon.style.display = "none";
      moonIcon.style.display = "block";
    }
  }

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      document.body.classList.toggle("dark-mode");

      if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
        if (sunIcon && moonIcon) {
          sunIcon.style.display = "none";
          moonIcon.style.display = "block";
        }
      } else {
        localStorage.setItem("theme", "light");
        if (sunIcon && moonIcon) {
          sunIcon.style.display = "block";
          moonIcon.style.display = "none";
        }
      }
    });
  }
}

// Mobile sidebar toggle
function initSidebar() {
  const menuToggle = document.getElementById("menuToggle");
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("sidebarOverlay");

  if (menuToggle) {
    menuToggle.addEventListener("click", function () {
      if (sidebar) sidebar.classList.toggle("active");
      if (overlay) overlay.classList.toggle("active");
    });
  }

  if (overlay) {
    overlay.addEventListener("click", function () {
      if (sidebar) sidebar.classList.remove("active");
      if (overlay) overlay.classList.remove("active");
    });
  }
}

// Notifications
function initNotifications() {
  const notifications = document.querySelectorAll(".notification");

  notifications.forEach((notification, index) => {
    setTimeout(() => {
      notification.classList.add("notification-show");
    }, index * 100);

    const timeout = parseInt(notification.dataset.autoDismiss) || 5000;
    const progressBar = notification.querySelector(".notification-progress");

    if (progressBar) {
      progressBar.style.animationDuration = timeout + "ms";
    }

    setTimeout(() => {
      dismissNotification(notification);
    }, timeout);
  });
}

function dismissNotification(notification) {
  if (!notification || notification.classList.contains("notification-hiding"))
    return;

  notification.classList.add("notification-hiding");
  notification.classList.remove("notification-show");

  setTimeout(() => {
    notification.remove();

    const container = document.getElementById("notificationsContainer");
    if (container && container.children.length === 0) {
      container.remove();
    }
  }, 300);
}

function showNotification(message, type = "info", duration = 5000) {
  let container = document.getElementById("notificationsContainer");

  if (!container) {
    container = document.createElement("div");
    container.id = "notificationsContainer";
    container.className = "notifications-container";
    const dashboardContent = document.querySelector(".dashboard-content");
    if (dashboardContent) {
      dashboardContent.parentNode.insertBefore(container, dashboardContent);
    }
  }

  const icons = {
    success:
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    error:
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
    warning:
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    info: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
  };

  const notification = document.createElement("div");
  notification.className = "notification notification-" + type;
  notification.dataset.autoDismiss = duration;
  notification.innerHTML = `
        <div class="notification-icon">${icons[type] || icons.info}</div>
        <div class="notification-content">
            <p class="notification-message">${message}</p>
        </div>
        <button class="notification-close" onclick="dismissNotification(this.parentElement)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
        </button>
        <div class="notification-progress" style="animation-duration: ${duration}ms;"></div>
    `;

  container.appendChild(notification);

  requestAnimationFrame(() => {
    notification.classList.add("notification-show");
  });

  setTimeout(() => {
    dismissNotification(notification);
  }, duration);

  return notification;
}

// Initialize everything when DOM is ready
document.addEventListener("DOMContentLoaded", function () {
  initDarkMode();
  initSidebar();
  initNotifications();
});
