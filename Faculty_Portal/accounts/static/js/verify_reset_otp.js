// Password visibility toggle
    document.getElementById('togglePassword').addEventListener('click', function() {
      const passwordInput = document.getElementById('newPassword');
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
      const passwordInput = document.getElementById('confirmPassword');
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
    
    // Password strength indicator
    const passwordInput = document.getElementById('newPassword');
    const strengthMeter = document.getElementById('passwordStrength');
    const strengthFill = document.getElementById('strengthFill');
    const strengthText = document.getElementById('strengthText');
    
    passwordInput.addEventListener('input', function() {
      const password = this.value;
      let strength = 0;
      
      // Show strength meter when typing
      if (password.length > 0) {
        strengthMeter.classList.add('active');
      } else {
        strengthMeter.classList.remove('active');
      }
      
      // Check password requirements
      checkRequirements(password);
      
      // Length requirement
      if (password.length >= 8) strength += 20;
      
      // Lowercase requirement
      if (/[a-z]/.test(password)) strength += 20;
      
      // Uppercase requirement
      if (/[A-Z]/.test(password)) strength += 20;
      
      // Number requirement
      if (/[0-9]/.test(password)) strength += 20;
      
      // Special character requirement
      if (/[^A-Za-z0-9]/.test(password)) strength += 20;
      
      // Update strength meter
      strengthFill.style.width = `${strength}%`;
      
      // Update strength text and color
      if (strength < 40) {
        strengthFill.style.background = '#d63031';
        strengthText.textContent = 'Password strength: Weak';
      } else if (strength < 80) {
        strengthFill.style.background = '#fdcb6e';
        strengthText.textContent = 'Password strength: Medium';
      } else {
        strengthFill.style.background = '#34a853';
        strengthText.textContent = 'Password strength: Strong';
      }
    });
    
    function checkRequirements(password) {
      const requirements = {
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[^A-Za-z0-9]/.test(password)
      };
      
      // Update requirement indicators
      Object.keys(requirements).forEach(req => {
        const element = document.getElementById(`req-${req}`);
        if (requirements[req]) {
          element.classList.add('valid');
          element.querySelector('i').className = 'fas fa-check-circle';
        } else {
          element.classList.remove('valid');
          element.querySelector('i').className = 'fas fa-circle';
        }
      });
    }
    
    // OTP Timer
    let timeLeft = 15 * 60; // 15 minutes in seconds
    const timerElement = document.getElementById('timer');
    const resendOtpLink = document.getElementById('resendOtp');
    
    function updateTimer() {
      const minutes = Math.floor(timeLeft / 60);
      const seconds = timeLeft % 60;
      
      timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
      
      if (timeLeft > 0) {
        timeLeft--;
        setTimeout(updateTimer, 1000);
      } else {
        resendOtpLink.classList.remove('disabled');
        timerElement.textContent = '00:00';
        timerElement.style.color = '#d63031';
      }
    }
    
    // Start the timer when page loads
    updateTimer();
    
    // Form submission loading state
    document.getElementById('otpForm').addEventListener('submit', function() {
      const submitBtn = document.getElementById('submitBtn');
      submitBtn.classList.add('loading');
      submitBtn.disabled = true;
      submitBtn.querySelector('span').textContent = 'Resetting Password...';
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