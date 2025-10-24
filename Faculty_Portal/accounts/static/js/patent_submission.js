// Enhanced file upload functionality
        document.addEventListener('DOMContentLoaded', function() {
            const fileUploadArea = document.getElementById('fileUploadArea');
            const fileInput = fileUploadArea.querySelector('input[type="file"]');
            const filePreview = document.getElementById('filePreview');
            const fileName = document.getElementById('fileName');
            const removeFileBtn = document.getElementById('removeFile');
            
            // Make the entire upload area clickable
            fileUploadArea.addEventListener('click', function() {
                fileInput.click();
            });
            
            // Drag and drop functionality
            fileUploadArea.addEventListener('dragover', function(e) {
                e.preventDefault();
                fileUploadArea.classList.add('dragover');
            });
            
            fileUploadArea.addEventListener('dragleave', function() {
                fileUploadArea.classList.remove('dragover');
            });
            
            fileUploadArea.addEventListener('drop', function(e) {
                e.preventDefault();
                fileUploadArea.classList.remove('dragover');
                
                if (e.dataTransfer.files.length > 0) {
                    fileInput.files = e.dataTransfer.files;
                    updateFilePreview();
                }
            });
            
            // Handle file selection
            fileInput.addEventListener('change', updateFilePreview);
            
            // Handle file removal
            removeFileBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                fileInput.value = '';
                filePreview.style.display = 'none';
            });
            
            function updateFilePreview() {
                if (fileInput.files.length > 0) {
                    const file = fileInput.files[0];
                    fileName.textContent = file.name;
                    filePreview.style.display = 'block';
                }
            }
            
            // Form validation
            const form = document.getElementById('patentForm');
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
                
                // Check if file is uploaded
                if (!fileInput.files.length) {
                    isValid = false;
                    fileUploadArea.style.borderColor = '#dc3545';
                    
                    if (!fileUploadArea.nextElementSibling || !fileUploadArea.nextElementSibling.classList.contains('text-danger')) {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'text-danger mt-1';
                        errorDiv.textContent = 'Please upload your patent document';
                        fileUploadArea.parentNode.appendChild(errorDiv);
                    }
                } else {
                    fileUploadArea.style.borderColor = '';
                    const errorDiv = fileUploadArea.parentNode.querySelector('.text-danger');
                    if (errorDiv) {
                        errorDiv.remove();
                    }
                }
                
                // Date validation: granted date should be after published date if both exist
                const publishedDate = document.querySelector('input[name="date_published"]');
                const grantedDate = document.querySelector('input[name="date_granted"]');
                
                if (publishedDate.value && grantedDate.value) {
                    const published = new Date(publishedDate.value);
                    const granted = new Date(grantedDate.value);
                    
                    if (granted < published) {
                        isValid = false;
                        grantedDate.classList.add('is-invalid');
                        // Add error message
                        if (!grantedDate.parentNode.querySelector('.date-error')) {
                            const errorDiv = document.createElement('div');
                            errorDiv.className = 'text-danger mt-1 date-error';
                            errorDiv.textContent = 'Granted date cannot be before published date';
                            grantedDate.parentNode.appendChild(errorDiv);
                        }
                    } else {
                        grantedDate.classList.remove('is-invalid');
                        // Remove error message
                        const existingError = grantedDate.parentNode.querySelector('.date-error');
                        if (existingError) {
                            existingError.remove();
                        }
                    }
                }
                
                if (!isValid) {
                    e.preventDefault();
                    // Scroll to first error
                    const firstError = form.querySelector('.is-invalid');
                    if (firstError) {
                        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            });
        });