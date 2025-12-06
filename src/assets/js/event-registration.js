/**
 * Event Registration Handler
 * Handles event registration form submission with validation
 */

(function() {
  'use strict';

  // Form validation patterns
  const VALIDATION = {
    name: {
      pattern: /^[a-zA-Z\s]{3,50}$/,
      message: 'Name must be at least 3 characters and contain only letters and spaces'
    },
    email: {
      pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      message: 'Please enter a valid email address'
    },
    phone: {
      pattern: /^(\+255|0)[67]\d{8}$/,
      message: 'Please enter a valid Tanzanian phone number (e.g., +255712345678 or 0712345678)'
    }
  };

  /**
   * Validate form field
   */
  function validateField(field, value) {
    const validation = VALIDATION[field];
    if (!validation) return { valid: true };

    const valid = validation.pattern.test(value.trim());
    return {
      valid,
      message: valid ? '' : validation.message
    };
  }

  /**
   * Show error message for a field
   */
  function showFieldError(fieldElement, message) {
    // Remove existing error
    const existingError = fieldElement.parentElement.querySelector('.field-error');
    if (existingError) {
      existingError.remove();
    }

    // Add error class
    fieldElement.classList.add('is-invalid');

    // Create and show error message
    if (message) {
      const errorDiv = document.createElement('div');
      errorDiv.className = 'field-error text-danger small mt-1';
      errorDiv.textContent = message;
      fieldElement.parentElement.appendChild(errorDiv);
    }
  }

  /**
   * Clear field error
   */
  function clearFieldError(fieldElement) {
    fieldElement.classList.remove('is-invalid');
    const errorDiv = fieldElement.parentElement.querySelector('.field-error');
    if (errorDiv) {
      errorDiv.remove();
    }
  }

  /**
   * Show notification message
   */
  function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
      notification.remove();
    }, 5000);
  }

  /**
   * Handle form submission
   */
  async function handleRegistration(event) {
    event.preventDefault();

    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.textContent;

    // Get form values
    const nameField = form.querySelector('#name');
    const emailField = form.querySelector('#email');
    const phoneField = form.querySelector('#phone');

    const name = nameField.value.trim();
    const email = emailField.value.trim();
    const phone = phoneField.value.trim();

    // Get event ID from URL or form data
    const urlParams = new URLSearchParams(window.location.search);
    const eventId = urlParams.get('id');

    if (!eventId) {
      showNotification('Event ID not found', 'danger');
      return;
    }

    // Validate all fields
    let hasErrors = false;

    const nameValidation = validateField('name', name);
    if (!nameValidation.valid) {
      showFieldError(nameField, nameValidation.message);
      hasErrors = true;
    } else {
      clearFieldError(nameField);
    }

    const emailValidation = validateField('email', email);
    if (!emailValidation.valid) {
      showFieldError(emailField, emailValidation.message);
      hasErrors = true;
    } else {
      clearFieldError(emailField);
    }

    const phoneValidation = validateField('phone', phone);
    if (!phoneValidation.valid) {
      showFieldError(phoneField, phoneValidation.message);
      hasErrors = true;
    } else {
      clearFieldError(phoneField);
    }

    if (hasErrors) {
      return;
    }

    // Disable submit button and show loading state
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Registering...';

    try {
      // Send registration request
      const response = await fetch('/api/events/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          event_id: parseInt(eventId),
          user_name: name,
          user_email: email,
          user_mobile_number: phone
        })
      });

      const data = await response.json();

      if (response.ok) {
        // Success
        showNotification(data.message || 'Successfully registered for the event!', 'success');
        form.reset();
      } else {
        // Error from server
        if (response.status === 400 && data.detail.includes('already registered')) {
          showNotification('You are already registered for this event', 'warning');
        } else {
          showNotification(data.detail || 'Registration failed. Please try again.', 'danger');
        }
      }
    } catch (error) {
      console.error('Registration error:', error);
      showNotification('An error occurred. Please check your connection and try again.', 'danger');
    } finally {
      // Re-enable submit button
      submitButton.disabled = false;
      submitButton.textContent = originalButtonText;
    }
  }

  /**
   * Add real-time validation
   */
  function setupRealtimeValidation(form) {
    const nameField = form.querySelector('#name');
    const emailField = form.querySelector('#email');
    const phoneField = form.querySelector('#phone');

    if (nameField) {
      nameField.addEventListener('blur', function() {
        const validation = validateField('name', this.value);
        if (!validation.valid && this.value.trim()) {
          showFieldError(this, validation.message);
        } else {
          clearFieldError(this);
        }
      });

      nameField.addEventListener('input', function() {
        if (this.classList.contains('is-invalid')) {
          const validation = validateField('name', this.value);
          if (validation.valid) {
            clearFieldError(this);
          }
        }
      });
    }

    if (emailField) {
      emailField.addEventListener('blur', function() {
        const validation = validateField('email', this.value);
        if (!validation.valid && this.value.trim()) {
          showFieldError(this, validation.message);
        } else {
          clearFieldError(this);
        }
      });

      emailField.addEventListener('input', function() {
        if (this.classList.contains('is-invalid')) {
          const validation = validateField('email', this.value);
          if (validation.valid) {
            clearFieldError(this);
          }
        }
      });
    }

    if (phoneField) {
      phoneField.addEventListener('blur', function() {
        const validation = validateField('phone', this.value);
        if (!validation.valid && this.value.trim()) {
          showFieldError(this, validation.message);
        } else {
          clearFieldError(this);
        }
      });

      phoneField.addEventListener('input', function() {
        if (this.classList.contains('is-invalid')) {
          const validation = validateField('phone', this.value);
          if (validation.valid) {
            clearFieldError(this);
          }
        }
      });
    }
  }

  /**
   * Initialize event registration
   */
  function init() {
    // Find registration form on the page
    const registrationForm = document.querySelector('.registration-form form');
    
    if (registrationForm) {
      // Add submit event listener
      registrationForm.addEventListener('submit', handleRegistration);
      
      // Setup real-time validation
      setupRealtimeValidation(registrationForm);
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
