function sortDataByTemperature() {
    
    var table = document.getElementById("data-table");
    var rows = Array.from(table.getElementsByTagName("tr"));

    rows.sort(function(a, b) {
        var aValue = parseFloat(a.cells[3].innerText);
        var bValue = parseFloat(b.cells[3].innerText);

        if (isNaN(aValue) || isNaN(bValue)) {
            return 0;
        }

        return aValue - bValue;
    });

    var tbody = table.querySelector("tbody");
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
}

function sortDataByLatitude() {
    var table = document.getElementById("data-table");
    var rows = Array.from(table.getElementsByTagName("tr"));

    rows.sort(function(a, b) {
        var aValue = parseFloat(a.cells[4].innerText);
        var bValue = parseFloat(b.cells[4].innerText);

        if (isNaN(aValue) || isNaN(bValue)) {
            return 0;
        }

        return aValue - bValue;
    });

    var tbody = table.querySelector("tbody");
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
}
// 






function sortDataByq1() {
    var table = document.getElementById("data-table");
    var rows = Array.from(table.getElementsByTagName("tr"));

    rows.sort(function(a, b) {
        var aValue = parseFloat(a.cells[6].innerText);
        var bValue = parseFloat(b.cells[6].innerText);

        if (isNaN(aValue) || isNaN(bValue)) {
            return 0;
        }

        return aValue - bValue;
    });

    var tbody = table.querySelector("tbody");
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
}
function sortDataByq2() {
    var table = document.getElementById("data-table");
    var rows = Array.from(table.getElementsByTagName("tr"));

    rows.sort(function(a, b) {
        var aValue = parseFloat(a.cells[7].innerText);
        var bValue = parseFloat(b.cells[7].innerText);

        if (isNaN(aValue) || isNaN(bValue)) {
            return 0;
        }

        return aValue - bValue;
    });

    var tbody = table.querySelector("tbody");
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
}
function sortDataByq3() {
    var table = document.getElementById("data-table");
    var rows = Array.from(table.getElementsByTagName("tr"));

    rows.sort(function(a, b) {
        var aValue = parseFloat(a.cells[8].innerText);
        var bValue = parseFloat(b.cells[8].innerText);

        if (isNaN(aValue) || isNaN(bValue)) {
            return 0;
        }

        return aValue - bValue;
    });

    var tbody = table.querySelector("tbody");
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
}
// 



function sortDataByLongitude() {
    var table = document.getElementById("data-table");
    var rows = Array.from(table.getElementsByTagName("tr"));

    rows.sort(function(a, b) {
        var aValue = parseFloat(a.cells[5].innerText);
        var bValue = parseFloat(b.cells[5].innerText);

        if (isNaN(aValue) || isNaN(bValue)) {
            return 0;
        }

        return aValue - bValue;
    });

    var tbody = table.querySelector("tbody");
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
}

function sortDataBySerialNumber() {
    var table = document.getElementById("data-table");
    var rows = Array.from(table.getElementsByTagName("tr"));

    rows.sort(function(a, b) {
        var aValue = parseInt(a.cells[0].innerText);
        var bValue = parseInt(b.cells[0].innerText);

        if (isNaN(aValue) || isNaN(bValue)) {
            return 0;
        }

        return aValue - bValue;
    });

    var tbody = table.querySelector("tbody");
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
}
function deleteData() {
    if (confirm("Are you sure you want to delete all data?\nIf you want to cancel and save data click cancel and save.")) {

        fetch("/delete", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ database: "gps_data", collection: "gps_messages" })
        })
        .then(response => {
            if (response.ok) {
                alert("All data deleted successfully!");
                location.reload(); 
            } else {
                throw new Error("Failed to delete data. Please try again.");
            }
        })
        .catch(error => {
            alert(error.message);
        });
    }
}
function opengraphs(){
    const url = '/graphs';
    window.location.href = url;
}

function saveDataAsCSV() {
    
    var table = document.getElementById('data-table');
    var csv='';
     csv+= 'Sr No.,Date, Robot ID ,Data ID,Topic,Temperature,Latitude,Longitude,Quality1,Quality2,Quality3,Time';
    csv += '\n';
    for (var i = 1; i < table.rows.length; i++) {
        var row = table.rows[i];

    
        for (var j = 0; j < row.cells.length; j++) {
            var cell = row.cells[j];
            csv += cell.innerText + ',';
        }

    
        csv += '\n';
    }

    
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv));
    element.setAttribute('download', 'gps_data.csv');

    
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}






document.addEventListener('DOMContentLoaded', () => {
    const filterForm = document.getElementById('filter-form');
    const resetButton = document.getElementById('reset-button');

    filterForm.addEventListener('submit', (event) => {
        event.preventDefault();
        applyFilter();
    });

    resetButton.addEventListener('click', (event) => {
        event.preventDefault();
        resetFilter();
    });

    function applyFilter() {
        const robotIdInput = document.getElementById('robot-id-input');
        const robotIds = robotIdInput.value.trim();
        const url = robotIds ? `${robotIds}` : '/';
        window.location.href = url;
    }

    function resetFilter() {
        const url = '/';
        window.location.href = url;
    }

});