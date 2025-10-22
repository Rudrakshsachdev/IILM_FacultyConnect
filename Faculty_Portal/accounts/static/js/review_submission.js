// Character count for remarks
        const remarksTextarea = document.getElementById('remarks');
        const charCount = document.getElementById('charCount');
        
        remarksTextarea.addEventListener('input', function() {
            charCount.textContent = this.value.length;
        });

        // Form submission confirmation
        document.getElementById('reviewForm').addEventListener('submit', function(e) {
            const status = document.querySelector('input[name="status"]:checked').value;
            const remarks = remarksTextarea.value.trim();
            
            if (!remarks) {
                e.preventDefault();
                alert('Please provide remarks for your review decision.');
                remarksTextarea.focus();
                return;
            }
            
            let message = '';
            if (status === 'approved_by_cluster') {
                message = 'Are you sure you want to APPROVE this submission?';
            } else if (status === 'rejected_by_cluster') {
                message = 'Are you sure you want to REJECT this submission?';
            } else {
                message = 'Are you sure you want to request REVISIONS for this submission?';
            }
            
            if (!confirm(message)) {
                e.preventDefault();
            }
        });

        // PDF viewer controls (basic implementation)
        let zoomLevel = 1;
        const zoomInBtn = document.getElementById('zoom-in');
        const zoomOutBtn = document.getElementById('zoom-out');
        const zoomLevelDisplay = document.getElementById('zoom-level');
        const pdfViewer = document.getElementById('pdf-viewer');
        
        if (zoomInBtn && zoomOutBtn) {
            zoomInBtn.addEventListener('click', function() {
                if (zoomLevel < 2) {
                    zoomLevel += 0.1;
                    updateZoom();
                }
            });
            
            zoomOutBtn.addEventListener('click', function() {
                if (zoomLevel > 0.5) {
                    zoomLevel -= 0.1;
                    updateZoom();
                }
            });
            
            function updateZoom() {
                const iframe = pdfViewer.querySelector('iframe');
                if (iframe) {
                    iframe.style.transform = `scale(${zoomLevel})`;
                    iframe.style.transformOrigin = '0 0';
                    iframe.style.width = `${100 / zoomLevel}%`;
                    iframe.style.height = `${100 / zoomLevel}%`;
                }
                zoomLevelDisplay.textContent = `${Math.round(zoomLevel * 100)}%`;
            }
        }

        // Add animation to form elements
        document.addEventListener('DOMContentLoaded', function() {
            const formGroups = document.querySelectorAll('.form-group');
            formGroups.forEach((group, index) => {
                group.style.animationDelay = `${index * 0.1}s`;
            });
        });