// Real-time data simulation
        document.addEventListener('DOMContentLoaded', function() {
            const refreshBtn = document.getElementById('refreshData');
            const refreshStatsBtn = document.getElementById('refresh-stats');
            const updateTimeEl = document.getElementById('update-time');
            
            // Function to update the last updated time
            function updateTime() {
                const now = new Date();
                updateTimeEl.textContent = now.toLocaleTimeString();
            }
            
            // Function to simulate data refresh
            function refreshData() {
                // Show loading state
                refreshBtn.innerHTML = '<i class="fas fa-sync-alt refresh-spin mr-2"></i> Refreshing...';
                refreshBtn.disabled = true;
                
                // Simulate API call delay
                setTimeout(() => {
                    // Update time
                    updateTime();
                    
                    // Simulate data changes (in a real app, this would come from an API)
                    const totalSubmissions = document.getElementById('total-submissions');
                    const currentCount = parseInt(totalSubmissions.textContent);
                    
                    // Randomly decide if we should add a submission (for demo purposes)
                    if (Math.random() > 0.7 && currentCount < 10) {
                        totalSubmissions.textContent = currentCount + 1;
                        document.getElementById('pending-count').textContent = currentCount + 1;
                        document.getElementById('cluster-pending').textContent = currentCount + 1;
                        document.getElementById('dean-pending').textContent = currentCount + 1;
                        
                        // Add a notification
                        showNotification('New submission data loaded');
                    } else {
                        showNotification('Data is up to date');
                    }
                    
                    // Reset button
                    refreshBtn.innerHTML = '<i class="fas fa-sync-alt mr-2"></i> Refresh';
                    refreshBtn.disabled = false;
                }, 1500);
            }
            
            // Function to refresh only stats
            function refreshStats() {
                refreshStatsBtn.innerHTML = '<i class="fas fa-sync-alt refresh-spin mr-1"></i> Refreshing...';
                
                setTimeout(() => {
                    // Update time
                    updateTime();
                    
                    // Simulate status changes
                    const clusterPending = document.getElementById('cluster-pending');
                    const clusterApproved = document.getElementById('cluster-approved');
                    const clusterRevision = document.getElementById('cluster-revision');
                    const clusterRejected = document.getElementById('cluster-rejected');
                    
                    const deanPending = document.getElementById('dean-pending');
                    const deanApproved = document.getElementById('dean-approved');
                    const deanRejected = document.getElementById('dean-rejected');
                    
                    // Random status updates for demo
                    if (parseInt(clusterPending.textContent) > 0 && Math.random() > 0.5) {
                        clusterPending.textContent = parseInt(clusterPending.textContent) - 1;
                        
                        if (Math.random() > 0.7) {
                            clusterApproved.textContent = parseInt(clusterApproved.textContent) + 1;
                        } else if (Math.random() > 0.5) {
                            clusterRevision.textContent = parseInt(clusterRevision.textContent) + 1;
                        } else {
                            clusterRejected.textContent = parseInt(clusterRejected.textContent) + 1;
                        }
                        
                        // Update dean stats if cluster approved
                        if (Math.random() > 0.8) {
                            deanPending.textContent = parseInt(deanPending.textContent) - 1;
                            deanApproved.textContent = parseInt(deanApproved.textContent) + 1;
                        }
                    }
                    
                    refreshStatsBtn.innerHTML = '<i class="fas fa-sync-alt mr-1"></i> Refresh Stats';
                    showNotification('Status statistics updated');
                }, 1000);
            }
            
            // Function to show notifications
            function showNotification(message) {
                // Create notification element
                const notification = document.createElement('div');
                notification.className = 'fixed top-20 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50 transform transition-transform duration-300 translate-x-0';
                notification.innerHTML = `
                    <div class="flex items-center">
                        <i class="fas fa-check-circle mr-2"></i>
                        <span>${message}</span>
                    </div>
                `;
                
                document.body.appendChild(notification);
                
                // Remove notification after 3 seconds
                setTimeout(() => {
                    notification.classList.add('translate-x-full');
                    setTimeout(() => {
                        document.body.removeChild(notification);
                    }, 300);
                }, 3000);
            }
            
            // Add event listeners
            refreshBtn.addEventListener('click', refreshData);
            refreshStatsBtn.addEventListener('click', refreshStats);
            
            // Add hover effects to table rows
            const tableRows = document.querySelectorAll('tbody tr');
            tableRows.forEach(row => {
                row.addEventListener('mouseenter', function() {
                    this.classList.add('bg-blue-50');
                });
                row.addEventListener('mouseleave', function() {
                    this.classList.remove('bg-blue-50');
                });
            });
            
            // Initialize the update time
            updateTime();
            
            // Auto-refresh data every 30 seconds (optional)
            // setInterval(refreshData, 30000);
        });