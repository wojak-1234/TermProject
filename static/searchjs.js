   document.addEventListener('DOMContentLoaded', function() {
        const searchSongBtn = document.getElementById('search-song-btn');
        const songQueryInput = document.getElementById('song-query-input');
        const songResultsDisplay = document.getElementById('song-results-display');

        if (searchSongBtn) {
            searchSongBtn.addEventListener('click', async function() {
                const query = songQueryInput.value.trim();
                if (!query) {
                    songResultsDisplay.innerHTML = '<p style="color: red;">Please input valid keyword!</p>';
                    return;
                }

                songResultsDisplay.innerHTML = '<p style="color: rgba(255, 255, 255, 0.7);">Searching...</p>';

                try {
                    const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);

                    if (!response.ok) {
                        const errorText = await response.text();
                        throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
                    }

                    const data = await response.json();
                    displaySongInfo(data);

                } catch (error) {
                    console.error("곡 검색 중 오류 발생:", error);
                    songResultsDisplay.innerHTML = `<p style="color: red;">곡 정보를 가져오지 못했습니다. 오류: ${error.message}</p>`;
                }
            });
        }

function displaySongInfo(data) {
    const songResultsDisplay = document.getElementById('song-results-display');
    songResultsDisplay.innerHTML = ''; 

    if (data.error) {
        songResultsDisplay.innerHTML = `<p style="color: red; font-weight: bold;">${data.error}</p>`;
        return;
    }

    if (!data.track_name) {
        songResultsDisplay.innerHTML = '<p style="color: rgba(255, 255, 255, 0.7);">There are no results.</p>';
        return;
    }

    const resultCard = document.createElement('div');
    resultCard.className = 'result-card';

    if (data.album_image_url) {
        const albumImage = document.createElement('img');
        albumImage.src = data.album_image_url;
        albumImage.alt = `${data.track_name} Album cover`;
        albumImage.className = 'album-image';
        resultCard.appendChild(albumImage);
    }

    const infoDiv = document.createElement('div');
    infoDiv.className = 'info-div';

    infoDiv.innerHTML += `<h3>${data.track_name}</h3>`;
    infoDiv.innerHTML += `<p><strong>Artist:</strong> ${data.artist_name}</p>`;

    if (data.popularity !== undefined) {
        infoDiv.innerHTML += `<p><strong>Popularity:</strong> ${data.popularity} / 100</p>`;
    } else {
        infoDiv.innerHTML += `<p><strong>Popularity:</strong> No info </p>`;
    }

    resultCard.appendChild(infoDiv);
    songResultsDisplay.appendChild(resultCard);
}});