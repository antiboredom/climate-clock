// http://countdownjs.org/demo.html
// https://github.com/albert-gonzalez/easytimer.js
// we need to test energy consumption on different methods
// we should make this a gif of some sort - something that's easy to embed without javascript
function remainingTime(deadline) {
  let now = new Date().getTime();
  let t = deadline - now;
  return {
    days: Math.floor(t / (1000 * 60 * 60 * 24)),
    hours: Math.floor((t % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
    minutes: Math.floor((t % (1000 * 60 * 60)) / (1000 * 60)),
    seconds: Math.floor((t % (1000 * 60)) / 1000),
  };
}

function startCountdown() {
  let deadline = new Date("Jan 5, 2020 15:37:25");
  setInterval(() => {
    let timeleft = countdown(
      deadline,
      new Date(),
      countdown.DAYS | countdown.HOURS | countdown.MINUTES | countdown.SECONDS
    );
    console.log(timeleft);
    let remaining = remainingTime(deadline.getTime());
    console.log(remaining);
  }, 1000);
  // let deadline = new Date("Jan 5, 2020 15:37:25").getTime();
  // setInterval(() => {
  //   let remaining = remainingTime(deadline);
  //   console.log(remaining);
  // }, 1000);
}

const app = new Vue({
  el: "#clock",
  data: {
    years: null,
    months: null,
    days: null,
    hours: null,
    minutes: null,
    seconds: null,
    co2Budget: 420000000000,
    tonsPerSecond: 1331,
    intervalTime: 100,
    fade: false,
    startdate: new Date("Jun10, 2018 00:00:00"),
    deadline: new Date("Jun10, 2028 00:00:00"),
  },
  created() {
    this.setRemaining();
    this.countdown();
    this.fadeOut();

    let now = (new Date()).getTime();
    let start = this.startdate.getTime();
    let seconds = Math.floor((now - start)/1000);
    this.co2Budget = this.co2Budget - seconds * this.tonsPerSecond;
  },
  filters: {
    pad(val, total) {
      if (!val) return "00";
      if (!total) total = 2;
      return val.toString().padStart(total, "0");
    },
  },
  methods: {
    setRemaining() {
      let timeleft = countdown(
        this.deadline,
        new Date(),
        countdown.YEARS |
          countdown.MONTHS |
          countdown.DAYS |
          countdown.HOURS |
          countdown.MINUTES |
          countdown.SECONDS
      );
      this.seconds = timeleft.seconds;
      this.minutes = timeleft.minutes;
      this.hours = timeleft.hours;
      this.days = timeleft.days;
      this.months = timeleft.months;
      this.years = timeleft.years;

      this.co2Budget -= Math.floor(
        this.tonsPerSecond * (this.intervalTime / 1000)
      );
    },
    countdown() {
      setInterval(() => {
        this.setRemaining();
      }, this.intervalTime);
    },
    fadeOut() {
      clearTimeout(this.fadeTimeout);
      this.fade = false;

      this.fadeTimeout = setTimeout(() => {
        this.fade = true;
      }, 10000)
    },
  },
});
