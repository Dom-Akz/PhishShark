/**
 * Security Admin Dashboard - Chart.js Implementation
 * PhishingShark & Sensibilisation Dashboard
 */

// Chart.js default configuration
Chart.defaults.font.family =
  "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = "#64748b";
Chart.defaults.responsive = true;
Chart.defaults.maintainAspectRatio = false;

// Color palette
const colors = {
  primary: "#2563eb",
  primaryLight: "#3b82f6",
  secondary: "#64748b",
  success: "#10b981",
  danger: "#ef4444",
  warning: "#f59e0b",
  info: "#06b6d4",
  purple: "#8b5cf6",
  teal: "#14b8a6",
  pink: "#ec4899",
  orange: "#f97316",
  lime: "#84cc16",
  // Transparent versions
  primaryAlpha: "rgba(37, 99, 235, 0.1)",
  successAlpha: "rgba(16, 185, 129, 0.1)",
  dangerAlpha: "rgba(239, 68, 68, 0.1)",
  warningAlpha: "rgba(245, 158, 11, 0.1)",
  purpleAlpha: "rgba(139, 92, 246, 0.1)",
};

// Store chart instances for updates
const chartInstances = {};

/**
 * Initialize all charts when DOM is ready
 */
document.addEventListener("DOMContentLoaded", function () {
  initializeCharts();
  initializeEventListeners();
  initializeSidebar();
});

/**
 * Initialize all chart instances
 */
function initializeCharts() {
  createEmailStatusChart();
  createEmailTypeChart();
  createTimelineChart();
  createQuizScoreChart();
  createTrainingEngagementChart();
  createDepartmentRiskChart();
  createAttemptsVsScoreChart();
}

/**
 * Email Status Distribution - Doughnut Chart
 */
function createEmailStatusChart() {
  const ctx = document.getElementById("emailStatusChart");
  if (!ctx) return;

  const data = dashboardData.emailStatus;

  chartInstances.emailStatus = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: data.labels,
      datasets: [
        {
          data: data.data,
          backgroundColor: [
            colors.secondary,
            colors.primary,
            colors.success,
            colors.danger,
            colors.warning,
          ],
          borderWidth: 0,
          hoverOffset: 8,
        },
      ],
    },
    options: {
      cutout: "65%",
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: "#1e293b",
          titleColor: "#f8fafc",
          bodyColor: "#f8fafc",
          padding: 12,
          cornerRadius: 8,
          displayColors: true,
          callbacks: {
            label: function (context) {
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const percentage = ((context.raw / total) * 100).toFixed(1);
              return `${context.label}: ${context.raw} (${percentage}%)`;
            },
          },
        },
      },
    },
  });

  // Create custom legend
  createCustomLegend("emailStatusLegend", data.labels, [
    colors.secondary,
    colors.primary,
    colors.success,
    colors.danger,
    colors.warning,
  ]);
}

/**
 * Email Type Performance - Bar Chart
 */
function createEmailTypeChart() {
  const ctx = document.getElementById("emailTypeChart");
  if (!ctx) return;

  const data = dashboardData.emailTypes;

  chartInstances.emailType = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Sent",
          data: data.sent,
          backgroundColor: colors.primary,
          borderRadius: 4,
          barPercentage: 0.7,
          categoryPercentage: 0.8,
        },
        {
          label: "Clicked",
          data: data.clicked,
          backgroundColor: colors.danger,
          borderRadius: 4,
          barPercentage: 0.7,
          categoryPercentage: 0.8,
        },
      ],
    },
    options: {
      indexAxis: "y",
      scales: {
        x: {
          beginAtZero: true,
          grid: {
            color: "rgba(0, 0, 0, 0.05)",
          },
        },
        y: {
          grid: {
            display: false,
          },
          ticks: {
            callback: function (value) {
              const label = this.getLabelForValue(value);
              return label.length > 15 ? label.substr(0, 15) + "..." : label;
            },
          },
        },
      },
      plugins: {
        legend: {
          position: "top",
          align: "end",
          labels: {
            boxWidth: 12,
            boxHeight: 12,
            borderRadius: 3,
            useBorderRadius: true,
            padding: 15,
          },
        },
        tooltip: {
          backgroundColor: "#1e293b",
          titleColor: "#f8fafc",
          bodyColor: "#f8fafc",
          padding: 12,
          cornerRadius: 8,
        },
      },
    },
  });
}

/**
 * Campaign Timeline - Line Chart
 */
