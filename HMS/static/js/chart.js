const diagnosisChart = document.getElementById('diagnosisChart');

const calculateFontSize = function(context) {
    var width = context.chart.width;
    return Math.round(width / 50); // Adjust the divisor for desired responsiveness
  };
  
      
new Chart(diagnosisChart, {
  type: 'bar',
  data: {
    labels: ['Malaria', 'Pneumonia', 'Headache', 'Seizure', 'Diabetes'],
    datasets: [{
      label: 'Diagnosis',
      data: [12, 19, 3, 5, 2],
      backgroundColor: [
        'orange',
        'red',
        'pink',
        'purple',
        'green',
        'blue',
      ],
      borderWidth: 1
    }]
  },
  options: {
       scales: {
        y: {
            beginAtZero: true,
            ticks: {
              font: {
                size: calculateFontSize
              }
            }
          },
          x: {
            ticks: {
              font: {
                size: calculateFontSize
              }
            }
          }
        },
        plugins: {
            legend: {
              labels: {
                font: {
                  size: calculateFontSize
                }
              }
            }
          }
  }
});

document.addEventListener("DOMContentLoaded", function () {
    var vitalsChart = document.getElementById('vitalsChart').getContext('2d');
    const calculateFontSize = function(context) {
    var width = context.chart.width;
    var height = context.chart.height;
    console.log(height);
    return Math.round(width / 50); // Adjust the divisor for desired responsiveness
  };
    var vitalsChart = new Chart(vitalsChart, {
        type: 'line',
        data: {
            labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6'],
            datasets: [{
                label: 'Temperature',
                data: [36, 30.2, 37.8, 34.5, 39.3, 34],
                borderColor: 'green',
                backgroundColor: 'green',
                tension: 0.4
            }, {
                label: 'Systole',
                data: [120, 118, 122, 125, 119, 112],
                borderColor: 'blue',
                backgroundColor: 'blue',
                tension: 0.4
            }, {
                label: 'Diastole',
                data: [76, 76, 84, 87, 80, 72],
                borderColor: 'deepskyblue',
                backgroundColor: 'deepskyblue',
                tension: 0.4
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        font: {
                        size: calculateFontSize
                        }
                    }
                    },
                    x: {
                    ticks: {
                        font: {
                        size: calculateFontSize
                        }
                    }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                        font: {
                            size: calculateFontSize
                        }
                        }
                    }
                    }
        }
    });
});
