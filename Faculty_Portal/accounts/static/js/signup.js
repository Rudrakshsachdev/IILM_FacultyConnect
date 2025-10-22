// Password visibility toggle
    document.getElementById('togglePassword').addEventListener('click', function() {
      const passwordInput = document.getElementById('password');
      const icon = this.querySelector('i');
      
      if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
      } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
      }
    });
    
    document.getElementById('toggleConfirmPassword').addEventListener('click', function() {
      const confirmPasswordInput = document.getElementById('confirmPassword');
      const icon = this.querySelector('i');
      
      if (confirmPasswordInput.type === 'password') {
        confirmPasswordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
      } else {
        confirmPasswordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
      }
    });
    
    // Form submission loading state
    document.getElementById('signupForm').addEventListener('submit', function() {
      const submitBtn = document.getElementById('submitBtn');
      submitBtn.classList.add('loading');
      submitBtn.disabled = true;
      submitBtn.querySelector('span').textContent = 'Creating Account...';
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