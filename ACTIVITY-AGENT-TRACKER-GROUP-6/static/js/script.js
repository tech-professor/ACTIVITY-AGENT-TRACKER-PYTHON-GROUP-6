document.getElementById('config-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way

    const formData = {
        interval: document.getElementById('interval').value,
        blur: document.getElementById('blur').value,
        scripted_activity_threshold: document.getElementById('scripted_activity_threshold').value,
        battery_threshold: document.getElementById('battery_threshold').value,
    };

    // Send the configuration to the server
    fetch('/api/config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response-message').textContent = data.message;
        document.getElementById('response-message').style.color = 'green'; // Change message color to green
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('response-message').textContent = 'Failed to update configuration.';
    });
});