function createTimelineChart() {
  const ctx = document.getElementById("timelineChart");
  if (!ctx) return;

  const data = dashboardData.timeline;

  chartInstances.timeline = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Emails Sent",
          data: data.sent,
          borderColor: colors.primary,
          backgroundColor: colors.primaryAlpha,
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: "#fff",
          pointBorderColor: colors.primary,
          pointBorderWidth: 2,
        },
        {
          label: "Received",
          data: data.received,
          borderColor: colors.success,
          backgroundColor: "transparent",
          borderWidth: 2,
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: "#fff",
          pointBorderColor: colors.success,
          pointBorderWidth: 2,
        },
        {
          label: "Clicked",
          data: data.clicked,
          borderColor: colors.danger,
          backgroundColor: "transparent",
          borderWidth: 2,
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: "#fff",
          pointBorderColor: colors.danger,
          pointBorderWidth: 2,
        },
      ],
    },
    options: {
      scales: {
        x: {
          grid: {
            display: false,
          },
        },
        y: {
          beginAtZero: true,
          grid: {
            color: "rgba(0, 0, 0, 0.05)",
          },
        },
      },
      plugins: {
        legend: {
          position: "top",
          align: "end",
          labels: {
            boxWidth: 12,
            boxHeight: 12,
            borderRadius: 3,
            useBorderRadius: true,
            padding: 15,
          },
        },
        tooltip: {
          mode: "index",
          intersect: false,
          backgroundColor: "#1e293b",
          titleColor: "#f8fafc",
          bodyColor: "#f8fafc",
          padding: 12,
          cornerRadius: 8,
        },
      },
      interaction: {
        mode: "index",
        intersect: false,
      },
    },
  });
}

/**
 * Quiz Score Distribution - Bar Chart
 */
function createQuizScoreChart() {
  const ctx = document.getElementById("quizScoreChart");
  if (!ctx) return;

  const data = dashboardData.quizScores;

  chartInstances.quizScore = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Number of Employees",
          data: data.data,
          backgroundColor: [
            colors.danger,
            colors.warning,
            colors.secondary,
            colors.info,
            colors.success,
          ],
          borderRadius: 6,
          barPercentage: 0.7,
        },
      ],
    },
    options: {
      scales: {
        x: {
          grid: {
            display: false,
          },
        },
        y: {
          beginAtZero: true,
          grid: {
            color: "rgba(0, 0, 0, 0.05)",
          },
          ticks: {
            stepSize: 10,
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: "#1e293b",
          titleColor: "#f8fafc",
          bodyColor: "#f8fafc",
          padding: 12,
          cornerRadius: 8,
          callbacks: {
            label: function (context) {
              return `${context.raw} employees`;
            },
          },
        },
      },
    },
  });
}

/**
 * Training Engagement by Department - Polar Area Chart
 */
function createTrainingEngagementChart() {
  const ctx = document.getElementById("trainingEngagementChart");
  if (!ctx) return;

  const data = dashboardData.trainingEngagement;

  chartInstances.trainingEngagement = new Chart(ctx, {
    type: "polarArea",
    data: {
      labels: data.labels,
      datasets: [
        {
          data: data.data,
          backgroundColor: [
            "rgba(37, 99, 235, 0.7)",
            "rgba(16, 185, 129, 0.7)",
            "rgba(245, 158, 11, 0.7)",
            "rgba(139, 92, 246, 0.7)",
            "rgba(20, 184, 166, 0.7)",
          ],
          borderWidth: 0,
        },
      ],
    },
    options: {
      scales: {
        r: {
          beginAtZero: true,
          max: 100,
          ticks: {
            stepSize: 25,
            backdropColor: "transparent",
          },
          grid: {
            color: "rgba(0, 0, 0, 0.05)",
          },
        },
      },
      plugins: {
        legend: {
          position: "right",
          labels: {
            boxWidth: 12,
            boxHeight: 12,
            borderRadius: 3,
            useBorderRadius: true,
            padding: 12,
          },
        },
        tooltip: {
          backgroundColor: "#1e293b",
          titleColor: "#f8fafc",
          bodyColor: "#f8fafc",
          padding: 12,
          cornerRadius: 8,
          callbacks: {
            label: function (context) {
              return `${context.label}: ${context.raw}% completion`;
            },
          },
        },
      },
    },
  });
}

/**
 * Department Risk Assessment - Radar Chart
 */
