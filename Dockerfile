# 프로덕션 환경에서 사용할 도커 이미지를 지정합니다.
FROM node:14

# 앱 소스코드를 복사할 디렉토리를 지정합니다.
WORKDIR '/app'

# package.json 및 package-lock.json을 복사하여 종속성을 먼저 설치합니다.
COPY package.json .

RUN npm install

# 소스 코드를 현재 디렉토리로 복사합니다.
COPY . .


# Express 애플리케이션을 시작합니다.
CMD ["npm", "start"]

# 애플리케이션이 사용하는 포트를 외부에 노출합니다.
EXPOSE 8000
