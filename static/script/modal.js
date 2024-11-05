/**
 * Updates the country list based on the search input and sorting criteria.
 * @param {string} search The search query.
 * @param {string} criteria The sorting criteria.
 * @param {string} order The sorting order.
 */
function updateSorting() {
    const search = document.getElementById('search').value;
    const criteria = document.getElementById('criteria').value;
    const order = document.querySelector('input[name="sort_order"]:checked').value;
    sortCountries(search, criteria, order);
}

/**
 * Fetches the sorted list of countries from the server and updates the HTML.
 * @param {string} search The search query.
 * @param {string} criteria The sorting criteria.
 * @param {string} order The sorting order.
 */
function sortCountries(search, criteria, order) {
    fetch(`/sort?search=${search}&criteria=${criteria}&sort_order=${order}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('country-results');
            resultsDiv.innerHTML = '';
            data.forEach(country => {
                resultsDiv.innerHTML += `
                    <div class="country-card">
                        <h2 class="country-name">${country.Name}</h2>
                        <p class="country-population">Population: ${country.Population.toLocaleString()}</p>
                    </div>
                `;
            });
        })
        .catch(error => console.error('Error:', error));
}

// Initial call to sort the list
sortCountries('', 'Name', 'asc');
