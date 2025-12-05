/**
 * UYD Data Manager
 * Handles dynamic content loading and updating for the frontend
 */

class UYDDataManager {
    constructor() {
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }

    /**
     * Check if cached data is still valid
     */
    isCacheValid(key) {
        const cached = this.cache.get(key);
        if (!cached) return false;
        
        return (Date.now() - cached.timestamp) < this.cacheTimeout;
    }

    /**
     * Get data from cache or API
     */
    async getData(key, apiCall) {
        if (this.isCacheValid(key)) {
            return this.cache.get(key).data;
        }

        try {
            const data = await apiCall();
            this.cache.set(key, {
                data,
                timestamp: Date.now()
            });
            return data;
        } catch (error) {
            console.error(`Error fetching ${key}:`, error);
            // Return cached data if available, even if expired
            const cached = this.cache.get(key);
            return cached ? cached.data : null;
        }
    }

    /**
     * Load site statistics and update UI
     */
    async loadSiteStats() {
        const stats = await this.getData('siteStats', () => window.uydApi.getSiteStats());
        
        if (stats) {
            this.updateStatsElements(stats);
        }
        
        return stats;
    }

    /**
     * Update statistics elements in the DOM
     */
    updateStatsElements(stats) {
        // Update hero section stats
        const statElements = document.querySelectorAll('.stat-number');
        if (statElements.length >= 3) {
            statElements[0].textContent = stats.engagement?.subscribers || '5000+';
            statElements[1].textContent = stats.programs?.total || '50+';
            statElements[2].textContent = stats.events?.total || '15+';
        }

        // Update main stats section
        const counters = document.querySelectorAll('[data-purecounter-end]');
        counters.forEach(counter => {
            const target = counter.getAttribute('data-purecounter-end');
            if (target === '5000' && stats.engagement?.subscribers) {
                counter.setAttribute('data-purecounter-end', stats.engagement.subscribers);
            }
            // Add more counter updates as needed
        });
    }

    /**
     * Load featured programs
     */
    async loadFeaturedPrograms() {
        const programs = await this.getData('featuredPrograms', () => window.uydApi.getFeaturedPrograms());
        
        if (programs && programs.results) {
            this.updateProgramsSection(programs.results);
        }
        
        return programs;
    }

    /**
     * Update programs section
     */
    updateProgramsSection(programs) {
        // This would update the featured programs section
        // Implementation depends on the specific HTML structure
        console.log('Featured programs loaded:', programs);
    }

    /**
     * Load upcoming events
     */
    async loadUpcomingEvents() {
        const events = await this.getData('upcomingEvents', () => window.uydApi.getUpcomingEvents());

        if (events && events.results) {
            this.updateEventsSection(events.results);
        }

        return events;
    }

    /**
     * Load all events for events page
     */
    async loadAllEvents() {
        const events = await this.getData('allEvents', () => window.uydApi.getEvents());

        if (events && events.results) {
            this.updateEventsPage(events.results);
        } else {
            this.showNoEventsMessage();
        }

        return events;
    }

    /**
     * Load all events for events page
     */
    async loadAllEvents() {
        const events = await this.getData('allEvents', () => window.uydApi.getEvents());

        if (events && events.results) {
            this.updateEventsPage(events.results);
        } else {
            this.showNoEventsMessage();
        }

        return events;
    }

    /**
     * Update events section
     */
    updateEventsSection(events) {
        const eventsContainer = document.querySelector('#events .row');
        if (!eventsContainer || !events.length) return;

        // Clear existing events (keep first 3 as fallback)
        const existingEvents = eventsContainer.querySelectorAll('.col-lg-4');
        if (existingEvents.length > 3) {
            for (let i = 3; i < existingEvents.length; i++) {
                existingEvents[i].remove();
            }
        }

        // Add new events
        events.slice(0, 3).forEach((event, index) => {
            if (index < existingEvents.length) {
                this.updateEventCard(existingEvents[index], event);
            } else {
                const eventCard = this.createEventCard(event);
                eventsContainer.appendChild(eventCard);
            }
        });
    }

