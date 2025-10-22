// Form handler using Alpine.js
        function formHandler() {
            return {
                currentStep: 1,
                totalSteps: 3,
                
                nextStep() {
                    if (this.validateStep(this.currentStep)) {
                        this.currentStep++;
                        this.updateProgress();
                        this.showStep(this.currentStep);
                    }
                },
                
                prevStep() {
                    this.currentStep--;
                    this.updateProgress();
                    this.showStep(this.currentStep);
                },
                
                showStep(step) {
                    document.querySelectorAll('.form-step').forEach(el => {
                        el.classList.remove('active');
                    });
                    document.getElementById(`step-${step}`).classList.add('active');
                },
                
                updateProgress() {
                    const progress = (this.currentStep / this.totalSteps) * 100;
                    document.getElementById('progress-bar').style.width = `${progress}%`;
                    document.getElementById('progress-percentage').textContent = `${Math.round(progress)}%`;
                },
                
                validateStep(step) {
                    // Simple validation for demo purposes
                    // In a real application, you would implement more comprehensive validation
                    if (step === 1) {
                        const title = document.getElementById('{{ form.title_of_paper.id_for_label }}').value;
                        if (!title.trim()) {
                            alert('Please enter a paper title');
                            return false;
                        }
                    }
                    return true;
                },
                
                init() {
                    // Set up event listeners
                    document.querySelectorAll('.next-step-btn').forEach(btn => {
                        btn.addEventListener('click', () => this.nextStep());
                    });
                    
                    document.querySelectorAll('.prev-step-btn').forEach(btn => {
                        btn.addEventListener('click', () => this.prevStep());
                    });
                    
                    // Update summary when form changes
                    this.updateSummary();
                    document.getElementById('publication-form').addEventListener('input', () => {
                        this.updateSummary();
                    });
                    
                    // Set up conditional field for "Other" index
                    this.setupConditionalFields();
                    
                    // Set up file upload preview
                    this.setupFileUpload();
                },
                
                updateSummary() {
                    document.getElementById('summary-title').textContent = 
                        document.getElementById('{{ form.title_of_paper.id_for_label }}').value || 'Not provided';
                    document.getElementById('summary-journal').textContent = 
                        document.getElementById('{{ form.journal_name.id_for_label }}').value || 'Not provided';
                    document.getElementById('summary-authorship').textContent = 
                        document.getElementById('{{ form.author_position.id_for_label }}').value || 'Not provided';
                    
                    const month = document.getElementById('{{ form.month_of_publication.id_for_label }}').value;
                    const year = document.getElementById('{{ form.year_of_publication.id_for_label }}').value;
                    document.getElementById('summary-date').textContent = 
                        (month && year) ? `${month} ${year}` : 'Not provided';
                },
                
                setupConditionalFields() {
                    const indexedInField = document.getElementById('{{ form.indexed_in.id_for_label }}');
                    const otherIndexContainer = document.getElementById('other-index-container');
                    
                    indexedInField.addEventListener('change', function() {
                        if (this.value === 'Other') {
                            otherIndexContainer.style.display = 'block';
                        } else {
                            otherIndexContainer.style.display = 'none';
                        }
                    });
                    
                    // Trigger change event on page load in case "Other" is already selected
                    if (indexedInField.value === 'Other') {
                        otherIndexContainer.style.display = 'block';
                    }
                },
                
                setupFileUpload() {
                    const fileInput = document.getElementById('{{ form.pdf_upload.id_for_label }}');
                    const uploadArea = document.getElementById('upload-area');
                    const filePreview = document.getElementById('file-preview');
                    const fileName = document.getElementById('file-name');
                    const fileSize = document.getElementById('file-size');
                    const removeFileBtn = document.getElementById('remove-file');
                    
                    fileInput.addEventListener('change', function(e) {
                        if (this.files.length > 0) {
                            const file = this.files[0];
                            fileName.textContent = file.name;
                            fileSize.textContent = this.formatFileSize(file.size);
                            filePreview.classList.remove('hidden');
                            uploadArea.classList.add('hidden');
                        }
                    });
                    
                    removeFileBtn.addEventListener('click', function() {
                        fileInput.value = '';
                        filePreview.classList.add('hidden');
                        uploadArea.classList.remove('hidden');
                    });
                    
                    // Drag and drop functionality
                    uploadArea.addEventListener('dragover', function(e) {
                        e.preventDefault();
                        this.classList.add('border-iilm-blue', 'bg-blue-50');
                    });
                    
                    uploadArea.addEventListener('dragleave', function(e) {
                        e.preventDefault();
                        this.classList.remove('border-iilm-blue', 'bg-blue-50');
                    });
                    
                    uploadArea.addEventListener('drop', function(e) {
                        e.preventDefault();
                        this.classList.remove('border-iilm-blue', 'bg-blue-50');
                        
                        if (e.dataTransfer.files.length > 0) {
                            fileInput.files = e.dataTransfer.files;
                            const event = new Event('change', { bubbles: true });
                            fileInput.dispatchEvent(event);
                        }
                    });
                },
                
                formatFileSize(bytes) {
                    if (bytes === 0) return '0 Bytes';
                    const k = 1024;
                    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                    const i = Math.floor(Math.log(bytes) / Math.log(k));
                    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
                }
            }
        }
        
        // Initialize form handler when DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            // Style all form inputs with Tailwind classes
            const formInputs = document.querySelectorAll('input, select, textarea');
            formInputs.forEach(input => {
                input.classList.add('w-full', 'px-4', 'py-3', 'border', 'border-gray-300', 'rounded-lg', 
                                  'focus:outline-none', 'focus:ring-2', 'focus:ring-iilm-blue', 'focus:border-transparent',
                                  'transition-colors', 'duration-200');
            });
            
            // Initialize the form handler
            const handler = formHandler();
            handler.init();
        });