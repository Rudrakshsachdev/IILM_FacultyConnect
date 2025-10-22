// OTP input handling
    const otpDigits = document.querySelectorAll('.otp-digit');
    const fullOtpInput = document.getElementById('fullOtp');
    
    otpDigits.forEach((digit, index) => {
      digit.addEventListener('input', function() {
        // Auto-focus next input
        if (this.value.length === 1 && index < otpDigits.length - 1) {
          otpDigits[index + 1].focus();
        }
        
        // Update hidden input with full OTP
        updateFullOtp();
      });
      
      digit.addEventListener('keydown', function(e) {
        // Handle backspace
        if (e.key === 'Backspace' && this.value.length === 0 && index > 0) {
          otpDigits[index - 1].focus();
        }
      });
    });
    
    function updateFullOtp() {
      const fullOtp = Array.from(otpDigits).map(digit => digit.value).join('');
      fullOtpInput.value = fullOtp;
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
      submitBtn.querySelector('span').textContent = 'Verifying...';
    });
    
    // Auto-focus first OTP input on page load
    document.addEventListener('DOMContentLoaded', function() {
      otpDigits[0].focus();
    });