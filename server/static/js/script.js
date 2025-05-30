document.addEventListener('DOMContentLoaded', function () {
    const searchInputElement = document.getElementById('searchbar');
    if (searchInputElement) {
        searchInputElement.placeholder =
            'Search by material, color, stone and collection';
    }
});
