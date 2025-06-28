// Modern Dashboard JavaScript

// Initialize dashboard
document.addEventListener("DOMContentLoaded", function () {
  initializeAnimations();
  initializeCharts();
  initializeCounters();
  initializeTooltips();
  initializeModals();
  initializeFileUploads();
});

// Animated counters
function initializeCounters() {
  const counters = document.querySelectorAll('[id$="-counter"]');
  counters.forEach((counter) => {
    const target = parseInt(counter.textContent.replace(/,/g, ""));
    const duration = 2000; // 2 seconds
    const increment = target / (duration / 16); // 60fps
    let current = 0;

    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      counter.textContent = Math.floor(current).toLocaleString();
    }, 16);
  });
}

// Initialize animations
function initializeAnimations() {
  // Intersection Observer for animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("animate-in");
      }
    });
  }, observerOptions);

  // Observe all animatable elements
  document
    .querySelectorAll(
      ".animate-fade-in-up, .animate-scale-in, .animate-slide-in-left, .animate-slide-in-right"
    )
    .forEach((el) => observer.observe(el));
}

// Initialize charts
function initializeCharts() {
  // Views Chart
  const viewsCanvas = document.getElementById("viewsChart");
  if (viewsCanvas && typeof Chart !== "undefined") {
    const ctx = viewsCanvas.getContext("2d");

    new Chart(ctx, {
      type: "line",
      data: {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        datasets: [
          {
            label: "Views",
            data: [1200, 1900, 3000, 5000, 2000, 3000, 4500],
            borderColor: "rgb(168, 85, 247)",
            backgroundColor: "rgba(168, 85, 247, 0.1)",
            borderWidth: 3,
            tension: 0.4,
            fill: true,
            pointBackgroundColor: "rgb(168, 85, 247)",
            pointBorderColor: "#fff",
            pointBorderWidth: 2,
            pointRadius: 6,
            pointHoverRadius: 8,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: "rgba(0, 0, 0, 0.8)",
            titleColor: "#fff",
            bodyColor: "#fff",
            borderColor: "rgb(168, 85, 247)",
            borderWidth: 1,
            cornerRadius: 8,
          },
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: "#6B7280" },
          },
          y: {
            beginAtZero: true,
            grid: { color: "#F3F4F6" },
            ticks: { color: "#6B7280" },
          },
        },
        interaction: {
          intersect: false,
          mode: "index",
        },
      },
    });
  }

  // Revenue Chart (if exists)
  const revenueCanvas = document.getElementById("revenueChart");
  if (revenueCanvas && typeof Chart !== "undefined") {
    const ctx = revenueCanvas.getContext("2d");

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [
          {
            label: "Revenue",
            data: [12000, 19000, 3000, 5000, 2000, 3000],
            backgroundColor: [
              "rgba(59, 130, 246, 0.8)",
              "rgba(16, 185, 129, 0.8)",
              "rgba(168, 85, 247, 0.8)",
              "rgba(245, 158, 11, 0.8)",
              "rgba(239, 68, 68, 0.8)",
              "rgba(99, 102, 241, 0.8)",
            ],
            borderRadius: 8,
            borderSkipped: false,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: "#6B7280" },
          },
          y: {
            beginAtZero: true,
            grid: { color: "#F3F4F6" },
            ticks: { color: "#6B7280" },
          },
        },
      },
    });
  }
}

// Initialize tooltips
function initializeTooltips() {
  const tooltipElements = document.querySelectorAll("[data-tooltip]");

  tooltipElements.forEach((element) => {
    element.addEventListener("mouseenter", showTooltip);
    element.addEventListener("mouseleave", hideTooltip);
  });
}

function showTooltip(event) {
  const text = event.target.getAttribute("data-tooltip");
  const tooltip = document.createElement("div");
  tooltip.className =
    "absolute bg-gray-800 text-white px-2 py-1 rounded text-sm z-50 tooltip";
  tooltip.textContent = text;
  document.body.appendChild(tooltip);

  const rect = event.target.getBoundingClientRect();
  tooltip.style.left =
    rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + "px";
  tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + "px";
}

