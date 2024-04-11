// game.js

class Card {
    constructor (title, sentence) {
        this.title = title;
        this.sentence = sentence;
    }
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

function elt(type, ...arguments) {
	const ele = document.createElement(type);
    console.log(arguments)
	// start at 1 or else we'll get the type argument!
	for (let i = 0; i < arguments.length; i++) {
		let child = arguments[i];
		if (typeof child === "string") {
			child = document.createTextNode(child);
		}
		ele.appendChild(child);
	}
	return ele;
}

class Deck {

    constructor(sentences) {
        this.cards = sentences.map(sentence => new Card("Read this sentence", sentence));
        this.shuffle()
    }

    shuffle() {
        this.cards = this.cards.reduce((shuffled, card) => {
            shuffled.splice(getRandomInt(0, shuffled.length), 0, card);
            return shuffled;
        }, []);
    }

    deal() {
        return this.cards.shift();
    }
}


function loadCardAreaFromHand(cardArea, hand) {

    console.log(hand);

    cardArea.innerHTML = '';

    const cardElt = elt('div', 
                        elt('div', hand[0].title),
                        elt('div', elt('div', hand[0].sentence)));
    cardElt.classList.add("card");
    cardElt.style.rotate = `0 0 1 ${getRandomInt(2, -2)}deg`;
    cardElt.childNodes[0].classList.add("card-header");
    cardElt.childNodes[1].classList.add("card-body");

    cardArea.appendChild(cardElt);

    return hand[0].sentence;
}

const cardArea = document.querySelector(".card-area");

let deck = [];
let currentSentence = '';
let score = 0;

const statusText = document.querySelector('#status');

const recordButton = document.querySelector('#record'); //adding a record button to start the recording
const stopButton = document.querySelector('#stop'); //adding a stop button to stop the recording
const nextButton = document.querySelector('#next'); //adding a record button to start the recording
const endButton = document.querySelector('#end'); //adding a stop button to stop the recording
const viewButton = document.querySelector('#view_scores'); //adding a stop button to stop the recording

function main() {
    console.log("DOM fully loaded and parsed");

    // Open Request
    const req = new XMLHttpRequest();
    req.open('GET', '/api/cards', false);
    req.addEventListener('load',function() {
        if(req.status >= 200 && req.status < 400) {
            const cards =JSON.parse(req.responseText);
            console.log(cards);
            deck = new Deck(cards["cards"]);
            deck.shuffle();
            console.log(cardArea);
            currentSentence = loadCardAreaFromHand(cardArea, deck.cards);
        }
    });
    // Error handling
    req.addEventListener('error', function(e) {
        console.log('uh-oh, something went wrong ' + e);
    });
    
    req.send();
    
    //adding an event listener to the record button to start recording audio when the user clicks on it
    recordButton.addEventListener('click', startRecording);
}

document.addEventListener('DOMContentLoaded', main);

async function startRecording () {
    //using the getUserMedia API to get the audio stream from the user's microphone
    const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
        sampleRate: 16000
        } 
    });
    //creating a mediaRecorder object to record the audio stream
    const mediaRecorder = new MediaRecorder(stream);
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
                const transcription =JSON.parse(req.responseText);
                console.log(transcription);
                const s = score_response(transcription["transcription"]);
                console.log(s);
                if (s) {
                    const score_request=new XMLHttpRequest();
                    score_request.open('POST', '/api/store-score', false);

                    const inputed = document.querySelector('#inputed');
                    inputed.value = currentSentence;
                    const scoreInput = document.querySelector('#score-input');
                    scoreInput.value = score;
                    console.log(scoreInput);
                    console.log(score);

                    const f = document.querySelector('#score-form');
                    const data = new FormData(f);

                    // Error handling
                    score_request.addEventListener('load', function() {
                        console.log(JSON.parse(req.responseText));
                    });

                    // Error handling
                    score_request.addEventListener('error', function(e) {
                        console.log('uh-oh, something went wrong ' + e);
                    });

                    score_request.send(data);

                    statusText.style.display = "";
                    statusText.textContent = "Correct!";
                    recordButton.style.display = "none";
                    if (deck.cards.length > 1) {
                        nextButton.style.display = '';
                        nextButton.addEventListener("click", () => {
                            score = 0;
                            statusText.style.display = "";
                            statusText.textContent = "";
                            deck.deal();
                            currentSentence = loadCardAreaFromHand(cardArea, deck.cards);
                            recordButton.style.display = "";
                            nextButton.style.display = 'none';
                        });
                    }
                    else {
                        endButton.style.display = '';
                        endButton.addEventListener("click", () => {
                            statusText.style.display = "";
                            statusText.textContent = "";
                            cardArea.style.display = 'none';
                            endButton.style.display = 'none';
                            viewButton.style.display = '';
                        });
                    }
                }
                else {
                    statusText.style.display = "";
                    statusText.textContent = "Try again";
                    recordButton.style.display = "";
                }
            }
        });
        // Error handling
        req.addEventListener('error', function(e) {
            console.log('uh-oh, something went wrong ' + e);
        });

        req.send(formData);
        
        // plays the audio back to the user
        // const audioUrl = URL.createObjectURL(audioBlob);
        // const audio = new Audio(audioUrl);
        // audio.play();

    });

    //if it's been 3 seconds since the recording started and the user hasn't stopped the recording, stop the recording
    setTimeout(() => {
        stopButton.click();
    }, 5000);
}

function score_response(sentence) {
    score ++;
    console.log(currentSentence.toLowerCase(), sentence.toLowerCase());
    return currentSentence.toLowerCase() === sentence.toLowerCase();
}


// Function to download data to a file
// function download(file, filename) {
//     if (window.navigator.msSaveOrOpenBlob) // IE10+
//         window.navigator.msSaveOrOpenBlob(file, filename);
//     else { // Others
//         var a = document.createElement("a"),
//                 url = URL.createObjectURL(file);
//         a.href = url;
//         a.download = filename;
//         document.body.appendChild(a);
//         a.click();
//         setTimeout(function() {
//             document.body.removeChild(a);
//             window.URL.revokeObjectURL(url);  
//         }, 0); 
//     }
// }