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
            const form = document.getElementById('publicationForm');
            form.addEventListener('submit', function(e) {
                let isValid = true;
                const requiredFields = form.querySelectorAll('.required');
                
                requiredFields.forEach(field => {
                    const input = field.closest('.form-group').querySelector('input, select, textarea');
                    if (!input.value.trim()) {
                        isValid = false;
                        input.classList.add('is-invalid');
                    } else {
                        input.classList.remove('is-invalid');
                    }
                });
                
                // Check if file is uploaded
                if (!fileInput.files.length) {
                    isValid = false;
                    fileUploadArea.style.borderColor = '#dc3545';
                } else {
                    fileUploadArea.style.borderColor = '';
                }
                
                if (!isValid) {
                    e.preventDefault();
                    alert('Please fill in all required fields and upload your research paper.');
                }
            });
        });