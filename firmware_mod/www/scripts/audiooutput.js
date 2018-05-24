

'use strict';

var bufferSize = 1024;
var audioContext;
var microphone;
var wsUri;
var SecurePort = "7681";
var UnsecurePort = "7682";
var connected = false;
var WsConnection;
var myPCMProcessingNode ;
var isStarted = false;
var resamplerObj;
var audioInputSelect = document.querySelector('select#audioSource');
var audioRateSelect = document.querySelector('select#audiorate');
var selectors = [audioInputSelect];
var inSampleRate = 48000;
var gainNode;


function getOutVolume()
{
    return document.getElementById("volumeOut").value;
}

function ChangeVolume()
{
    console.log("ChangeVolume");
    if (connected == true)
    {
        var configString = "ServerSetValues [" + getOutSampleRate().toString() + "," + getOutVolume().toString() + "]";
        console.log("Configstring is ="+configString);
        WsConnection.send(configString);
    }
}

function wsOpen(){
    connected = true;
    console.log("connection made.");
    var configString = "ServerSetValues [" + getOutSampleRate().toString() + "," + getOutVolume().toString() + "]";
    console.log("Configstring is ="+configString);
    WsConnection.send(configString);
}

var errorCallback = function(e) {
    alert("Error in getUserMedia: " + e);
};

function handlePWM(e){  }
function wsError(error){
    connected = false;
    console.log('WebSocket Error ' + error.data);
    stop();
}

function WsClose(closeEvent){
    stopAudio();
    stop();
    connected = false;
    console.log('WS connection closed --- Code: ' + closeEvent.code + ' --- reason: ' + closeEvent.reason);
}

function stopAudio()
{
    if (window.localStream != null)
    {
        window.localStream.getAudioTracks()[0].stop();
        //this will stop video and audio both track
        window.localStream.getTracks().map(function (val) {
            val.stop();
        });
    }
    window.localStream = null;
    microphone = null;
    resamplerObj = null;
    audioContext = null;
    WsConnection  = null;
    myPCMProcessingNode  = null;
    resamplerObj = null;
    gainNode  = null;
}

///////////////////////////////////////



function getOutSampleRate()
{
 var outSampleRate =  inSampleRate;
 if (audioRateSelect.selectedIndex > 0)
    outSampleRate = audioRateSelect[audioRateSelect.selectedIndex].value;

 return outSampleRate;

}

function gotDevices(deviceInfos) {
   console.log("gotDevices");
  // Handles being called several times to update labels. Preserve values.
  var values = selectors.map(function(select) {
    return select.value;
  });
  selectors.forEach(function(select) {
    while (select.firstChild) {
      select.removeChild(select.firstChild);
    }
  });
  for (var i = 0; i !== deviceInfos.length; ++i) {
    var deviceInfo = deviceInfos[i];
    var option = document.createElement('option');
    option.value = deviceInfo.deviceId;
    if (deviceInfo.kind === 'audioinput') {
      option.text = deviceInfo.label ||
          'microphone ' + (audioInputSelect.length + 1);
      audioInputSelect.appendChild(option);
    }
  }
  selectors.forEach(function(select, selectorIndex) {
    if (Array.prototype.slice.call(select.childNodes).some(function(n) {
      return n.value === values[selectorIndex];
    })) {
      select.value = values[selectorIndex];
    }
  });

      console.log("audioRateSelect=>"+audioRateSelect);
      var option = document.createElement('option');
      option.value = 48000;
      option.text = "Default sample Rate";
      audioRateSelect.appendChild(option);
      option = document.createElement('option');
      option.value = 8000;
      option.text = "8000";
      audioRateSelect.appendChild(option);

}

function getAllDevices()
{
    navigator.mediaDevices.enumerateDevices().then(gotDevices).catch(errorCallback);
}

