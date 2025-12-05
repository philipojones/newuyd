/**
 * UYD API Client
 * JavaScript client for interacting with the UYD Django backend API
 */

class UYDApiClient {
    constructor(baseURL = 'http://127.0.0.1:8000') {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('uyd_token');
    }

    /**
     * Set authentication token
     */
    setToken(token) {
        this.token = token;
        localStorage.setItem('uyd_token', token);
    }

    /**
     * Remove authentication token
     */
    removeToken() {
        this.token = null;
        localStorage.removeItem('uyd_token');
    }

    /**
     * Get default headers for API requests
     */
    getHeaders(includeAuth = true) {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (includeAuth && this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        return headers;
    }

    /**
     * Make HTTP request
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: this.getHeaders(options.includeAuth !== false),
            ...options,
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            
            return await response.text();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    /**
     * GET request
     */
    async get(endpoint, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const url = queryString ? `${endpoint}?${queryString}` : endpoint;
        
        return this.request(url, {
            method: 'GET',
        });
    }

    /**
     * POST request
     */
    async post(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    /**
     * PUT request
     */
    async put(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    /**
     * DELETE request
     */
    async delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE',
        });
    }

    // Core API methods
    async getSiteStats() {
        return this.get('/api/core/stats/');
    }

    // Programs API methods
    async getPrograms(params = {}) {
        return this.get('/api/programs/', params);
    }

    async getFeaturedPrograms() {
        return this.get('/api/programs/featured/');
    }

    async getProgram(id) {
        return this.get(`/api/programs/${id}`);
    }

    // Events API methods
    async getEvents(params = {}) {
        return this.get('/api/events/', params);
    }

    async getUpcomingEvents() {
        return this.get('/api/events/upcoming/');
    }

    async getEvent(id) {
        return this.get(`/api/events/${id}`);
    }

    // News API methods
    async getNews(params = {}) {
        return this.get('/api/news/', params);
    }

    async getFeaturedNews() {
        return this.get('/api/news/featured/');
    }

    async getLatestNews() {
        return this.get('/api/news/latest/');
    }

    async getNewsArticle(id) {
        return this.get(`/api/news/${id}`);
    }

    // Newsletter subscription (placeholder - not implemented in FastAPI yet)
    async subscribe(email, subscriptionType = 'general') {
        // For now, just return success - implement later if needed
        console.log('Newsletter subscription:', email, subscriptionType);
        return { success: true };
    }

    // Authentication methods
    async login(email, password) {
        const response = await this.post('/token/', {
            email,
            password
        }, { includeAuth: false });
        
        if (response.access) {
            this.setToken(response.access);
        }
        
        return response;
    }

    async refreshToken() {
        const refreshToken = localStorage.getItem('uyd_refresh_token');
        if (!refreshToken) {
            throw new Error('No refresh token available');
        }

        const response = await this.post('/token/refresh/', {
            refresh: refreshToken
        }, { includeAuth: false });

        if (response.access) {
            this.setToken(response.access);
        }

        return response;
    }

    logout() {
        this.removeToken();
        localStorage.removeItem('uyd_refresh_token');
    }
}

// Create global API client instance
window.uydApi = new UYDApiClient();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UYDApiClient;
}