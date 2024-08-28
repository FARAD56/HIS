document.addEventListener("DOMContentLoaded", function () {
  fetch('http://127.0.0.1:8000/patients/chart/')
  .then(response => response.json())
  .then(data => {
      // Diagnosis chart data
      const diagnosisData = data.diagnosis;
      const diagnosisChart = document.getElementById('diagnosisChart').getContext('2d');
      new Chart(diagnosisChart, {
          type: 'bar',
          data: {
              labels: diagnosisData.labels,
              datasets: [{
                  label: 'Diagnosis',
                  data: diagnosisData.data,
                  backgroundColor: ['orange', 'red', 'pink', 'purple', 'green', 'blue'],
                  borderWidth: 1
              }]
          },
          options: {
              scales: {
                  y: {
                      beginAtZero: true,
                      ticks: {
                          font: { size: 12 } // Replace calculateFontSize with a fixed value or a function
                      }
                  },
                  x: {
                      ticks: {
                          font: { size: 12 }
                      }
                  }
              },
              plugins: {
                  legend: {
                      labels: {
                          font: { size: 12 }
                      }
                  }
              }
          }
      });

      // Vitals chart data
      const vitalsData = data.vitals;
      const vitalsChartCtx = document.getElementById('vitalsChart').getContext('2d');
      new Chart(vitalsChartCtx, {
          type: 'line',
          data: {
              labels: vitalsData.labels,
              datasets: [
                  {
                      label: 'Temperature',
                      data: vitalsData.temperature,
                      borderColor: 'green',
                      backgroundColor: 'green',
                      tension: 0.4
                  },
                  {
                      label: 'Systole',
                      data: vitalsData.systole,
                      borderColor: 'blue',
                      backgroundColor: 'blue',
                      tension: 0.4
                  },
                  {
                      label: 'Diastole',
                      data: vitalsData.diastole,
                      borderColor: 'deepskyblue',
                      backgroundColor: 'deepskyblue',
                      tension: 0.4
                  }
              ]
          },
          options: {
              scales: {
                  y: {
                      beginAtZero: true,
                      ticks: {
                          font: { size: 12 }
                      }
                  },
                  x: {
                      ticks: {
                          font: { size: 12 }
                      }
                  }
              },
              plugins: {
                  legend: {
                      labels: {
                          font: { size: 12 }
                      }
                  }
              }
          }
      });
  })
  .catch(error => console.error('Error fetching chart data:', error));
});
