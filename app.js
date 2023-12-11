const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 8000; // 환경 변수에서 포트를 가져오거나 기본값을 사용
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const fs = require('fs'); // 파일 시스템 모듈을 추가합니다.

// JSON 데이터를 파싱하기 위한 미들웨어 등록
app.use(bodyParser.json());

// "Front" 디렉토리를 정적 파일로 서빙하기 위한 미들웨어를 등록합니다.
app.use(express.static(path.join(__dirname, 'Front')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'Front', 'index.html'));
});

app.post('/sendData', async (req, res) => {
  const { year, month, date, selectedCity, selectedModel } = req.body;
  console.log('Received data:', year, month, date, selectedCity, selectedModel);

  try {
      const data = await runPythonScript(year, month, date, selectedCity, selectedModel);
      res.json({ pythonData: data });
  } catch (error) {
      console.error('Python 에러:', error);
      res.status(500).json({ error: `Python 에러: ${error.message}` });
  }
});

function runPythonScript(year, month, date, selectedCity, selectedModel) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['Get.py', year, month, date, selectedCity, selectedModel]);

      pythonProcess.stdout.on('data', (data) => {
          resolve(data.toString().trim());
      });

      pythonProcess.stderr.on('data', (data) => {
          reject(new Error(data.toString()));
      });
  });
}

// 피드백을 받아서 파일에 저장하는 라우트
app.post('/submitFeedback', (req, res) => {
  const feedback = req.body.feedback; // 클라이언트에서 보낸 후기 내용
  const feedbackDate = new Date().toISOString(); // 현재 날짜와 시간

  // 파일에 작성할 문자열 생성
  const feedbackEntry = `날짜: ${feedbackDate}\n후기: ${feedback}\n\n`;

  // data.txt 파일에 후기 내용 추가하기
  fs.appendFile(path.join(__dirname, 'data.txt'), feedbackEntry, (err) => {
      if (err) {
          console.error('파일 작성 에러:', err);
          res.status(500).send('파일 작성 중 에러 발생'); // 클라이언트에 에러 응답
      } else {
          res.send('피드백이 성공적으로 제출되었습니다.'); // 클라이언트에 성공 응답
      }
  });
});

app.listen(port, () => {
  console.log(`서버가 http://localhost:${port}에서 실행 중입니다.`);
});
