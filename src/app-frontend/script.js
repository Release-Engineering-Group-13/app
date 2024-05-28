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
        return response.json();  
    })
    .then(data => {
        // Display the response in the responseText textarea
        if (data.prediction == 1) {
            document.getElementById('responseText').value = 'This is a phishing URL!! \nPlease do not visit this URL';
        }
        else {
            document.getElementById('responseText').value = 'This looks like a legitimate URL!! \ntry this URL at your own risk';
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        document.getElementById('responseText').value = 'There was a problem with the fetch operation';
    });
  
}
