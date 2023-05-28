import "../css/home.css"
import "../image/1.png"
import "../image/2.png"
import "../image/3.png"
import "../image/12.png"
import "../image/accessory_logo.png"
import "../image/coffee_logo.png"
import "../image/chocolate_logo.png"
import "../image/espresso_maker_logo.png"
import "../image/banner1.png"
import "../image/banner2.png"

// (function offer_counter() {
//     const second = 1000,
//         minute = second * 60,
//         hour = minute * 60,
//         day = hour * 24;
//     const birthday = '09/03/2024';
//     const countDown = new Date(birthday).getTime(),
//         x = setInterval(function() {
//
//             const now = new Date().getTime(),
//                 distance = countDown - now;
//
//         document.getElementById("days").innerText = Math.floor(distance / (day)),
//         document.getElementById("hours").innerText = Math.floor((distance % (day)) / (hour)),
//         document.getElementById("minutes").innerText = Math.floor((distance % (hour)) / (minute)),
//         document.getElementById("seconds").innerText = Math.floor((distance % (minute)) / second);
//
//         //do something later when date is reached
//         if (distance < 0) {
//             document.getElementById("headline").innerText = "It's my birthday!";
//             document.getElementById("countdown").style.display = "none";
//             document.getElementById("content").style.display = "block";
//             clearInterval(x);
//         }
//         //seconds
//       }, 0)
//   }());

// function offer_timer(date) {
//     const second = 1000,
//         minute = second * 60,
//         hour = minute * 60,
//         day = hour * 24;
//
//     const countDown = new Date(date).getTime();
//     const now = Date.now();
//     const distance = countDown - now;
//
//     let days = Math.floor(distance / (day));
//     let hours = Math.floor((distance % (day)) / (hour));
//     let minutes = Math.floor((distance % (hour)) / (minute));
//     let seconds = Math.floor((distance % (minute)) / second);
//     const addZero = num => {
//         if(num < 10) { return '0' + num }
//         return num;
//     }
//     $('#day').text(days);
//     $('#hour').text(addZero(hours));
//     $('#minute').text(addZero(minutes));
//     $('#second').text(addZero(seconds));
// }
// setInterval(offer_timer, offer_deadline, 1000);