function createDepartmentRiskChart() {
  const ctx = document.getElementById("departmentRiskChart");
  if (!ctx) return;

  const data = dashboardData.departmentRisk;

  chartInstances.departmentRisk = new Chart(ctx, {
    type: "radar",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Click Rate (%)",
          data: data.clickRate,
          borderColor: colors.danger,
          backgroundColor: colors.dangerAlpha,
          borderWidth: 2,
          pointBackgroundColor: colors.danger,
          pointBorderColor: "#fff",
          pointBorderWidth: 2,
          pointRadius: 4,
        },
        {
          label: "Training Score (%)",
          data: data.trainingScore,
          borderColor: colors.success,
          backgroundColor: colors.successAlpha,
          borderWidth: 2,
          pointBackgroundColor: colors.success,
          pointBorderColor: "#fff",
          pointBorderWidth: 2,
          pointRadius: 4,
        },
      ],
    },
    options: {
      scales: {
        r: {
          beginAtZero: true,
          max: 100,
          ticks: {
            stepSize: 25,
            backdropColor: "transparent",
          },
          grid: {
            color: "rgba(0, 0, 0, 0.05)",
          },
          pointLabels: {
            font: {
              size: 11,
            },
          },
        },
      },
      plugins: {
        legend: {
          position: "top",
          labels: {
            boxWidth: 12,
            boxHeight: 12,
            borderRadius: 3,
            useBorderRadius: true,
            padding: 15,
          },
        },
        tooltip: {
          backgroundColor: "#1e293b",
          titleColor: "#f8fafc",
          bodyColor: "#f8fafc",
          padding: 12,
          cornerRadius: 8,
        },
      },
    },
  });
}

/**
 * Quiz Attempts vs Performance - Scatter Chart
 */
function createAttemptsVsScoreChart() {
  const ctx = document.getElementById("attemptsVsScoreChart");
  if (!ctx) return;

  const data = dashboardData.attemptsVsScore;

  chartInstances.attemptsVsScore = new Chart(ctx, {
    type: "scatter",
    data: {
      datasets: [
        {
          label: "Employees",
          data: data,
          backgroundColor: colors.purple,
          borderColor: "transparent",
          pointRadius: 8,
          pointHoverRadius: 10,
        },
      ],
    },
    options: {
      scales: {
        x: {
          title: {
            display: true,
            text: "Number of Attempts",
            font: { weight: "bold" },
          },
          beginAtZero: true,
          max: 5,
          grid: {
            color: "rgba(0, 0, 0, 0.05)",
          },
        },
        y: {
          title: {
            display: true,
            text: "Score (%)",
            font: { weight: "bold" },
          },
          beginAtZero: true,
          max: 100,
          grid: {
            color: "rgba(0, 0, 0, 0.05)",
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: "#1e293b",
          titleColor: "#f8fafc",
          bodyColor: "#f8fafc",
          padding: 12,
          cornerRadius: 8,
          callbacks: {
            label: function (context) {
              return `Attempts: ${context.raw.x}, Score: ${context.raw.y}%`;
            },
          },
        },
      },
    },
  });
}

/**
 * Create custom legend for doughnut chart
 */
function createCustomLegend(containerId, labels, colors) {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = labels
    .map(
      (label, index) => `
        <div class="legend-item">
            <span class="legend-color" style="background-color: ${colors[index]}"></span>
            <span>${label}</span>
        </div>
    `,
    )
    .join("");
}

/**
 * Initialize event listeners
 */
function initializeEventListeners() {
  // Date range filter
  const dateRange = document.getElementById("dateRange");
  if (dateRange) {
    dateRange.addEventListener("change", function () {
      updateDashboardData(this.value);
    });
  }

  // Department filter
  const deptFilter = document.getElementById("departmentFilter");
  if (deptFilter) {
    deptFilter.addEventListener("change", function () {
      filterByDepartment(this.value);
    });
  }

  // Refresh button
  const refreshBtn = document.getElementById("refreshData");
  if (refreshBtn) {
    refreshBtn.addEventListener("click", function () {
      refreshDashboard();
    });
  }

  // Timeline period tabs
  const tabBtns = document.querySelectorAll(".tab-btn");
  tabBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      tabBtns.forEach((b) => b.classList.remove("active"));
      this.classList.add("active");
      updateTimelinePeriod(this.dataset.period);
    });
  });
}

/**
 * Initialize sidebar toggle for mobile
 */
function initializeSidebar() {
  const menuToggle = document.getElementById("menuToggle");
  const sidebar = document.querySelector(".sidebar");

  if (menuToggle && sidebar) {
    // Create overlay
    const overlay = document.createElement("div");
    overlay.className = "sidebar-overlay";
    document.body.appendChild(overlay);

    menuToggle.addEventListener("click", function () {
      sidebar.classList.toggle("open");
      overlay.classList.toggle("show");
    });

    overlay.addEventListener("click", function () {
      sidebar.classList.remove("open");
      overlay.classList.remove("show");
    });
  }
}