function hideTooltip() {
  const tooltip = document.querySelector(".tooltip");
  if (tooltip) {
    tooltip.remove();
  }
}

// Initialize modals
function initializeModals() {
  // Close modal when clicking outside
  document.addEventListener("click", function (event) {
    const modals = document.querySelectorAll(".modal");
    modals.forEach((modal) => {
      if (event.target === modal) {
        modal.classList.add("hidden");
      }
    });
  });

  // Close modal with Escape key
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      const openModals = document.querySelectorAll(".modal:not(.hidden)");
      openModals.forEach((modal) => {
        modal.classList.add("hidden");
      });
    }
  });
}

// Initialize file upload functionality
function initializeFileUploads() {
  // Video upload
  const videoUploadArea = document.getElementById("video-upload-area");
  const videoInput = document.getElementById("video-input");

  if (videoUploadArea && videoInput) {
    videoUploadArea.addEventListener("click", () => videoInput.click());
    videoUploadArea.addEventListener("dragover", handleDragOver);
    videoUploadArea.addEventListener("drop", (e) => handleVideoDrop(e));
    videoInput.addEventListener("change", (e) => handleVideoSelect(e));
  }

  // Poster upload
  const posterUploadArea = document.getElementById("poster-upload-area");
  const posterInput = document.getElementById("poster-input");

  if (posterUploadArea && posterInput) {
    posterUploadArea.addEventListener("click", () => posterInput.click());
    posterUploadArea.addEventListener("dragover", handleDragOver);
    posterUploadArea.addEventListener("drop", (e) => handlePosterDrop(e));
    posterInput.addEventListener("change", (e) => handlePosterSelect(e));
  }
}

// Handle drag over
function handleDragOver(e) {
  e.preventDefault();
  e.currentTarget.classList.add("border-purple-400", "bg-purple-50");
}

// Handle video file drop
function handleVideoDrop(e) {
  e.preventDefault();
  e.currentTarget.classList.remove("border-purple-400", "bg-purple-50");

  const files = e.dataTransfer.files;
  if (files.length > 0) {
    const file = files[0];
    if (file.type.startsWith("video/")) {
      uploadVideoFile(file);
    } else {
      showNotification("Please select a valid video file", "error");
    }
  }
}

// Handle video file selection
function handleVideoSelect(e) {
  const file = e.target.files[0];
  if (file) {
    uploadVideoFile(file);
  }
}

// Upload video file via AJAX
function uploadVideoFile(file) {
  // Validate file size (500MB limit)
  const maxSize = 500 * 1024 * 1024; // 500MB
  if (file.size > maxSize) {
    showNotification("Video file too large. Maximum size is 500MB.", "error");
    return;
  }

  // Set uploading state
  window.uploadState?.setUploading("video", true);

  // Show upload progress
  const uploadProgress = document.getElementById("video-upload-progress");
  const progressBar = document.getElementById("video-progress-bar");
  const uploadStatus = document.getElementById("video-upload-status");
  const uploadPercent = document.getElementById("video-upload-percent");
  const uploadArea = document.getElementById("video-upload-area");

  uploadProgress.classList.remove("hidden");
  uploadArea.classList.add("hidden");

  // Create FormData
  const formData = new FormData();
  formData.append("video", file);

  // Get CSRF token
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  // Create XMLHttpRequest for progress tracking
  const xhr = new XMLHttpRequest();

  // Track upload progress
  xhr.upload.addEventListener("progress", function (e) {
    if (e.lengthComputable) {
      const percentComplete = (e.loaded / e.total) * 100;
      progressBar.style.width = percentComplete + "%";
      uploadPercent.textContent = Math.round(percentComplete) + "%";

      if (percentComplete < 100) {
        uploadStatus.textContent = "Uploading...";
      } else {
        uploadStatus.textContent = "Processing...";
      }
    }
  });

  // Handle completion
  xhr.addEventListener("load", function () {
    window.uploadState?.setUploading("video", false);

    if (xhr.status === 200) {
      try {
        const response = JSON.parse(xhr.responseText);
        if (response.success) {
          // Hide progress, show preview
          uploadProgress.classList.add("hidden");
          showVideoPreview(file.name, file.size, response.file_path);

          // Set hidden input value
          document.getElementById("video-path").value = response.file_path;

          showNotification("Video uploaded successfully!", "success");
        } else {
          throw new Error(response.error || "Upload failed");
        }
      } catch (e) {
        showUploadError("Failed to process server response");
      }
    } else {
      showUploadError("Upload failed. Please try again.");
    }
  });

  // Handle errors
  xhr.addEventListener("error", function () {
    window.uploadState?.setUploading("video", false);
    showUploadError("Network error. Please check your connection.");
  });

  // Open connection and send
  xhr.open("POST", "/films/ajax/upload-video/", true);
  xhr.setRequestHeader("X-CSRFToken", csrfToken);
  xhr.send(formData);
}

