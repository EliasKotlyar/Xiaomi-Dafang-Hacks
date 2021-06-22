var gumStream; //stream from getUserMedia()
var rec; //Recorder.js object
var input; //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

function startRecording() {
    console.log("Recording started");
    /*
    	Simple constraints object, for more advanced audio features see
    	https://addpipe.com/blog/audio-constraints-getusermedia/
    */

    var constraints = {
        audio: true,
        video: false
    }

    /*
    	We're using the standard promise based getUserMedia()
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

    navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

        /*
        	create an audio context after getUserMedia is called
        	sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
        	the sampleRate defaults to the one set in your OS for your playback device
        */
        audioContext = new AudioContext({
            sampleRate: 8000
        });

        /*  assign to gumStream for later use  */
        gumStream = stream;

        /* use the stream */
        input = audioContext.createMediaStreamSource(stream);

        /*
        	Create the Recorder object and configure to record mono sound (1 channel)
        	Recording 2 channels  will double the file size
        */
        rec = new Recorder(input, {
            numChannels: 1
        })

        //start the recording process
        rec.record()
    });
}

function stopRecording() {
    //tell the recorder to stop the recording

    // The Dafang fails to play the last two seconds because some bug on audioplay...
    setTimeout(() => {
        rec.stop();

        //stop microphone access
        gumStream.getAudioTracks()[0].stop();
	    
	rec.exportWAV(sendAudio);
	
	function sendAudio(blob) {
		var xhr = new XMLHttpRequest();
		xhr.onload = function (e) {
		    if (this.readyState === 4) {
			console.log("Server returned: ", e.target.responseText);
		    }
		};
		var fd = new FormData();
		fd.append("audio_data", blob, 'recording.wav');
		xhr.open("POST", "cgi-bin/audio_upload.cgi", true);
		xhr.send(fd);
	}
	console.log("Audio sent");
    }, 2000);
}


