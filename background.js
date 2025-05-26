const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');


canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
console.log(window.innerWidth);  // 창 너비 (스크롤바 제외)
console.log(window.innerHeight); // 창 높이
// Daylight sky color
const topcolor ={r : 0, g : 141, b : 218};
const seccolor = {r : 65,g : 201,b : 226 };
const thirdcolor = {r : 172,g : 226,b : 225 };  
const lastcolor = {r : 247,g : 238,b : 221 };

// Sunset sky color
const topcolmid ={r: 195 , g: 14, b:89 };
const seccolmid ={r: 232, g:37, b:97};
const thirdcolmid = {r:242 , g:174, b:102};
const lastcolmid ={r:232, g:231, b:171};

// Night sky color
const topcolend ={r:33,g:15,b:55};
const seccolend ={r:79,g:28,b:81};
const thirdcolend={r:165,g:91,b:75};
const lastcolend={r:220,g:160,b:109};

sliderval=document.getElementById("selector"); //slider 값 조회 변수
const moonimg = document.getElementById("moon"); // moon 이미지 값 조회 변수
const sunimg = document.getElementById("sun"); // sun 이미지 값 조회 변수
const maintext = document.getElementById("maintext"); // maintext 내용 집어넣기 위한 변수

let progress = 0;

// 값에 맞는 중간 색상을 계산
// t 는 0.01 단위.
function lerp(start, end, t) {
  return start + (end - start) * t;
}

// lerp 에서 계산된 r , g , b 값 반환한다.
function interpolateColor(color1, color2, t) {
  const r = Math.round(lerp(color1.r, color2.r, t));
  const g = Math.round(lerp(color1.g, color2.g, t));
  const b = Math.round(lerp(color1.b, color2.b, t));
  return `rgb(${r}, ${g}, ${b})`;
}

function daytosunsetanimate(slidervalue) {
  progress = slidervalue;
  drawBackground(topcolor,topcolmid,seccolor,seccolmid,thirdcolor,thirdcolmid,lastcolor,lastcolmid,progress*2);
}

function sunsettonightanimate(slidervalue) {
  progress = slidervalue-0.5;
  drawBackground(topcolmid,topcolend,seccolmid,seccolend,thirdcolmid,thirdcolend,lastcolmid,lastcolend,progress*2);
}

// 배경 색 채워넣기
function drawBackground(topstart1,topend1,topstart2,topend2,topstart3,topend3,topstart4,topend4,time) {
  const colorTop1 = interpolateColor(topstart1, topend1, time);
  const colorTop2 = interpolateColor(topstart2, topend2, time);
  const colorTop3 = interpolateColor(topstart3, topend3, time);
  const colorTop4 = interpolateColor(topstart4, topend4, time);
  

  const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
  gradient.addColorStop(0.5, colorTop1); 
  gradient.addColorStop(0.7, colorTop2);
  gradient.addColorStop(0.9, colorTop3); 
  gradient.addColorStop(1, colorTop4); 

  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

// 슬라이더 값이 바뀔 때마다 실행됩니다.
sliderval.addEventListener('input',() => {  
  const value = parseFloat(sliderval.value, 10);
    if (value <= 0.5) {
      daytosunsetanimate(sliderval.value);
    } 
    else {
      sunsettonightanimate(sliderval.value);
    }})

sliderval.oninput = function() {
  const alpha = parseFloat(this.value);

  // 달/해의 위치 및 투명도 조정
  moonimg.style.opacity = alpha;
  sunimg.style.opacity = 1 - alpha;
  moonimg.style.top = (150 - 100 * alpha) + 'px';
  sunimg.style.top = (90 + 100 * alpha) + 'px';

  // 상태 텍스트 변경
  // 텍스트 변경 전에 투명하게 만들기
  maintext.style.opacity = 0;

  // 조금 기다렸다가 텍스트 바꾸고 다시 보이게
  setTimeout(() => {
    if (alpha <= 0.25) {
      maintext.textContent = "Bright Morning Vibe";
    } else if (alpha <= 0.5) {
      maintext.textContent = "Calm Afternoon Vibe";
    } else if (alpha <= 0.75) {
      maintext.textContent = "Late Afternoon Vibe";
    } else {
      maintext.textContent = "Late Night Vibe";
    }

    maintext.style.opacity = 1;
  }, 300);
};
