// Auto-refresh statistics every 30 seconds on dashboard
if (window.location.pathname === '/') {
    setInterval(function() {
        fetch('/api/statistics')
            .then(response => response.json())
            .then(data => {
                // Update statistics if needed
                // This can be enhanced to update the UI without page reload
            })
            .catch(error => console.error('Error fetching statistics:', error));
    }, 30000);
}