    /**
     * Create event card HTML
     */
    createEventCard(event) {
        const eventDate = new Date(event.start_date);
        const month = eventDate.toLocaleDateString('en', { month: 'short' }).toUpperCase();
        const day = eventDate.getDate();

        const col = document.createElement('div');
        col.className = 'col-lg-4 col-md-6';
        col.setAttribute('data-aos', 'zoom-in');
        col.setAttribute('data-aos-delay', '200');

        col.innerHTML = `
            <div class="event-item">
                <div class="event-image">
                    <img src="${event.featured_image || 'assets/img/education/events-3.webp'}" alt="${event.title}" class="img-fluid">
                    <div class="event-date-overlay">
                        <span class="date">${month}<br>${day}</span>
                    </div>
                </div>
                <div class="event-details">
                    <div class="event-category">
                        <span class="badge ${event.event_type}">${event.event_type}</span>
                        <span class="event-time">${eventDate.toLocaleTimeString('en', { hour: '2-digit', minute: '2-digit' })}</span>
                    </div>
                    <h3>${event.title}</h3>
                    <p>${event.description.substring(0, 150)}${event.description.length > 150 ? '...' : ''}</p>
                    <div class="event-info">
                        <div class="info-row">
                            <i class="bi bi-geo-alt"></i>
                            <span>${event.location}</span>
                        </div>
                        <div class="info-row">
                            <i class="bi bi-people"></i>
                            <span>${event.max_participants || 'Open'} Participants</span>
                        </div>
                    </div>
                    <div class="event-footer">
                        <a href="#" class="register-btn" onclick="window.uydData.registerForEvent(${event.id})">Register Now</a>
                        <div class="event-share">
                            <i class="bi bi-share"></i>
                            <i class="bi bi-heart"></i>
                        </div>
                    </div>
                </div>
            </div>
        `;

        return col;
    }

    /**
     * Update existing event card
     */
    updateEventCard(cardElement, event) {
        const eventDate = new Date(event.start_date);
        const month = eventDate.toLocaleDateString('en', { month: 'short' }).toUpperCase();
        const day = eventDate.getDate();

        // Update date
        const dateElement = cardElement.querySelector('.date');
        if (dateElement) {
            dateElement.innerHTML = `${month}<br>${day}`;
        }

        // Update title
        const titleElement = cardElement.querySelector('h3');
        if (titleElement) {
            titleElement.textContent = event.title;
        }

        // Update description
        const descElement = cardElement.querySelector('p');
        if (descElement) {
            descElement.textContent = event.description.substring(0, 150) + 
                (event.description.length > 150 ? '...' : '');
        }

        // Update location
        const locationElement = cardElement.querySelector('.info-row span');
        if (locationElement) {
            locationElement.textContent = event.location;
        }
    }

    /**
     * Update events page with dynamic content
     */
    updateEventsPage(events) {
        const eventsContainer = document.getElementById('events-list');
        const loadingElement = document.getElementById('events-loading');

        if (!eventsContainer || !events || events.length === 0) {
            this.showNoEventsMessage();
            return;
        }

        // Hide loading
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }

        // Clear existing events except the loading/no-events message
        const existingEvents = eventsContainer.querySelectorAll('.event-item');
        existingEvents.forEach(event => event.remove());