/**
 * Update dashboard data based on date range
 * This would typically make an AJAX call to the backend
 */
function updateDashboardData(days) {
  console.log(`Updating dashboard for last ${days} days`);

  // Show loading state
  document.querySelectorAll(".chart-card").forEach((card) => {
    card.classList.add("loading");
  });

  // Simulated API call - replace with actual fetch
  // fetch(`/api/dashboard/data/?days=${days}`)
  //     .then(response => response.json())
  //     .then(data => {
  //         updateCharts(data);
  //     });

  // Remove loading state after simulated delay
  setTimeout(() => {
    document.querySelectorAll(".chart-card").forEach((card) => {
      card.classList.remove("loading");
    });
  }, 500);
}

/**
 * Filter dashboard by department
 */
function filterByDepartment(deptId) {
  console.log(`Filtering by department: ${deptId}`);

  // Simulated filter - replace with actual implementation
  // fetch(`/api/dashboard/data/?department=${deptId}`)
  //     .then(response => response.json())
  //     .then(data => {
  //         updateCharts(data);
  //     });
}

/**
 * Refresh all dashboard data
 */
function refreshDashboard() {
  const refreshBtn = document.getElementById("refreshData");
  if (refreshBtn) {
    refreshBtn.disabled = true;
    refreshBtn.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="animate-spin">
                <circle cx="12" cy="12" r="10" stroke-opacity="0.25"/>
                <path d="M12 2a10 10 0 0 1 10 10"/>
            </svg>
            Refreshing...
        `;
  }

  // Simulated refresh - replace with actual fetch
  setTimeout(() => {
    if (refreshBtn) {
      refreshBtn.disabled = false;
      refreshBtn.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="23 4 23 10 17 10"/>
                    <polyline points="1 20 1 14 7 14"/>
                    <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
                </svg>
                Refresh
            `;
    }

    // Recreate charts with new data
    Object.values(chartInstances).forEach((chart) => {
      if (chart) chart.update();
    });
  }, 1000);
}

/**
 * Update timeline chart period (daily/weekly/monthly)
 */
function updateTimelinePeriod(period) {
  console.log(`Switching timeline to: ${period}`);

  const timelineChart = chartInstances.timeline;
  if (!timelineChart) return;

  // Simulated data update - replace with actual fetch
  let newLabels, newData;

  switch (period) {
    case "weekly":
      newLabels = ["Week 1", "Week 2", "Week 3", "Week 4"];
      newData = {
        sent: [180, 220, 195, 240],
        received: [165, 200, 180, 220],
        clicked: [35, 45, 38, 50],
      };
      break;
    case "monthly":
      newLabels = ["Jan", "Feb", "Mar", "Apr"];
      newData = {
        sent: [720, 850, 680, 920],
        received: [650, 780, 620, 840],
        clicked: [140, 180, 130, 195],
      };
      break;
    default: // daily
      newLabels = dashboardData.timeline.labels;
      newData = {
        sent: dashboardData.timeline.sent,
        received: dashboardData.timeline.received,
        clicked: dashboardData.timeline.clicked,
      };
  }

  timelineChart.data.labels = newLabels;
  timelineChart.data.datasets[0].data = newData.sent;
  timelineChart.data.datasets[1].data = newData.received;
  timelineChart.data.datasets[2].data = newData.clicked;
  timelineChart.update();
}

/**
 * Animate numbers on KPI cards
 */
function animateNumbers() {
  const kpiValues = document.querySelectorAll(".kpi-value[data-value]");

  kpiValues.forEach((el) => {
    const target = parseFloat(el.dataset.value) || 0;
    const duration = 1000;
    const start = 0;
    const startTime = performance.now();

    function animate(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easeOut = 1 - Math.pow(1 - progress, 3);
      const current = start + (target - start) * easeOut;

      if (el.textContent.includes("%")) {
        el.textContent = Math.round(current) + "%";
      } else if (el.textContent.includes(":")) {
        // Time format - skip animation
        return;
      } else {
        el.textContent = Math.round(current).toLocaleString();
      }

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    }

    requestAnimationFrame(animate);
  });
}

// Run number animation after page load
window.addEventListener("load", animateNumbers);

/**
 * Export chart as image
 */
function exportChart(chartId, filename) {
  const chart = chartInstances[chartId];
  if (!chart) return;

  const link = document.createElement("a");
  link.download = filename || `${chartId}-chart.png`;
  link.href = chart.toBase64Image();
  link.click();
}

// Make export function available globally
window.exportChart = exportChart;
