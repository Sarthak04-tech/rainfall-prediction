document.addEventListener('DOMContentLoaded', async () => {
    const form = document.getElementById('predictionForm');
    const submitBtn = document.getElementById('submitBtn');
    const spinner = document.getElementById('spinner');
    const btnText = document.querySelector('.btn-text');
    const resultContainer = document.getElementById('resultContainer');
    const predictionResult = document.getElementById('predictionResult');
    const categoryBadge = document.getElementById('categoryBadge');
    const errorContainer = document.getElementById('errorContainer');
    const errorMessage = document.getElementById('errorMessage');
    const autoFillBtn = document.getElementById('autoFillBtn');
    
    let historicalData = [];
    let rainfallChart = null;

    // Fetch historical averages on load
    try {
        const statsResponse = await fetch('/stats');
        if (statsResponse.ok) {
            const stats = await statsResponse.json();
            historicalData = Object.values(stats);
            initChart();
        }
    } catch (e) {
        console.error("Failed to load historical stats", e);
    }

    function initChart() {
        const ctx = document.getElementById('rainfallChart').getContext('2d');
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        
        rainfallChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: months,
                datasets: [
                    {
                        label: 'Historical Average',
                        data: historicalData,
                        borderColor: 'rgba(148, 163, 184, 0.5)',
                        borderDash: [5, 5],
                        fill: false,
                        tension: 0.4
                    },
                    {
                        label: 'Your Input',
                        data: Array(12).fill(0),
                        backgroundColor: 'rgba(79, 70, 229, 0.2)',
                        borderColor: '#4F46E5',
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        labels: { color: '#94a3b8', font: { family: 'Outfit' } }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(148, 163, 184, 0.1)' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8' }
                    }
                }
            }
        });
    }

    function updateChartData() {
        if (!rainfallChart) return;
        const currentData = [
            parseFloat(document.getElementById('JAN').value) || 0,
            parseFloat(document.getElementById('FEB').value) || 0,
            parseFloat(document.getElementById('MAR').value) || 0,
            parseFloat(document.getElementById('APR').value) || 0,
            parseFloat(document.getElementById('MAY').value) || 0,
            parseFloat(document.getElementById('JUN').value) || 0,
            parseFloat(document.getElementById('JUL').value) || 0,
            parseFloat(document.getElementById('AUG').value) || 0,
            parseFloat(document.getElementById('SEP').value) || 0,
            parseFloat(document.getElementById('OCT').value) || 0,
            parseFloat(document.getElementById('NOV').value) || 0,
            parseFloat(document.getElementById('DEC').value) || 0
        ];
        rainfallChart.data.datasets[1].data = currentData;
        rainfallChart.update();
    }

    // Auto-fill mock data
    autoFillBtn.addEventListener('click', () => {
        document.getElementById('YEAR').value = new Date().getFullYear();
        const mockData = [15.2, 22.4, 45.1, 78.5, 120.3, 350.6, 480.2, 410.5, 290.7, 130.4, 35.6, 12.8];
        const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
        
        months.forEach((month, index) => {
            document.getElementById(month).value = mockData[index];
        });
        updateChartData();
    });

    // Reset button functionality
    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            form.reset();
            resultContainer.classList.remove('show');
            errorContainer.classList.remove('show');
            updateChartData();
        });
    }

    // Listen for input changes to update chart in real-time
    form.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', updateChartData);
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        resultContainer.classList.remove('show');
        errorContainer.classList.remove('show');
        btnText.textContent = "Analyzing Patterns...";
        spinner.style.display = "block";
        submitBtn.disabled = true;

        const formData = new FormData(form);
        const data = {};
        for(let [key, value] of formData.entries()) {
            data[key] = parseFloat(value);
        }

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok) {
                animateValue(predictionResult, 0, result.prediction, 1500);
                
                // Update badge
                categoryBadge.textContent = result.category;
                categoryBadge.className = 'category-badge ' + result.category.toLowerCase();
                
                resultContainer.classList.add('show');
                updateChartData(); // Final sync
            } else {
                errorMessage.textContent = result.error || "An error occurred during prediction.";
                errorContainer.classList.add('show');
            }

        } catch (error) {
            console.error('Prediction Error:', error);
            errorMessage.textContent = "Unable to connect to the prediction server.";
            errorContainer.classList.add('show');
        } finally {
            btnText.textContent = "Predict Annual Rainfall";
            spinner.style.display = "none";
            submitBtn.disabled = false;
        }
    });
});

function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const easeOut = 1 - Math.pow(1 - progress, 4);
        const current = start + easeOut * (end - start);
        obj.innerHTML = current.toFixed(2);
        if (progress < 1) window.requestAnimationFrame(step);
    };
    window.requestAnimationFrame(step);
}
