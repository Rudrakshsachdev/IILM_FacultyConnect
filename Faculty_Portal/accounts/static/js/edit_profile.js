// Enhanced profile image upload functionality
        document.addEventListener('DOMContentLoaded', function() {
            const profileUploadArea = document.getElementById('profileUploadArea');
            const profileInput = profileUploadArea.querySelector('input[type="file"]');
            const imagePreview = document.getElementById('imagePreview');
            
            // Make the entire upload area clickable
            profileUploadArea.addEventListener('click', function() {
                profileInput.click();
            });
            
            // Drag and drop functionality
            profileUploadArea.addEventListener('dragover', function(e) {
                e.preventDefault();
                profileUploadArea.classList.add('dragover');
            });
            
            profileUploadArea.addEventListener('dragleave', function() {
                profileUploadArea.classList.remove('dragover');
            });
            
            profileUploadArea.addEventListener('drop', function(e) {
                e.preventDefault();
                profileUploadArea.classList.remove('dragover');
                
                if (e.dataTransfer.files.length > 0) {
                    profileInput.files = e.dataTransfer.files;
                    updateImagePreview();
                }
            });
            
            // Handle file selection
            profileInput.addEventListener('change', updateImagePreview);
            
            function updateImagePreview() {
                if (profileInput.files.length > 0) {
                    const file = profileInput.files[0];
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                        imagePreview.src = e.target.result;
                        imagePreview.style.display = 'block';
                        // Hide the upload icon and text when image is selected
                        profileUploadArea.querySelector('.upload-icon').style.display = 'none';
                        profileUploadArea.querySelector('.upload-text').style.display = 'none';
                    }
                    
                    reader.readAsDataURL(file);
                }
            }
            
            // Form validation and enhancement
            const form = document.getElementById('editProfileForm');
            const inputs = form.querySelectorAll('input, select, textarea');
            
            // Add focus effects
            inputs.forEach(input => {
                input.addEventListener('focus', function() {
                    this.parentElement.classList.add('focused');
                });
                
                input.addEventListener('blur', function() {
                    this.parentElement.classList.remove('focused');
                });
            });
            
            // Real-time validation
            form.addEventListener('submit', function(e) {
                let isValid = true;
                const requiredFields = form.querySelectorAll('[required]');
                
                requiredFields.forEach(field => {
                    if (!field.value.trim()) {
                        isValid = false;
                        field.classList.add('is-invalid');
                        
                        if (!field.parentNode.querySelector('.required-error')) {
                            const errorDiv = document.createElement('div');
                            errorDiv.className = 'invalid-feedback required-error';
                            errorDiv.innerHTML = '<i class="fas fa-exclamation-triangle"></i> This field is required';
                            field.parentNode.appendChild(errorDiv);
                        }
                    } else {
                        field.classList.remove('is-invalid');
                        const existingError = field.parentNode.querySelector('.required-error');
                        if (existingError) {
                            existingError.remove();
                        }
                    }
                });
                
                // Validate URLs if provided
                const urlFields = form.querySelectorAll('input[type="url"]');
                urlFields.forEach(field => {
                    if (field.value.trim() && !isValidUrl(field.value)) {
                        isValid = false;
                        field.classList.add('is-invalid');
                        if (!field.parentNode.querySelector('.url-error')) {
                            const errorDiv = document.createElement('div');
                            errorDiv.className = 'invalid-feedback url-error';
                            errorDiv.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Please enter a valid URL';
                            field.parentNode.appendChild(errorDiv);
                        }
                    } else {
                        field.classList.remove('is-invalid');
                        const existingError = field.parentNode.querySelector('.url-error');
                        if (existingError) {
                            existingError.remove();
                        }
                    }
                });
                
                if (!isValid) {
                    e.preventDefault();
                    // Scroll to first error
                    const firstError = form.querySelector('.is-invalid');
                    if (firstError) {
                        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            });
            
            function isValidUrl(string) {
                try {
                    new URL(string);
                    return true;
                } catch (_) {
                    return false;
                }
            }
            
            // Add character counters for textareas
            const textareas = form.querySelectorAll('textarea');
            textareas.forEach(textarea => {
                const counter = document.createElement('div');
                counter.className = 'form-text character-counter';
                counter.innerHTML = `<i class="fas fa-text-height"></i> <span class="char-count">0</span> characters`;
                textarea.parentNode.appendChild(counter);
                
                textarea.addEventListener('input', function() {
                    const count = this.value.length;
                    counter.querySelector('.char-count').textContent = count;
                });
            });
        });