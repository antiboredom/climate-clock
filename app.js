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
    startdate: new Date("2018-01-01 00:00:00+01:00"),
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

    this.deadline = new Date((now + (this.co2Budget/this.tonsPerSecond)*1000))
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
