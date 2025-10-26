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
            const form = document.getElementById('industryForm');
            form.addEventListener('submit', function(e) {
                let isValid = true;
                const requiredFields = form.querySelectorAll('input[required], select[required], textarea[required]');
                
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
                        errorDiv.textContent = 'Please upload supporting document';
                        fileUploadArea.parentNode.appendChild(errorDiv);
                    }
                } else {
                    fileUploadArea.style.borderColor = '';
                    const errorDiv = fileUploadArea.parentNode.querySelector('.text-danger');
                    if (errorDiv) {
                        errorDiv.remove();
                    }
                }
                
                // Date validation: end date should not be before start date
                const startDate = document.querySelector('input[name="start_date"]');
                const endDate = document.querySelector('input[name="end_date"]');
                
                if (startDate.value && endDate.value) {
                    const start = new Date(startDate.value);
                    const end = new Date(endDate.value);
                    
                    if (end < start) {
                        isValid = false;
                        endDate.classList.add('is-invalid');
                        // Add error message
                        if (!endDate.parentNode.querySelector('.date-error')) {
                            const errorDiv = document.createElement('div');
                            errorDiv.className = 'text-danger mt-1 date-error';
                            errorDiv.textContent = 'End date cannot be before start date';
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
                
                // Date validation: start date should not be in the future
                if (startDate.value) {
                    const start = new Date(startDate.value);
                    const today = new Date();
                    
                    if (start > today) {
                        isValid = false;
                        startDate.classList.add('is-invalid');
                        // Add error message
                        if (!startDate.parentNode.querySelector('.start-date-error')) {
                            const errorDiv = document.createElement('div');
                            errorDiv.className = 'text-danger mt-1 start-date-error';
                            errorDiv.textContent = 'Start date cannot be in the future';
                            startDate.parentNode.appendChild(errorDiv);
                        }
                    } else {
                        startDate.classList.remove('is-invalid');
                        // Remove error message
                        const existingError = startDate.parentNode.querySelector('.start-date-error');
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