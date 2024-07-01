HOST = "localhost";
PORT = 8080;

const scoreList = document.querySelector(".score-list");

class BalloonScore {
    constructor(id) {
        this.id = id;
        this.htmlElement = document.querySelector(`#balloon${id}`);
        this.points = 0;
        this.rank = id;
    }
}

let daily_record = 0;
let season_record = 0;

// instantiate the 12 score objects
let scoreObjects = [];
for (let id=1; id<13; id++) {
    let score = new BalloonScore(id);
    scoreObjects.push(score);
};

// websocket to receive score data
const socket = new WebSocket(`ws://${HOST}:${PORT}`);

socket.onopen = () => {
    console.log('WebSocket connection established.');
};

socket.onmessage = event => {
    console.log("\nNEW DATA")
    // get list of points for each balloon and assign it to corresponding Score Object
    let score_data = JSON.parse(event.data);
    for (let i=0; i<12; i++) {
        scoreObjects[i].points = score_data[i]
    }
    // sort and rank the objects
    let scoreObjectsSorted = scoreObjects.slice().sort((score_a, score_b) => score_a.points - score_b.points);
    for (let i=0; i<12; i++) {
        scoreObjectsSorted[i].rank = i+1;
    }
    for (let i=0; i<12; i++) {
        console.log(`ID: ${scoreObjectsSorted[i].id}`);
        console.log(`Place: ${scoreObjectsSorted[i].rank}`);
        console.log(`Points: ${scoreObjectsSorted[i].points}`);
    }
    
    // update frontend
    for (let i=0; i<12; i++) {
        // update position
        let scoreObject = scoreObjectsSorted[i];
        scoreObjectElemet.htmlElement.removeAttribute("id");
        scoreObjectElemet.htmlElement.setAttribute("id", `balloon${i+1}`);

        // update viewed score 
        let scoreDiv = document.querySelector(`#score${scoreObject.id}`);
        scoreDiv.innerHTML = scoreObject.points;

        // updated highscore-records
        daily_record = score_data[12];
        season_record = score_data[13];
        document.querySelector("#tagesrekord").innerHTML = daily_record;
        document.querySelector("#jahresrekord").innerHTML = season_record;
    }
};

socket.onerror = error => {
    console.error('WebSocket error:', error);
};

socket.onclose = event => {
    console.log('WebSocket connection closed.');
};



// just for testing ranking mechanism
// invert the ranking by clicking on 1st element
let testElement = document.querySelector("#balloon1");
testElement.addEventListener("click", () => {    
    for (let i=0; i<12; i++) {
        let balloonScore = scoreObjects[i];
        balloonScore.htmlElement.removeAttribute("id");
        balloonScore.htmlElement.setAttribute("id", `balloon${12-i}`);

        let scoreDiv = document.querySelector(`#score${balloonScore.id}`);
        scoreDiv.innerHTML = i+1;
    }
});
