$(function() {
  $('.chart').easyPieChart({
    size: 180,
    easing: 'easeOutElastic',
    barColor: "#36e617",
    scaleLength: 5,
    lineWidth: 15,
    trackColor: "#525151",
    lineCap: "circle",
    animate: {duration: 2000, enabled : true},
    onStep: function (from, to, percent) {
        $(this.el).find('.percent').text(Math.round(percent));
    }
  });
});
