const express = require('express');
const path = require('path');
const app = express();
const port = 8000;
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

    const pythonProcess = spawn('python', ['test.py', year, month, date, selectedCity, selectedModel]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python 에러: ${data}`);
    });

    // 에러 핸들링
    try {
        // 에러가 발생할 수 있는 코드 작성
    } catch (error) {
        console.error('에러 발생:', error);
    }

    res.sendStatus(200); // 성공 상태 코드를 클라이언트로 보냄
});

app.listen(port, () => {
  console.log(`서버가 http://localhost:${port}에서 실행 중입니다.`);
});
