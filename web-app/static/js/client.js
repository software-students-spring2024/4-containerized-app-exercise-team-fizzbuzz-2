// // // client.js

// // $(document).ready(function() {
// //     $('#predict-button').click(function() {
// //         console.log('AJAX request successful'); // Log a message when the AJAX request is successful
// //         $.ajax({
// //             type: 'GET',
// //             url: 'http://localhost:9696/test',
// //             success: function(response) {
// //                 // Parse the JSON response
// //                 var transcription = response.transcription;

// //                 // Display the transcription
// //                 $('#transcription-result').text('Transcription: ' + transcription);
// //             },
// //             error: function(xhr, status, error) {
// //                 console.error('Error:', error);
// //             }
// //         });
// //     });
// // });

// // client.js

// $(document).ready(function() {
//     $('#predict-button').click(function() {
//         console.log('AJAX request successful'); // Log a message when the AJAX request is successful
//         $.ajax({
//             const url = 'http://localhost:3000/hello.json';
//             const req = new XMLHttpRequest();
//             req.open('GET', url, true);,
//             success: function(response) {
//                 // Parse the JSON response
//                 var transcription = response.transcription;

//                 // Display the transcription
//                 $('#transcription-result').text('Transcription: ' + transcription);
//             },
//             error: function(xhr, status, error) {
//                 console.error('Error:', error);
//             }
//         });
//     });
// });

const recordButton = document.getElementById('record'); //adding a record button to start the recording
const stopButton = document.getElementById('stop'); //adding a stop button to stop the recording
let mediaRecorder; //creating a mediaRecorder object to record the audio

//adding an event listener to the record button to start recording audio when the user clicks on it
recordButton.addEventListener('click', async () => { 
    //using the getUserMedia API to get the audio stream from the user's microphone
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    //creating a mediaRecorder object to record the audio stream
    mediaRecorder = new MediaRecorder(stream);
    //starting the mediaRecorder object to record the audio stream
    mediaRecorder.start();
    recordButton.style.display = 'none'; //when recording starts, hide the record button
    stopButton.style.display = ''; //when recording starts, show the stop button
    const audioChunks = []; //creating an array to store the audio chunks

    //adding an event listener to the mediaRecorder object to store the audio chunks in the array when they become available
    mediaRecorder.addEventListener("dataavailable", event => {
        audioChunks.push(event.data);
    });

    //adding an event listener to the stop button to stop the recording when the user clicks on it
    //mostly stylistic stuff + stopping the recording of the media recorder object
    stopButton.addEventListener('click', () => {
        mediaRecorder.stop();
        //when the recording stops, hide the stop button
        stopButton.style.display = 'none';
        //when the recording stops, show the record button
        recordButton.style.display = '';
        
    });

    //here, start to prepare the audio to send to the backend
    mediaRecorder.addEventListener("stop", () => {
        //for example, create a Blob object from the audio chunks and make it a WAV file
        const audioBlob = new Blob(audioChunks , { 'type' : 'audio/wav' });
        //now send the audioBlob to the ML client to process the audio and ge the prediction
        const formData = new FormData();
        formData.append('audio', audioBlob);
        console.log(formData)
        
        // Open Request
        const req=new XMLHttpRequest();
        req.open('POST', 'http://localhost:5000/upload-audio');
        // req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8; audio/wav');
        req.addEventListener('load',function() {
            if(req.status >= 200 && req.status < 400) {
                const messages =JSON.parse(req.responseText);
                console.log(messages)
            }
        });
        // Error handling
        req.addEventListener('error', function(e) {
            console.log('uh-oh, something went wrong ' + e);
        });
        req.send(formData);
        
        //plays the audio back to the user
        // const audioUrl = URL.createObjectURL(audioBlob);
        // const audio = new Audio(audioUrl);
        // audio.play();

    });

    

    //if it's been 3 seconds since the recording started and the user hasn't stopped the recording, stop the recording
    setTimeout(() => {
        mediaRecorder.stop();
    }, 3000);
});