// Enhanced profile image upload functionality
        document.addEventListener('DOMContentLoaded', function() {
            const profileUploadArea = document.getElementById('profileUploadArea');
            const profileInput = profileUploadArea.querySelector('input[type="file"]');
            const profilePreview = document.getElementById('profilePreview');
            
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
                    updateProfilePreview();
                }
            });
            
            // Handle file selection
            profileInput.addEventListener('change', updateProfilePreview);
            
            function updateProfilePreview() {
                if (profileInput.files.length > 0) {
                    const file = profileInput.files[0];
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                        profilePreview.src = e.target.result;
                        profilePreview.style.display = 'block';
                        // Hide the upload icon and text when image is selected
                        profileUploadArea.querySelector('.profile-upload-icon').style.display = 'none';
                        profileUploadArea.querySelector('.profile-upload-text').style.display = 'none';
                    }
                    
                    reader.readAsDataURL(file);
                }
            }
            
            // Form validation
            const form = document.getElementById('facultyProfileForm');
            form.addEventListener('submit', function(e) {
                let isValid = true;
                const requiredFields = form.querySelectorAll('input[required], select[required]');
                
                requiredFields.forEach(field => {
                    if (!field.value.trim()) {
                        isValid = false;
                        field.classList.add('is-invalid');
                        
                        // Add error styling
                        if (!field.nextElementSibling || !field.nextElementSibling.classList.contains('text-danger')) {
                            const errorDiv = document.createElement('div');
                            errorDiv.className = 'text-danger mt-1';
                            errorDiv.textContent = 'This field is required';
                            field.parentNode.appendChild(errorDiv);
                        }
                    } else {
                        field.classList.remove('is-invalid');
                        const errorDiv = field.parentNode.querySelector('.text-danger');
                        if (errorDiv) {
                            errorDiv.remove();
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
                            errorDiv.className = 'text-danger mt-1 url-error';
                            errorDiv.textContent = 'Please enter a valid URL';
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
        });