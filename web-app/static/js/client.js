const recordButton = document.getElementById('record'); //adding a record button to start the recording
const stopButton = document.getElementById('stop'); //adding a stop button to stop the recording
let mediaRecorder; //creating a mediaRecorder object to record the audio

//adding an event listener to the record button to start recording audio when the user clicks on it
recordButton.addEventListener('click', async () => { 
    //using the getUserMedia API to get the audio stream from the user's microphone
    const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
        sampleRate: 16000
        } 
    });
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
        const audioBlob = new Blob(audioChunks , { type : 'audio/mp3' });
        //now send the audioBlob to the ML client to process the audio and ge the prediction
        const formData = new FormData();
        formData.set('audio', audioBlob, 'test.mp3');

        // Open Request
        const req=new XMLHttpRequest();
        req.open('POST', 'http://localhost:9696/api/transcribe', true);
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

        // req.setRequestHeader("Content-Type", "multipart/form-data");

        req.send(formData);
        
        // plays the audio back to the user
        // const audioUrl = URL.createObjectURL(audioBlob);
        // const audio = new Audio(audioUrl);
        // audio.play();

    });

    

    //if it's been 3 seconds since the recording started and the user hasn't stopped the recording, stop the recording
    setTimeout(() => {
        mediaRecorder.stop();
    }, 3000);
});

// Function to download data to a file
function download(file, filename) {
    if (window.navigator.msSaveOrOpenBlob) // IE10+
        window.navigator.msSaveOrOpenBlob(file, filename);
    else { // Others
        var a = document.createElement("a"),
                url = URL.createObjectURL(file);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);  
        }, 0); 
    }
}