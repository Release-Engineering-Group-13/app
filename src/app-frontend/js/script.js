function sendRequest() {
    // Get the text from the input field
    var inputText = document.getElementById('inputText').value;

    var apiUrl = '{{API_URL}}/get_prediction?input=' + encodeURIComponent(inputText);

    // Make a GET request to the API
    fetch(apiUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();  // parse the JSON from the response
    })
    .then(data => {
        console.log(data);
        // Display the response in the responseText textarea
        if (data.Prediction == 1) {
            // set the response text to the data.Link with the correct message
            document.getElementById('responseText').value = 'This looks like a malicious URL!! \nDo not try this URL: ' + data.Link;
        }
        else {
            document.getElementById('responseText').value = 'This looks like a legitimate URL!! \nSafely try this URL: ' + data.Link;
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        document.getElementById('responseText').value = 'There was a problem with the fetch operation';
    });
}

// execute directly
versionRequest();
function versionRequest() {

    var apiUrl = '{{API_URL}}/get_version';

    fetch(apiUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();  // parse the JSON from the response
    })
    .then(data => {
        console.log('API Version: ' + data.version);
        // Display the response in the responseText textarea
        document.getElementById('versionText').textContent = data.version;
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        document.getElementById('versionText').textContent = 'There was a problem with the version fetch operation';
    });
}
