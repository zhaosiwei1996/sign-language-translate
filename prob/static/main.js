// 创建WebSocket连接
const socket = io.connect('ws://localhost:5000');

// 视频流,画布
const srcvideo = document.getElementById('srcvideo');
const respimg = document.getElementById('respimg');
const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');
//打开摄像头
navigator.mediaDevices.getUserMedia({video: true})
    .then(function (stream) {
        const video = document.querySelector('video');
        srcvideo.srcObject = stream;
        setInterval(function () {
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            // 将视频流数据传输到服务端
            const imageData = canvas.toDataURL('image/webp');
            socket.emit('video_stream', imageData);
        }, 100);

        // 处理返回结果
        socket.on('hand_gesture', (base64Data) => {
            respimg.src = `data:image/webp;base64,${base64Data}`;
        });
    })
    .catch(function (error) {
        console.log('Error accessing the camera: ' + error);
    });