        // Add new events
        events.forEach((event, index) => {
            const eventElement = this.createEventListItem(event, index);
            eventsContainer.appendChild(eventElement);
        });
    }

    /**
     * Create event list item for events page
     */
    createEventListItem(event, index) {
        const eventDate = new Date(event.start_date);
        const day = eventDate.getDate();
        const month = eventDate.toLocaleDateString('en', { month: 'short' }).toUpperCase();

        const eventDiv = document.createElement('div');
        eventDiv.className = 'event-item';
        eventDiv.setAttribute('data-aos', 'fade-up');
        eventDiv.setAttribute('data-aos-delay', (index * 100) + 'ms');

        eventDiv.innerHTML = `
            <div class="event-date">
                <span class="day">${day}</span>
                <span class="month">${month}</span>
            </div>
            <div class="event-content">
                <h3 class="event-title">${event.title}</h3>
                <div class="event-meta">
                    <span><i class="bi bi-clock"></i> ${eventDate.toLocaleTimeString('en', { hour: '2-digit', minute: '2-digit' })}</span>
                    <span><i class="bi bi-geo-alt"></i> ${event.location}</span>
                </div>
                <p class="event-description">${event.description ? event.description.substring(0, 200) + (event.description.length > 200 ? '...' : '') : 'Join us for this exciting event!'}</p>
                <a href="event-details.html?id=${event.id}" class="btn-event-details">Learn More <i class="bi bi-arrow-right"></i></a>
            </div>
        `;

        return eventDiv;
    }

    /**
     * Show no events message
     */
    showNoEventsMessage() {
        const loadingElement = document.getElementById('events-loading');
        const noEventsElement = document.getElementById('no-events-message');

        if (loadingElement) {
            loadingElement.style.display = 'none';
        }

        if (noEventsElement) {
            noEventsElement.classList.remove('d-none');
        }
    }

    /**
     * Load latest news
     */
    async loadLatestNews() {
        const news = await this.getData('latestNews', () => window.uydApi.getLatestNews());
        
        if (news && news.results) {
            this.updateNewsSection(news.results);
        }
        
        return news;
    }

    /**
     * Update news section
     */
    updateNewsSection(articles) {
        const newsContainer = document.querySelector('#recent-resources .row');
        if (!newsContainer || !articles.length) return;

        articles.slice(0, 4).forEach((article, index) => {
            const existingItem = newsContainer.children[index];
            if (existingItem) {
                this.updateNewsItem(existingItem, article);
            }
        });
    }

    /**
     * Update individual news item
     */
    updateNewsItem(itemElement, article) {
        const titleElement = itemElement.querySelector('.post-title a');
        if (titleElement) {
            titleElement.textContent = article.title;
            titleElement.href = `news-details.html?id=${article.id}`;
        }

        const descElement = itemElement.querySelector('.post-description');
        if (descElement) {
            descElement.textContent = article.excerpt || article.content.substring(0, 150) + '...';
        }

        const dateElement = itemElement.querySelector('.post-date');
        if (dateElement) {
            const publishDate = new Date(article.publish_date);
            dateElement.textContent = publishDate.toLocaleDateString('en', { 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric' 
            });
        }

        const categoryElement = itemElement.querySelector('.category');
        if (categoryElement && article.category) {
            categoryElement.textContent = article.category.name;
        }
    }

    /**
     * Handle newsletter subscription
     */
    async subscribeNewsletter(email) {
        try {
            const result = await window.uydApi.subscribe(email);
            
            // Show success message
            this.showNotification('Successfully subscribed to newsletter!', 'success');
            
            return result;
        } catch (error) {
            console.error('Newsletter subscription failed:', error);
            this.showNotification('Subscription failed. Please try again.', 'error');
            throw error;
        }
    }

    /**
     * Handle event registration
     */
    async registerForEvent(eventId) {
        // This would typically open a modal or redirect to registration page
        console.log('Register for event:', eventId);
        // Implementation depends on your registration flow
    }

    /**
     * Show notification to user
     */
    showNotification(message, type = 'info') {
        // Create a simple notification system
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#007bff'};
            color: white;
            border-radius: 5px;
            z-index: 10000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Remove after 5 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 5000);
    }

    /**
     * Initialize data loading
     */
    async init() {
        try {
            // Load all data in parallel
            await Promise.all([
                this.loadSiteStats(),
                this.loadUpcomingEvents(),
                this.loadLatestNews(),
                this.loadFeaturedPrograms()
            ]);

            console.log('UYD Data Manager initialized successfully');
        } catch (error) {
            console.error('Error initializing UYD Data Manager:', error);
        }
    }
}

// Create global data manager instance
window.uydData = new UYDDataManager();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UYDDataManager;
}