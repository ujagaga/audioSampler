// set up basic variables for app

var startstop = document.querySelector('#startstop');
const canvas = document.querySelector('.visualizer');
const mainSection = document.querySelector('.main-controls');
const msgWindow = document.querySelector('#ui-msg');
var progressBar = document.querySelector('#myBar');
var busy = new busy_indicator(document.getElementById("busybox"),  document.querySelector("#busybox div"));
const promptMsg = [0, 9, 2, 1, 4, 3, 7, 7, 4, 2, 1, 1, 5, 5, 4, 8, 6, 7, 9, 2, 3, 6, 8, 8, 5, 6, 9, 0, 0, 3];
var promptTimer;
var mediaRecorder;
var userName;
var sample;
var recordStarted = false;


// visualiser setup - create web audio api context and canvas
let audioCtx;
const canvasCtx = canvas.getContext("2d");
var i = 0;
var j = 0;

function send_data(){
    busy.show();

    var form = new FormData();
    form.append('file', sample, userName);
    //Chrome inspector shows that the post data includes a file and a title.
    $.ajax({
      type: 'POST',
      url: '/collect',
      data: form,
      cache: false,
      processData: false,
      contentType: false,
    }).done(function(data) {
          busy.hide();
          alert(data);
    });
}

function numberPrompt(){
    if(i >= promptMsg.length){
        stopRecording();
        progressBar.style.width = "100%";
        userName = prompt('Mogu li da pošaljem audio?','Molim Vas, upišite Vaše ime.');

        if(userName && sample){
            send_data();
        }
    } else{
        if((j % 3) == 0){
            msgWindow.innerHTML = "<p>" + promptMsg[i] + "</p>";
            window.scrollTo(0,document.body.scrollHeight);
            i++;
        }

        if(((j + 1) % 3) == 0){
            msgWindow.innerHTML = "<p>&nbsp</p>";
        }

        var percent = (33 * j) / promptMsg.length;
        progressBar.style.width = percent + "%";
    }
    j++;
}

function startPrompt(){
    i = 0;
    j = 0;
    userName = null;
    numberPrompt();
    promptTimer = setInterval(function(){ numberPrompt(); }, 1000);
}

function stopRecording(){
    mediaRecorder.stop();
    clearInterval(promptTimer);
    console.log("recorder stopped");
    recordStarted = false;
    startstop.textContent = "Start";
}

//main block for doing the audio recording

if (navigator.mediaDevices.getUserMedia) {
    console.log('getUserMedia supported.');

    const constraints = { audio: true };

    let onSuccess = function(stream) {
        mediaRecorder = new MediaRecorder(stream);

        visualize(stream);

        startstop.onclick = function() {
            if(recordStarted){
                stopRecording();
            }else{
                sample = null;
                mediaRecorder.start();
                console.log("recorder started");
                recordStarted = true;
                startstop.textContent = "Stop";
                startPrompt();
            }
        }
        mediaRecorder.ondataavailable = function(e) {
            sample = e.data;

            if(userName && sample){
                send_data();
            }
        }
    }

    let onError = function(err) {
        console.log('The following error occurred: ' + err);
    }

    navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);

} else {
    console.log('getUserMedia not supported on your browser!');
    alert("Vaš internet pretraživač ne podržava snimanje");
}

function visualize(stream) {
  if(!audioCtx) {
    audioCtx = new AudioContext();
  }

  const source = audioCtx.createMediaStreamSource(stream);

  const analyser = audioCtx.createAnalyser();
  analyser.fftSize = 2048;
  const bufferLength = analyser.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);

  source.connect(analyser);
  draw()

  function draw() {
    const WIDTH = canvas.width
    const HEIGHT = canvas.height;

    requestAnimationFrame(draw);

    analyser.getByteTimeDomainData(dataArray);

    canvasCtx.fillStyle = 'rgb(200, 200, 200)';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

    canvasCtx.lineWidth = 2;
    canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

    canvasCtx.beginPath();

    let sliceWidth = WIDTH * 1.0 / bufferLength;
    let x = 0;


    for(let i = 0; i < bufferLength; i++) {

      let v = dataArray[i] / 128.0;
      let y = v * HEIGHT/2;

      if(i === 0) {
        canvasCtx.moveTo(x, y);
      } else {
        canvasCtx.lineTo(x, y);
      }

      x += sliceWidth;
    }

    canvasCtx.lineTo(canvas.width, canvas.height/2);
    canvasCtx.stroke();

  }
}

window.onresize = function() {
  canvas.width = mainSection.offsetWidth;
}

window.onresize();

$(document).ready(function(){
    startstop.textContent = "Start";
});


