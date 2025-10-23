// Dashboard Data with URLs
        const dashboardData = {
            forms: [
                {
                    id: 1,
                    title: "Journal Publication",
                    description: "Submit your journal publication details for review and approval.",
                    icon: "fas fa-file-alt",
                    category: "publication",
                    status: "active",
                    usage: 45,
                    recent: true,
                    url: "{% url 'journal_publication' %}"
                },
                {
                    id: 2,
                    title: "Book Publication",
                    description: "Provide information about published books and monographs.",
                    icon: "fas fa-book",
                    category: "publication",
                    status: "active",
                    usage: 32,
                    recent: false,
                    
                },
                {
                    id: 3,
                    title: "Book Chapter",
                    description: "Submit details of book chapters authored or co-authored.",
                    icon: "fas fa-book-open",
                    category: "publication",
                    status: "active",
                    usage: 28,
                    recent: true,
                    
                },
                {
                    id: 4,
                    title: "Conference Publication",
                    description: "Enter details for your conference papers and presentations.",
                    icon: "fas fa-microphone",
                    category: "publication",
                    status: "active",
                    usage: 38,
                    recent: false,
                   
                },
                {
                    id: 5,
                    title: "Patent",
                    description: "Submit information about patents filed or granted.",
                    icon: "fas fa-certificate",
                    category: "recognition",
                    status: "active",
                    usage: 15,
                    recent: true,
                    
                },
                {
                    id: 6,
                    title: "Consultancy Project",
                    description: "Fill details about consultancy and funded projects.",
                    icon: "fas fa-handshake",
                    category: "project",
                    status: "active",
                    usage: 22,
                    recent: false,
                   
                },
                {
                    id: 7,
                    title: "Research Grant",
                    description: "Record grants or research funding obtained.",
                    icon: "fas fa-money-bill-wave",
                    category: "project",
                    status: "active",
                    usage: 18,
                    recent: true,
                    
                },
                {
                    id: 8,
                    title: "PhD Guidance",
                    description: "Provide details of PhD guidance or supervision.",
                    icon: "fas fa-user-graduate",
                    category: "recognition",
                    status: "active",
                    usage: 25,
                    recent: false,
                   
                },
                {
                    id: 9,
                    title: "Workshops & FDPs",
                    description: "Submit info about workshops or FDPs attended or conducted.",
                    icon: "fas fa-chalkboard-teacher",
                    category: "collaboration",
                    status: "active",
                    usage: 35,
                    recent: true,
                   
                },
                {
                    id: 10,
                    title: "Awards & Recognitions",
                    description: "Record any research awards or recognitions received.",
                    icon: "fas fa-trophy",
                    category: "recognition",
                    status: "active",
                    usage: 20,
                    recent: false,
                  
                },
                {
                    id: 11,
                    title: "MOUs & Collaborations",
                    description: "Submit details about research MOUs or collaborations.",
                    icon: "fas fa-handshake",
                    category: "collaboration",
                    status: "active",
                    usage: 12,
                    recent: true,
                   
                },
                {
                    id: 12,
                    title: "Copyright",
                    description: "Provide information about copyright registrations.",
                    icon: "fas fa-copyright",
                    category: "recognition",
                    status: "active",
                    usage: 8,
                    recent: false,
                   
                },
                {
                    id: 13,
                    title: "Research Projects",
                    description: "Enter details of ongoing or completed research projects.",
                    icon: "fas fa-project-diagram",
                    category: "project",
                    status: "active",
                    usage: 30,
                    recent: true,
                   
                }
            ],
            activities: [
                {
                    id: 1,
                    title: "Journal Publication Submitted",
                    time: "2 hours ago",
                    status: "pending",
                    icon: "fas fa-file-alt"
                },
                {
                    id: 2,
                    title: "Book Chapter Approved",
                    time: "1 day ago",
                    status: "approved",
                    icon: "fas fa-book-open"
                },
                {
                    id: 3,
                    title: "Conference Paper Review Completed",
                    time: "2 days ago",
                    status: "completed",
                    icon: "fas fa-microphone"
                },
                {
                    id: 4,
                    title: "Research Grant Application",
                    time: "3 days ago",
                    status: "pending",
                    icon: "fas fa-money-bill-wave"
                },
                {
                    id: 5,
                    title: "Patent Filed Successfully",
                    time: "1 week ago",
                    status: "completed",
                    icon: "fas fa-certificate"
                }
            ]
        };

        // High-Level JavaScript Features
        class ResearchDashboard {
            constructor() {
                this.forms = dashboardData.forms;
                this.activities = dashboardData.activities;
                this.filteredForms = [...this.forms];
                this.searchTerm = '';
                this.categoryFilter = 'all';
                this.statusFilter = 'all';
                
                this.init();
            }
            
            init() {
                this.renderForms();
                this.renderActivities();
                this.setupEventListeners();
                this.showWelcomeToast();
                this.startLiveUpdates();
            }
            
            renderForms() {
                const cardGrid = document.getElementById('cardGrid');
                cardGrid.innerHTML = '';
                
                this.filteredForms.forEach((form, index) => {
                    const card = document.createElement('div');
                    card.className = 'card fade-in';
                    card.style.animationDelay = `${index * 0.1}s`;
                    
                    // Use the actual URL from the form data
                    const formUrl = form.url || '#';
                    
                    card.innerHTML = `
                        <div class="card-icon">
                            <i class="${form.icon}"></i>
                        </div>
                        <h3>${form.title}</h3>
                        <p>${form.description}</p>
                        <a href="${formUrl}" class="form-link" data-id="${form.id}">
                            <i class="fas fa-external-link-alt"></i> Open Form
                        </a>
                    `;
                    
                    cardGrid.appendChild(card);
                });
                
                // Add click event to form links for analytics/confirmation
                document.querySelectorAll('.form-link').forEach(link => {
                    link.addEventListener('click', (e) => {
                        const formId = e.target.closest('.form-link').getAttribute('data-id');
                        const form = this.forms.find(f => f.id == formId);
                        
                        // Only show toast if it's a placeholder link
                        if (link.getAttribute('href') === '#') {
                            e.preventDefault();
                            this.showToast(`Opening ${form.title} form`, 'info');
                            
                            // Simulate form opening with a delay
                            setTimeout(() => {
                                console.log(`Opening form: ${form.title}`);
                            }, 1000);
                        } else {
                            // For actual URLs, just track the click
                            this.showToast(`Redirecting to ${form.title} form`, 'info');
                        }
                    });
                });
            }
            
            renderActivities() {
                const activityList = document.getElementById('activityList');
                activityList.innerHTML = '';
                
                this.activities.forEach(activity => {
                    const item = document.createElement('li');
                    item.className = 'activity-item';
                    
                    item.innerHTML = `
                        <div class="activity-icon">
                            <i class="${activity.icon}"></i>
                        </div>
                        <div class="activity-content">
                            <div class="activity-title">${activity.title}</div>
                            <div class="activity-time">${activity.time}</div>
                        </div>
                        <div class="activity-status status-${activity.status}">
                            ${activity.status.charAt(0).toUpperCase() + activity.status.slice(1)}
                        </div>
                    `;
                    
                    activityList.appendChild(item);
                });
            }
            
            setupEventListeners() {
                // Search functionality
                document.getElementById('searchInput').addEventListener('input', (e) => {
                    this.searchTerm = e.target.value.toLowerCase();
                    this.applyFilters();
                });
                
                // Category filter
                document.getElementById('categoryFilter').addEventListener('change', (e) => {
                    this.categoryFilter = e.target.value;
                    this.applyFilters();
                });
                
                // Status filter
                document.getElementById('statusFilter').addEventListener('change', (e) => {
                    this.statusFilter = e.target.value;
                    this.applyFilters();
                });
                
                // Notification badge
                document.getElementById('notificationBadge').addEventListener('click', () => {
                    this.showNotifications();
                });
                
                // Stat cards click events
                document.querySelectorAll('.stat-card').forEach(card => {
                    card.addEventListener('click', () => {
                        const statType = card.getAttribute('data-stat');
                        this.filterByStat(statType);
                    });
                });
            }
            
            applyFilters() {
                this.filteredForms = this.forms.filter(form => {
                    // Search filter
                    const matchesSearch = form.title.toLowerCase().includes(this.searchTerm) || 
                                         form.description.toLowerCase().includes(this.searchTerm);
                    
                    // Category filter
                    const matchesCategory = this.categoryFilter === 'all' || form.category === this.categoryFilter;
                    
                    // Status filter
                    let matchesStatus = true;
                    if (this.statusFilter === 'popular') {
                        matchesStatus = form.usage > 25;
                    } else if (this.statusFilter === 'recent') {
                        matchesStatus = form.recent;
                    }
                    
                    return matchesSearch && matchesCategory && matchesStatus;
                });
                
                this.renderForms();
            }
            
            filterByStat(statType) {
                let filterValue = 'all';
                
                switch(statType) {
                    case 'submissions':
                        filterValue = 'publication';
                        break;
                    case 'pending':
                        // Show notification toast for pending items
                        this.showToast('You have 5 submissions pending review', 'warning');
                        return;
                    case 'approved':
                        filterValue = 'recognition';
                        break;
                    case 'monthly':
                        // Show recent items
                        document.getElementById('statusFilter').value = 'recent';
                        this.statusFilter = 'recent';
                        this.applyFilters();
                        return;
                }
                
                document.getElementById('categoryFilter').value = filterValue;
                this.categoryFilter = filterValue;
                this.applyFilters();
                
                // Pulse animation for the filtered stat card
                const statCard = document.querySelector(`[data-stat="${statType}"]`);
                statCard.classList.add('pulse');
                setTimeout(() => {
                    statCard.classList.remove('pulse');
                }, 2000);
            }
            
            openForm(formId) {
                const form = this.forms.find(f => f.id == formId);
                
                // Use the actual URL if available
                if (form.url && form.url !== '#') {
                    window.location.href = form.url;
                } else {
                    this.showToast(`Opening ${form.title} form`, 'info');
                    
                    // Simulate form opening with a delay
                    setTimeout(() => {
                        console.log(`Opening form: ${form.title}`);
                    }, 1000);
                }
            }
            
            showNotifications() {
                const pendingCount = document.getElementById('pendingReviews').textContent;
                this.showToast(`You have ${pendingCount} submissions pending review`, 'warning');
                
                // Pulse the notification badge
                const badge = document.getElementById('notificationBadge');
                badge.classList.add('pulse');
                setTimeout(() => {
                    badge.classList.remove('pulse');
                }, 2000);
            }
            
            showToast(message, type = 'info') {
                const toastContainer = document.getElementById('toastContainer');
                const toastId = 'toast-' + Date.now();
                
                const icons = {
                    success: 'fas fa-check-circle',
                    info: 'fas fa-info-circle',
                    warning: 'fas fa-exclamation-triangle'
                };
                
                const toast = document.createElement('div');
                toast.className = `toast toast-${type}`;
                toast.id = toastId;
                
                toast.innerHTML = `
                    <div class="toast-icon">
                        <i class="${icons[type]}"></i>
                    </div>
                    <div class="toast-content">
                        <div class="toast-title">Notification</div>
                        <div class="toast-message">${message}</div>
                    </div>
                    <button class="toast-close" onclick="document.getElementById('${toastId}').remove()">
                        <i class="fas fa-times"></i>
                    </button>
                `;
                
                toastContainer.appendChild(toast);
                
                // Show toast with animation
                setTimeout(() => {
                    toast.classList.add('show');
                }, 100);
                
                // Auto remove after 5 seconds
                setTimeout(() => {
                    if (document.getElementById(toastId)) {
                        toast.classList.remove('show');
                        setTimeout(() => {
                            if (document.getElementById(toastId)) {
                                document.getElementById(toastId).remove();
                            }
                        }, 300);
                    }
                }, 5000);
            }
            
            showWelcomeToast() {
                setTimeout(() => {
                    this.showToast('Welcome to your Research Dashboard!', 'success');
                }, 1000);
            }
            
            startLiveUpdates() {
                // Simulate live data updates
                setInterval(() => {
                    this.updateStats();
                }, 10000);
                
                // Simulate new activity
                setInterval(() => {
                    this.addRandomActivity();
                }, 15000);
            }
            
            updateStats() {
                // Randomly update stats to simulate live data
                const stats = ['totalSubmissions', 'pendingReviews', 'approvedSubmissions', 'monthlySubmissions'];
                
                stats.forEach(statId => {
                    const element = document.getElementById(statId);
                    const currentValue = parseInt(element.textContent);
                    const change = Math.random() > 0.5 ? 1 : -1;
                    const newValue = Math.max(1, currentValue + change);
                    
                    element.textContent = newValue;
                    
                    // Add visual feedback
                    element.style.color = change > 0 ? '#28a745' : '#dc3545';
                    setTimeout(() => {
                        element.style.color = '';
                    }, 1000);
                });
            }
            
            addRandomActivity() {
                const activities = [
                    {
                        title: "New Journal Submission",
                        icon: "fas fa-file-alt",
                        status: "pending"
                    },
                    {
                        title: "Research Project Updated",
                        icon: "fas fa-project-diagram",
                        status: "completed"
                    },
                    {
                        title: "Conference Paper Approved",
                        icon: "fas fa-microphone",
                        status: "approved"
                    }
                ];
                
                const randomActivity = activities[Math.floor(Math.random() * activities.length)];
                const timeOptions = ["Just now", "5 minutes ago", "10 minutes ago"];
                
                this.activities.unshift({
                    id: this.activities.length + 1,
                    title: randomActivity.title,
                    time: timeOptions[Math.floor(Math.random() * timeOptions.length)],
                    status: randomActivity.status,
                    icon: randomActivity.icon
                });
                
                // Keep only 5 most recent activities
                if (this.activities.length > 5) {
                    this.activities.pop();
                }
                
                this.renderActivities();
                
                // Show notification for new activity
                this.showToast(`New activity: ${randomActivity.title}`, 'info');
            }
        }

        // Initialize the dashboard when DOM is loaded
        document.addEventListener('DOMContentLoaded', () => {
            new ResearchDashboard();
        });