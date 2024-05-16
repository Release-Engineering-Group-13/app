function sendRequest() {
    // Get the text from the input field
    var inputText = document.getElementById('inputText').value;
	
	var apiUrl = 'http://localhost:8081/get_prediction?input=' + encodeURIComponent(inputText);

    // Make a GET request to the API
    fetch(apiUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(data => {
        // Display the response in the responseText textarea
        document.getElementById('responseText').value = data;
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
