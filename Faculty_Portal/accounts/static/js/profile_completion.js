// File Upload Interactions
        const fileUploadArea = document.getElementById('fileUploadArea');
        const fileInput = fileUploadArea.querySelector('input[type="file"]');
        const imagePreview = document.getElementById('imagePreview');

        fileUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUploadArea.classList.add('dragover');
        });

        fileUploadArea.addEventListener('dragleave', () => {
            fileUploadArea.classList.remove('dragover');
        });

        fileUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUploadArea.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                updateFileUploadDisplay();
            }
        });

        fileInput.addEventListener('change', updateFileUploadDisplay);

        function updateFileUploadDisplay() {
            if (fileInput.files.length > 0) {
                const fileName = fileInput.files[0].name;
                fileUploadArea.innerHTML = `
                    <div class="file-upload-icon">
                        <i class="fas fa-check-circle" style="color: var(--success)"></i>
                    </div>
                    <div class="file-upload-text">
                        <h4>File Selected</h4>
                        <p>${fileName}</p>
                        <p class="file-upload-btn">Change File</p>
                    </div>
                    ${fileInput.outerHTML}
                `;
                
                // Re-attach event listeners
                document.querySelector('#fileUploadArea input[type="file"]').addEventListener('change', updateFileUploadDisplay);
                
                // Update image preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                };
                reader.readAsDataURL(fileInput.files[0]);
            }
        }

        // Progress Animation
        function updateProgress(step) {
            const progress = document.getElementById('progress');
            const progressPercentage = document.getElementById('progressPercentage');
            const percentage = (step / 3) * 100;
            
            progress.style.width = `${percentage}%`;
            progressPercentage.textContent = `${Math.round(percentage)}%`;
            
            // Update step markers
            document.querySelectorAll('.step-marker').forEach((marker, index) => {
                if (index < step) {
                    marker.classList.add('active');
                } else {
                    marker.classList.remove('active');
                }
            });
        }

        // Step Navigation (Preserved Django Functionality)
        function nextStep(step) {
            saveStep(step, () => {
                document.querySelector(`.step${step}`).classList.remove('active');
                document.querySelector(`.step${step+1}`).classList.add('active');
                updateProgress(step);
            });
        }

        function prevStep(step) {
            document.querySelector(`.step${step}`).classList.remove('active');
            document.querySelector(`.step${step-1}`).classList.add('active');
            updateProgress(step - 2);
        }

        function saveStep(step, callback) {
            let formData = new FormData(document.getElementById('multiStepForm'));
            fetch(`/save-step/${step}/`, {
                method: 'POST',
                headers: {'X-CSRFToken': '{{ csrf_token }}'},
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if(data.status === 'success') callback();
                else alert('Please fix errors.');
            });
        }

        function submitForm(step) {
            saveStep(step, () => {
                alert('Profile completed successfully!');
                window.location.href = '/dashboard/';
            });
        }

        // Initialize progress
        document.addEventListener('DOMContentLoaded', function() {
            updateProgress(1);
        });