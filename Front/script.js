// 클릭한 날짜를 표시하는 함수
function showSelectedDate(cell) {
    // 모든 날짜의 클래스를 초기화
    const cells = document.querySelectorAll('.calendar table td');
    cells.forEach((c) => {
        c.classList.remove('selected');
    });

    // 클릭한 날짜에 클래스 추가
    cell.classList.add('selected');
}

// 날짜 클릭 이벤트 처리
const cells = document.querySelectorAll('.calendar table td');
cells.forEach((cell) => {
    cell.addEventListener('click', function () {
        showSelectedDate(cell);
        const year = new Date().getFullYear();
        const month = new Date().getMonth();
        const date = cell.textContent;
        updateSelectedDateAlert(year, month, date);
    });
});

// 선택된 날짜를 저장하는 변수
let selectedCell = null;

// 이전 달과 다음 달 버튼에 대한 이벤트 핸들러 추가
document.getElementById('prevMonth').addEventListener('click', function () {
    // 이전 달을 선택할 때 선택한 날짜 초기화
    selectedCell = null;

    const title = document.getElementById('calendarTitle').textContent;
    const currentYear = parseInt(title.split("년")[0]);
    const currentMonth = parseInt(title.split("년")[1].split("월")[0]);

    if (currentMonth === 1) {
        createCalendar(currentYear - 1, 11);
    } else {
        createCalendar(currentYear, currentMonth - 2);
    }
});

document.getElementById('nextMonth').addEventListener('click', function () {
    // 다음 달을 선택할 때 선택한 날짜 초기화
    selectedCell = null;

    const title = document.getElementById('calendarTitle').textContent;
    const currentYear = parseInt(title.split("년")[0]);
    const currentMonth = parseInt(title.split("년")[1].split("월")[0]);

    if (currentMonth === 12) {
        createCalendar(currentYear + 1, 0);
    } else {
        createCalendar(currentYear, currentMonth);
    }
});

// 초기화면에 현재 달력 생성
const currentDate = new Date();
createCalendar(currentDate.getFullYear(), currentDate.getMonth());

function bindCellClickEvent() {
    const cells = document.querySelectorAll('.calendar table td');
    cells.forEach((cell) => {
        cell.addEventListener('click', function () {
            cells.forEach((c) => c.classList.remove('selected'));
            cell.classList.add('selected');
            selectedDateInfo = {
                year: year,
                month: month + 1,
                date: cell.textContent
            };
        });
    });
}

let currentYear = new Date().getFullYear();
let currentMonth = new Date().getMonth();

function createCalendar(year, month) {
    const calendarBody = document.querySelector('.calendar table tbody');
    calendarBody.innerHTML = '';

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    document.getElementById('calendarTitle').textContent = `${year}년 ${month + 1}월`;

    let date = 1;
    for (let i = 0; i < 6; i++) {
        const row = document.createElement('tr');

        for (let j = 0; j < 7; j++) {
            const cell = document.createElement('td');
            if (i === 0 && j < firstDay || date > daysInMonth) {
                cell.textContent = '';
            } else {
                cell.textContent = date++;
            }
            row.appendChild(cell);
        }
        calendarBody.appendChild(row);
    }

    const cells = document.querySelectorAll('.calendar table td');
    cells.forEach((cell) => {
        cell.addEventListener('click', function () {
            cells.forEach((c) => c.classList.remove('selected'));
            cell.classList.add('selected');
            selectedDateInfo = {
                year: year,
                month: month + 1,
                date: cell.textContent
            };
        });
    });
}


document.getElementById('showResult').addEventListener('click', function() {
    if (selectedDateInfo) {
        const { year, month, date } = selectedDateInfo;

        const citySelectBox = document.getElementById('cityListBox');
        const selectedCity = citySelectBox.options[citySelectBox.selectedIndex].text;

        const modelSelectBox = document.getElementById('modelListBox');
        const selectedModel = modelSelectBox.options[modelSelectBox.selectedIndex].text;
        updateSelectedDateAlert(year, month, date, selectedCity, selectedModel);
        // 데이터를 객체로 만들기
        const data = {
            year: year,
            month: month,
            date: date,
            selectedCity: selectedCity,
            selectedModel: selectedModel
        };

        // 서버로 데이터를 POST 요청으로 보내기
        fetch('/sendData', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.status === 200) {
                alert('데이터가 성공적으로 전송되었습니다.');
            } else {
                alert('데이터 전송에 실패했습니다.');
            }
        });
    } else {
        alert('날짜를 선택해주세요.');
    }
});

function updateSelectedDateAlert(year, month, date, city, model) {
    const selectedDateAlert = document.getElementById('selectedDateAlert');
    selectedDateAlert.textContent = `${year}년 ${month}월 ${date}일 / ${city} / ${model}을 선택했습니다.`;
}

document.getElementById('prevMonth').addEventListener('click', function () {
    if (--currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    createCalendar(currentYear, currentMonth);
});

document.getElementById('nextMonth').addEventListener('click', function () {
    if (++currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    createCalendar(currentYear, currentMonth);
});

// 페이지 로드 시 현재 달력을 생성합니다.
createCalendar(currentYear, currentMonth);