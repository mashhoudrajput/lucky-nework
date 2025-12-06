if (window.location.pathname === '/') {
    setInterval(function() {
        fetch('/api/statistics')
            .then(response => response.json())
            .catch(error => console.error('Error:', error));
    }, 30000);
}
