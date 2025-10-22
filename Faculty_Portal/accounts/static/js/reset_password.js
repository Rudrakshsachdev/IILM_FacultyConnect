// Form submission loading state
    document.getElementById('otpForm').addEventListener('submit', function() {
      const submitBtn = document.getElementById('submitBtn');
      submitBtn.classList.add('loading');
      submitBtn.disabled = true;
      submitBtn.querySelector('span').textContent = 'Sending OTP...';
    });
    
    // Input focus effects
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
      input.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
      });
      
      input.addEventListener('blur', function() {
        if (this.value === '') {
          this.parentElement.classList.remove('focused');
        }
      });
    });
    
    // Add subtle animation to the form when page loads
    document.addEventListener('DOMContentLoaded', function() {
      const form = document.getElementById('otpForm');
      form.style.animation = 'fadeIn 0.8s ease-out';
    });