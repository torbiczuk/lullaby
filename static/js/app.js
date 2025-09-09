class TicketApp {
    constructor() {
        this.statusBar = document.getElementById('statusBar');
        this.statusIndicator = document.getElementById('statusIndicator');
        this.statusText = document.getElementById('statusText');
        this.summaryCard = document.getElementById('summaryCard');
        this.eventsGrid = document.getElementById('eventsGrid');
        this.loading = document.getElementById('loading');
        this.errorMessage = document.getElementById('errorMessage');
        this.errorText = document.getElementById('errorText');
        this.cacheInfo = document.getElementById('cacheInfo');

        this.init();
    }

    init() {
        this.loadData();
        // Auto-refresh every 5 minutes
        setInterval(() => this.loadData(), 5 * 60 * 1000);
    }

    async loadData() {
        try {
            this.showLoading();

            const response = await fetch('/api/seats');
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Failed to fetch data');
            }

            this.displayData(result);
            this.updateCacheInfo(result);
            this.showSuccess('Dane załadowane pomyślnie');
        } catch (error) {
            console.error('Error loading data:', error);
            this.showError(error.message);
        }
    }

    showLoading() {
        this.loading.style.display = 'block';
        this.summaryCard.style.display = 'none';
        this.eventsGrid.style.display = 'none';
        this.errorMessage.style.display = 'none';

        this.statusIndicator.className = 'status-indicator loading';
        this.statusText.textContent = 'Pobieranie danych...';
    }

    showSuccess(message) {
        this.statusIndicator.className = 'status-indicator success';
        this.statusText.textContent = message;
    }

    showError(errorMsg) {
        this.loading.style.display = 'none';
        this.summaryCard.style.display = 'none';
        this.eventsGrid.style.display = 'none';
        this.errorMessage.style.display = 'block';

        this.statusIndicator.className = 'status-indicator error';
        this.statusText.textContent = 'Błąd pobierania danych';
        this.errorText.textContent = errorMsg;
    }

    displayData(result) {
        const {data, cached_at} = result;
        const {events, summary} = data;

        this.loading.style.display = 'none';
        this.errorMessage.style.display = 'none';
        this.summaryCard.style.display = 'block';
        this.eventsGrid.style.display = 'grid';

        // Update summary
        document.getElementById('totalFree').textContent = summary.free_total;
        document.getElementById('totalTaken').textContent = summary.taken_total;
        document.getElementById('totalAll').textContent = summary.all_total;
        document.getElementById('totalPercent').textContent = `${summary.total_percent}%`;

        // Clear and populate events grid
        this.eventsGrid.innerHTML = '';
        events.forEach(event => {
            const eventCard = this.createEventCard(event);
            this.eventsGrid.appendChild(eventCard);
        });
    }

    createEventCard(event) {
        const card = document.createElement('div');
        card.className = 'event-card';

        const availabilityPercent = Math.round((event.free / event.total) * 100) || 0;

        card.innerHTML = `
            <div class="event-date">${this.formatDate(event.date)}</div>
            <div class="event-stats">
                <div class="event-stat">
                    <span class="event-stat-value">${event.free}</span>
                    <div class="event-stat-label">Wolne</div>
                </div>
                <div class="event-stat">
                    <span class="event-stat-value">${event.taken}</span>
                    <div class="event-stat-label">Zajęte</div>
                </div>
            </div>
            <div class="availability-bar">
                <div class="availability-fill" style="width: ${availabilityPercent}%"></div>
            </div>
            <div class="availability-percent">${availabilityPercent}% dostępne</div>
            <a href="${event.url}" target="_blank" class="event-link">Kup bilet</a>
        `;

        return card;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const options = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            weekday: 'long'
        };
        return date.toLocaleDateString('pl-PL', options);
    }

    updateCacheInfo(result) {
        if (result.cached_at) {
            const cachedDate = new Date(result.cached_at);
            const expiresDate = new Date(result.cache_expires_at);
            const now = new Date();

            console.log('Cache debug:', {
                cached_at: result.cached_at,
                cache_expires_at: result.cache_expires_at,
                cachedDate: cachedDate.toISOString(),
                expiresDate: expiresDate.toISOString(),
                now: now.toISOString(),
                timeDiff: (expiresDate - now) / 1000 / 60
            });

            const timeUntilRefresh = Math.max(0, Math.ceil((expiresDate - now) / 1000 / 60));

            this.cacheInfo.textContent = `Ostatnia aktualizacja: ${cachedDate.toLocaleString('pl-PL')} | Następna za: ${timeUntilRefresh} min`;
        }
    }
}

// Global function for retry button
function loadData() {
    window.ticketApp.loadData();
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.ticketApp = new TicketApp();
});