// Show video preview
function showVideoPreview(fileName, fileSize, filePath) {
  const preview = document.getElementById("video-preview");
  const fileNameElement = document.getElementById("video-file-name");
  const fileSizeElement = document.getElementById("video-file-size");

  fileNameElement.textContent = fileName;
  fileSizeElement.textContent = formatFileSize(fileSize);
  preview.classList.remove("hidden");
}

// Remove video preview
function removeVideoPreview() {
  const preview = document.getElementById("video-preview");
  const uploadArea = document.getElementById("video-upload-area");
  const uploadProgress = document.getElementById("video-upload-progress");
  const videoPath = document.getElementById("video-path");
  const videoInput = document.getElementById("video-input");

  preview.classList.add("hidden");
  uploadArea.classList.remove("hidden");
  uploadProgress.classList.add("hidden");
  videoPath.value = "";
  videoInput.value = "";
}

// Handle poster file drop
function handlePosterDrop(e) {
  e.preventDefault();
  e.currentTarget.classList.remove("border-purple-400", "bg-purple-50");

  const files = e.dataTransfer.files;
  if (files.length > 0) {
    const file = files[0];
    if (file.type.startsWith("image/")) {
      uploadPosterFile(file);
    } else {
      showNotification("Please select a valid image file", "error");
    }
  }
}

// Handle poster file selection
function handlePosterSelect(e) {
  const file = e.target.files[0];
  if (file) {
    uploadPosterFile(file);
  }
}

// Upload poster file via AJAX
function uploadPosterFile(file) {
  // Validate file size (10MB limit)
  const maxSize = 10 * 1024 * 1024; // 10MB
  if (file.size > maxSize) {
    showNotification("Image file too large. Maximum size is 10MB.", "error");
    return;
  }

  // Set uploading state
  window.uploadState?.setUploading("poster", true);

  // Create FormData
  const formData = new FormData();
  formData.append("image", file);

  // Get CSRF token
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  // Show loading state
  const uploadArea = document.getElementById("poster-upload-area");
  uploadArea.innerHTML = `
    <div class="space-y-1 text-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500 mx-auto"></div>
      <p class="text-sm text-gray-600">Uploading...</p>
    </div>
  `;

  // Upload via fetch
  fetch("/films/ajax/upload-image/", {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      window.uploadState?.setUploading("poster", false);

      if (data.success) {
        showPosterPreview(file, data.file_path);
        document.getElementById("poster-path").value = data.file_path;
        showNotification("Image uploaded successfully!", "success");
      } else {
        throw new Error(data.error || "Upload failed");
      }
    })
    .catch((error) => {
      window.uploadState?.setUploading("poster", false);
      // Reset upload area
      resetPosterUploadArea();
      showNotification("Upload failed: " + error.message, "error");
    });
}

