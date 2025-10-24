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
            
            // Add styling to Django form fields
            document.querySelectorAll('input, select, textarea').forEach(field => {
                if (!field.classList.contains('form-control') && !field.classList.contains('form-select') && 
                    !field.classList.contains('status-field') && field.type !== 'file') {
                    field.classList.add('django-form-field');
                }
            });
            
            // Form validation
            const form = document.getElementById('researchProjectForm');
            form.addEventListener('submit', function(e) {
                let isValid = true;
                const requiredFields = form.querySelectorAll('[required]');
                
                requiredFields.forEach(field => {
                    if (!field.value.trim()) {
                        isValid = false;
                        field.classList.add('is-invalid');
                        
                        // Add error message if not already present
                        if (!field.parentNode.querySelector('.field-error')) {
                            const errorDiv = document.createElement('div');
                            errorDiv.className = 'text-danger mt-1 field-error';
                            errorDiv.textContent = 'This field is required';
                            field.parentNode.appendChild(errorDiv);
                        }
                    } else {
                        field.classList.remove('is-invalid');
                        // Remove error message if present
                        const existingError = field.parentNode.querySelector('.field-error');
                        if (existingError) {
                            existingError.remove();
                        }
                    }
                });
                
                // Check if file is uploaded
                if (!fileInput.files.length) {
                    isValid = false;
                    fileUploadArea.style.borderColor = '#dc3545';
                    // Add error message if not already present
                    if (!fileUploadArea.parentNode.querySelector('.file-error')) {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'text-danger mt-1 file-error';
                        errorDiv.textContent = 'Please upload the sanctioned letter';
                        fileUploadArea.parentNode.appendChild(errorDiv);
                    }
                } else {
                    fileUploadArea.style.borderColor = '';
                    // Remove error message if present
                    const existingError = fileUploadArea.parentNode.querySelector('.file-error');
                    if (existingError) {
                        existingError.remove();
                    }
                }
                
                // Date validation: end date should be after start date
                const startDate = document.querySelector('input[name="duration_from"]');
                const endDate = document.querySelector('input[name="duration_to"]');
                
                if (startDate.value && endDate.value) {
                    const start = new Date(startDate.value);
                    const end = new Date(endDate.value);
                    
                    if (end <= start) {
                        isValid = false;
                        endDate.classList.add('is-invalid');
                        // Add error message
                        if (!endDate.parentNode.querySelector('.date-error')) {
                            const errorDiv = document.createElement('div');
                            errorDiv.className = 'text-danger mt-1 date-error';
                            errorDiv.textContent = 'End date must be after start date';
                            endDate.parentNode.appendChild(errorDiv);
                        }
                    } else {
                        endDate.classList.remove('is-invalid');
                        // Remove error message
                        const existingError = endDate.parentNode.querySelector('.date-error');
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