function start()
{
    console.log("Start");
    try {
        window.AudioContext = window.AudioContext || window.webkitAudioContext;
        audioContext = new AudioContext();
    } catch(e) {
        alert('Web Audio API is not supported in this browser');
    }

    // Check if there is microphone input.
    try {
        navigator.getUserMedia = navigator.getUserMedia ||  navigator.webkitGetUserMedia || navigator.mozGetUserMedia ||  navigator.msGetUserMedia;
      var hasMicrophoneInput = (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);

    } catch(e) {
        alert("getUserMedia() is not supported in your browser");
    }

    myPCMProcessingNode = audioContext.createScriptProcessor(bufferSize, 1, 1);


    myPCMProcessingNode.onaudioprocess = function(e)
    {
        var input = e.inputBuffer.getChannelData(0);
        var outSampleRate =  inSampleRate;
        var isResampleNeeded = false;

        if (audioRateSelect.selectedIndex > 0)
            outSampleRate = audioRateSelect[audioRateSelect.selectedIndex].value;
        if (inSampleRate == outSampleRate) isResampleNeeded = false
        else isResampleNeeded = true;

        //console.log("Selected sampleRate="+outSampleRate + "Source samplerate="+inSampleRate+"resampleneeded=", isResampleNeeded);

        if (isResampleNeeded == true)
        {
            //var buffer = inputSample;
            var resampledBuffer = resamplerObj.resampler(input);
            var resamplerObj = new Resampler(inSampleRate, outSampleRate, 1, input.length, false);
            let Uint16Buf = new Uint16Array(resampledBuffer.length);

            for (let i=0;i<resampledBuffer.length;i++){

                let s = Math.max(-1, Math.min(1, resampledBuffer[i]));
                s = s < 0 ? s * 0x8000 : s * 0x7FFF;
                Uint16Buf[i] = s;
            }

            if(connected == true && WsConnection != null){
               WsConnection.send(Uint16Buf);
            }
        }
        else
        {
            let Uint16Buf = new Uint16Array(input.length);
            for (let i=0;i<input.length;i++){

                let s = Math.max(-1, Math.min(1, input[i]));
                s = s < 0 ? s * 0x8000 : s * 0x7FFF;
                Uint16Buf[i] = s;
            }

            if(connected == true && WsConnection != null ){
               WsConnection.send(Uint16Buf);
            }
        }
    }



    if (location.protocol != 'https:')
    {
        wsUri = "ws://" + window.location.hostname +":"+ UnsecurePort;
    }
    else
    {
        wsUri = "wss://" + window.location.hostname + ":"+ SecurePort;
    }

    console.log(wsUri);

    var audioSource = audioInputSelect[audioInputSelect.selectedIndex].value;
    var constraints = {
        audio: {deviceId: audioSource ? {exact: audioSource} : undefined}
      };


    navigator.getUserMedia(constraints, function(stream) {
        window.localStream = stream

        microphone = audioContext.createMediaStreamSource(stream);
        inSampleRate = audioContext.sampleRate;
        microphone.connect(myPCMProcessingNode);
        myPCMProcessingNode.connect(audioContext.destination);

        gainNode = audioContext.createGain();
        microphone.connect(gainNode);
        gainNode.connect(myPCMProcessingNode);
        document.getElementById('volume').onchange = function() {
                gainNode.gain.value = this.value; // Any number between 0 and 1.
                console.log("Volume="+this.value);
        };

    }, errorCallback);

    WsConnection = new WebSocket(wsUri);
    WsConnection.onmessage = handlePWM;
    WsConnection.onerror = wsError;
    WsConnection.onopen = wsOpen;
    WsConnection.onclose = WsClose;

    $("#mic").attr('src','mic-sel.png');
}



function stop()
{
    console.log("Stop");
    if(connected == true && WsConnection != null )
    {
        WsConnection.close();
    }
    connected = false;
    stopAudio();
    $("#mic").attr('src','mic.png');
    isStarted = false;

    // Don't know why, but in Chrome the second start audio is not working
    // So force reloading ...
    location.reload();

}

function startorstop()
{
    if (isStarted == true)
    {
        stop();
        isStarted = false;
    } else {
        start();
        isStarted = true;
    }

}