// Show poster preview
function showPosterPreview(file, filePath) {
  const reader = new FileReader();
  reader.onload = function (e) {
    const preview = document.getElementById("poster-preview");
    const previewImg = document.getElementById("poster-preview-img");
    const uploadArea = document.getElementById("poster-upload-area");

    previewImg.src = e.target.result;
    preview.classList.remove("hidden");
    uploadArea.classList.add("hidden");
  };
  reader.readAsDataURL(file);
}

// Remove poster preview
function removePosterPreview() {
  const preview = document.getElementById("poster-preview");
  const posterPath = document.getElementById("poster-path");
  const posterInput = document.getElementById("poster-input");

  preview.classList.add("hidden");
  posterPath.value = "";
  posterInput.value = "";
  resetPosterUploadArea();
}

// Reset poster upload area
function resetPosterUploadArea() {
  const uploadArea = document.getElementById("poster-upload-area");
  uploadArea.classList.remove("hidden");
  uploadArea.innerHTML = `
    <div class="space-y-1 text-center">
      <i class="fas fa-image text-gray-400 text-3xl mb-3"></i>
      <div class="flex text-sm text-gray-600">
        <span class="text-purple-600 hover:text-purple-500 font-medium">Upload poster image</span>
        <p class="pl-1">or drag and drop</p>
      </div>
      <p class="text-xs text-gray-500">PNG, JPG up to 10MB</p>
    </div>
  `;
}

// Show upload error
function showUploadError(message) {
  window.uploadState?.setUploading("video", false);

  const uploadProgress = document.getElementById("video-upload-progress");
  const uploadArea = document.getElementById("video-upload-area");

  uploadProgress.classList.add("hidden");
  uploadArea.classList.remove("hidden");

  showNotification(message, "error");
}

// Format file size
function formatFileSize(bytes) {
  if (bytes === 0) return "0 Bytes";

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

// Utility functions
function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function showNotification(message, type = "success") {
  const notification = document.createElement("div");
  notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg transition-all duration-300 ${
    type === "success"
      ? "bg-green-500 text-white"
      : type === "error"
      ? "bg-red-500 text-white"
      : "bg-blue-500 text-white"
  }`;
  notification.textContent = message;

  document.body.appendChild(notification);

  // Animate in
  setTimeout(() => {
    notification.classList.add("animate-slide-in-right");
  }, 10);

  // Remove after 3 seconds
  setTimeout(() => {
    notification.style.transform = "translateX(100%)";
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 300);
  }, 3000);
}

// Dark mode toggle
function toggleDarkMode() {
  document.documentElement.classList.toggle("dark");
  localStorage.setItem(
    "darkMode",
    document.documentElement.classList.contains("dark")
  );
}

// Search functionality
function handleSearch(query) {
  if (query.length < 2) return;

  // Simulate search (replace with actual search logic)
  console.log("Searching for:", query);

  // You can implement real search here
  // For example, filter cards based on query
  const cards = document.querySelectorAll("[data-searchable]");
  cards.forEach((card) => {
    const text = card.textContent.toLowerCase();
    if (text.includes(query.toLowerCase())) {
      card.style.display = "block";
    } else {
      card.style.display = "none";
    }
  });
}

// Sidebar toggle for mobile
function toggleSidebar() {
  const sidebar = document.querySelector("#sidebar");
  if (sidebar) {
    sidebar.classList.toggle("hidden");
  }
}

// Real-time updates (placeholder)
function startRealTimeUpdates() {
  setInterval(() => {
    // Update stats periodically
    updateStats();
  }, 30000); // Update every 30 seconds
}

function updateStats() {
  // Simulate real-time stat updates
  const statsElements = document.querySelectorAll("[data-stat]");
  statsElements.forEach((element) => {
    const currentValue = parseInt(element.textContent.replace(/,/g, ""));
    const newValue = currentValue + Math.floor(Math.random() * 10);
    element.textContent = formatNumber(newValue);
  });
}

// Export functions for global use
window.dashboardUtils = {
  showNotification,
  toggleDarkMode,
  handleSearch,
  toggleSidebar,
  formatNumber,
};
