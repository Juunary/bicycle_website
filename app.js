const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 8000; // 환경 변수에서 포트를 가져오거나 기본값을 사용
const bodyParser = require('body-parser');
const { spawn } = require('child_process');


// JSON 데이터를 파싱하기 위한 미들웨어 등록
app.use(bodyParser.json());

// "Front" 디렉토리를 정적 파일로 서빙하기 위한 미들웨어를 등록합니다.
app.use(express.static(path.join(__dirname, 'Front')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'Front', 'index.html'));
});

app.post('/sendData', (req, res) => {
    // 클라이언트에서 보낸 데이터는 req.body에서 사용 가능
    const { year, month, date, selectedCity, selectedModel } = req.body;
    
    // 데이터를 터미널에 출력
    console.log('Received data:', year, month, date, selectedCity, selectedModel);

    const pythonProcess = spawn('python', ['Get.py', year, month, date, selectedCity, selectedModel]);
    
    

    pythonProcess.stdout.on('data', (data) => {
        const receivedDataFromPython = data.toString().trim();
        console.log(`receivedDataFromPython: ${receivedDataFromPython}`);

        // 성공 응답과 함께 데이터를 클라이언트로 전송
        res.json({ pythonData: receivedDataFromPython });
    });


    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python 에러: ${data}`);
        
        // 클라이언트로 에러 메시지 전송
        res.status(500).json({ error: `Python 에러: ${data.toString()}` });
    });

    // NOTE: 여기에 res.sendStatus(200); 라인은 삭제해야 합니다.
});



app.listen(port, () => {
  console.log(`서버가 http://localhost:${port}에서 실행 중입니다.`);
});
