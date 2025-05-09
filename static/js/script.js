document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('stressForm');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const params = new URLSearchParams();
        for (const [key, value] of formData.entries()) {
            params.append(key, value);
        }

        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: params
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('result').innerHTML = `<p>${data.error}</p>`;
            } else {
                document.getElementById('prediction').innerText = `Predicted Stress Level: ${data.prediction}`;

                const meterFill = document.getElementById('meterFill');
                if (data.prediction === 'Low stress') {
                    meterFill.style.width = '33%';
                    meterFill.style.backgroundColor = '#4CAF50';
                } else if (data.prediction === 'Medium stress') {
                    meterFill.style.width = '66%';
                    meterFill.style.backgroundColor = '#FFC107';
                } else if (data.prediction === 'High stress') {
                    meterFill.style.width = '100%';
                    meterFill.style.backgroundColor = '#F44336';
                }

                const remediesList = document.getElementById('remedies');
                remediesList.innerHTML = '';
                data.remedies.forEach(remedy => {
                    const li = document.createElement('li');
                    li.innerText = remedy;
                    remediesList.appendChild(li);
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
