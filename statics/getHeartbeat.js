const fetchData = (did) => {
    return fetch(`/api/heartbeat/device/${did}`)
        .then(res => {
            if (res.status !== 200) {
                console.log(res);
            }
            return res;
        })
        .then(res => res.json())
        .catch(error => console.log(error));
}

const plotly = (first, second) => {
    const layout = {
        title: "Heartrate"
    }
    return Plotly.newPlot("graph-container", [{x: first, y: second}], layout)
}

const unpack = (arr, key) => arr.map((a) => a.values[key])
fetchData("mock-device").then(
    (res) => {
        plotly(unpack(res.records, "_time"), unpack(res.records, "_value"));
    }
)