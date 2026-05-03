document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("addEmployeeForm");

  // Client-side validation
  form.addEventListener("submit", function (e) {
    let isValid = true;
    const requiredFields = form.querySelectorAll("[required]");

    requiredFields.forEach((field) => {
      const formGroup = field.closest(".form-group");
      const existingError = formGroup.querySelector(".error-message");

      // Remove existing error styling
      formGroup.classList.remove("has-error");
      if (existingError && !existingError.dataset.server) {
        existingError.remove();
      }

      if (!field.value.trim()) {
        isValid = false;
        formGroup.classList.add("has-error");

        if (!existingError) {
          const errorSpan = document.createElement("span");
          errorSpan.className = "error-message";
          errorSpan.innerHTML = `
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <line x1="12" y1="8" x2="12" y2="12"/>
                            <line x1="12" y1="16" x2="12.01" y2="16"/>
                        </svg>
                        This field is required
                    `;
          formGroup.appendChild(errorSpan);
        }
      }

      // Email validation
      if (field.type === "email" && field.value.trim()) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(field.value)) {
          isValid = false;
          formGroup.classList.add("has-error");

          if (!existingError) {
            const errorSpan = document.createElement("span");
            errorSpan.className = "error-message";
            errorSpan.innerHTML = `
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"/>
                                <line x1="12" y1="8" x2="12" y2="12"/>
                                <line x1="12" y1="16" x2="12.01" y2="16"/>
                            </svg>
                            Please enter a valid email address
                        `;
            formGroup.appendChild(errorSpan);
          }
        }
      }
    });

    if (!isValid) {
      e.preventDefault();
      // Scroll to first error
      const firstError = form.querySelector(".has-error");
      if (firstError) {
        firstError.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }
  });

  // Clear error styling on input
  form.querySelectorAll("input, select").forEach((field) => {
    field.addEventListener("input", function () {
      const formGroup = this.closest(".form-group");
      formGroup.classList.remove("has-error");
      const errorMessage = formGroup.querySelector(
        ".error-message:not([data-server])",
      );
      if (errorMessage) {
        errorMessage.remove();
      }
    });
  });
});
