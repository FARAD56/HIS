document.addEventListener("DOMContentLoaded", function () {
    fetch('http://127.0.0.1:8000/chart/')
      .then(response => response.json())
      .then(data => {
        // Diagnosis chart data
        const diagnosisData = data.diagnosis;
        const diagnosisChartCtx = document.getElementById('diagnosisChart').getContext('2d');
        new Chart(diagnosisChartCtx, {
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
  
        // Gender chart data
        const genderAgeData = data.gender_age;
        const genderAgeChartCtx = document.getElementById('genderAgeChart').getContext('2d');
        new Chart(genderAgeChartCtx, {
          type: 'bar',
          data: {
            labels: genderAgeData.labels,
            datasets: [{
              label: 'Gender & Age Group',
              data: genderAgeData.data,
              backgroundColor: ['blue', 'pink', 'yellow'], // Colors for Men, Women, Children
              borderWidth: 1
            }]
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
  