document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // предотвращаем перезагрузку страницы

    const videoInput = document.getElementById('videoInput');
    const videoFile = videoInput.files[0];

    if (videoFile) {
        const formData = new FormData();
        formData.append('video', videoFile);

        try {
            const response = await fetch('http://localhost:8000/upload-video/', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Error uploading video');
            }

            const result = await response.json();
            const csvUrl = result.csv_url;

            // Fetch the CSV file
            const csvResponse = await fetch(csvUrl);
            const csvData = await csvResponse.text();

            // Parse and display the CSV data
            displayCSV(csvData);
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('result').innerHTML = '<p>Failed to upload video. Try again later.</p>';
        }
    } else {
        alert('Please select a video file');
    }
});

/*obrabotchik dlya knopki poiska po id video*/
document.getElementById('checkIdButton').addEventListener('click', async () => {
    const videoId = document.getElementById('videoIdInput').value;

    if (videoId) {
        try {
            const response = await fetch(`http://localhost:8000/check-video-id/${videoId}/`);

            if (!response.ok) {
                throw new Error('Video ID does not exist');
            }

            const result = await response.json();
            // Предполагается, что сервер вернет информацию о видео
            document.getElementById('idResult').innerHTML = `
                <p>Video ID: ${result.id}</p>
                <p>Title: ${result.title}</p>
                <p>Description: ${result.description}</p>
            `;
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('idResult').innerHTML = '<p>Video ID does not exist.</p>';
        }
    } else {
        alert('Please enter a video ID');
    }
});


// Function to parse and display CSV as a table
function displayCSV(csv) {
    const rows = csv.split('\n').filter(row => row.trim() !== '');
    const table = document.createElement('table');
    table.classList.add('csv-table');

    // Loop through rows and add to table
    rows.forEach((row, index) => {
        const cols = row.split(',');

        const tr = document.createElement('tr');
        if (index === 0) {
            tr.classList.add('table-header');
        }

        cols.forEach(col => {
            const td = document.createElement(index === 0 ? 'th' : 'td');
            td.textContent = col.trim();
            tr.appendChild(td);
        });

        table.appendChild(tr);
    });

    // Append table to result div
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = ''; // Clear previous content
    resultDiv.appendChild(table);
}
