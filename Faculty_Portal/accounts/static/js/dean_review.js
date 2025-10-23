// Character count for remarks
        const remarksTextarea = document.getElementById('remarks');
        const charCount = document.getElementById('charCount');
        
        remarksTextarea.addEventListener('input', function() {
            charCount.textContent = this.value.length;
        });

        // Form submission confirmation
        document.getElementById('reviewForm').addEventListener('submit', function(e) {
            const decision = document.querySelector('input[name="action"]:checked').value;
            const remarks = remarksTextarea.value.trim();
            
            if (!remarks) {
                e.preventDefault();
                alert('Please provide remarks for your decision.');
                remarksTextarea.focus();
                return;
            }
            
            let message = '';
            if (decision === 'approve') {
                message = 'Are you sure you want to APPROVE this submission for final publication?';
            } else {
                message = 'Are you sure you want to REJECT this submission?';
            }
            
            if (!confirm(message)) {
                e.preventDefault();
            }
        });

        // Add animation to form elements
        document.addEventListener('DOMContentLoaded', function() {
            // Animate the form elements
            const formGroups = document.querySelectorAll('.form-group');
            formGroups.forEach((group, index) => {
                group.style.animationDelay = `${index * 0.1}s`;
            });
        });