console.log("JavaScript file loaded");
document.querySelector('.menu-icon').addEventListener('click', function() {
    document.querySelector('.menu-dropdown').classList.toggle('show');
});
function connectToDatabase() {
    const databaseUrl = document.getElementById('database-url').value;
    // Placeholder: Add code to connect to the database using the provided URL
    document.getElementById('connection-status').textContent = 'Connected to the database!';
}

function searchDatabase() {
    const searchTerm = document.getElementById('search-input').value;
    // Placeholder: Add code to search the database using the provided search term
    console.log('Searching the database for:', searchTerm);
}

function saveApiKey() {
    const apiKey = document.getElementById('api-key').value;
    // Placeholder: Add code to save the API key securely
    document.getElementById('api-status').textContent = 'API key saved!';
}

document.getElementById('connect-button').addEventListener('click', connectToDatabase);
document.querySelector('.search-logo').addEventListener('click', searchDatabase);
document.getElementById('save-key-button').addEventListener('click', saveApiKey);