HOST = "localhost";
PORT = 8080;

const scoreList = document.querySelector("#score-list");

class Score {
    constructor(id) {
        this.id = id;
        this.htmlElement = document.querySelector(`#s${id}`);
        this.points = 0;
        this.place = id+1;
    }
}

/* instantiate the 12 score objects */
let scoreObjects = [];
for (let i=0; i<12; i++) {
    let score = new Score(i);
    scoreObjects.push(score);
};

/* define the 12 pixel positions */
let pxPositions = []
for (let i=0; i<12; i++) {
    let rect = scoreObjects[i].htmlElement.getBoundingClientRect();
    pxPositions.push(rect.top);
}


/* websocket to receive score data */
const socket = new WebSocket(`ws://${HOST}:${PORT}`);

socket.onopen = () => {
    console.log('WebSocket connection established.');
};

socket.onmessage = event => {
    console.log("\nNEW DATA")
    /* get list of points for each balloon and assign it to corresponding Score Object */
    let score_data = JSON.parse(event.data);
    for (let i=0; i<12; i++) {
        scoreObjects[i].points = score_data[i]
    }
    /* sort and rank the objects */
    let scoreObjectsSorted = scoreObjects.slice().sort((score_a, score_b) => score_a.points - score_b.points);
    for (let i=0; i<12; i++) {
        scoreObjectsSorted[i].place = i + 1;
    }
    for (let i=0; i<12; i++) {
        console.log(`ID: ${scoreObjectsSorted[i].id}`);
        console.log(`Place: ${scoreObjectsSorted[i].place}`);
        console.log(`Points: ${scoreObjectsSorted[i].points}`);
    }
    
    /* change positions depending on points */
    scoreList.innerHTML = ""
    for (let i=0; i<12; i++) {
        scoreList.appendChild(scoreObjectsSorted[i].htmlElement);
    }

};

socket.onerror = error => {
    console.error('WebSocket error:', error);
};

socket.onclose = event => {
    console.log('WebSocket connection closed.');
};



/* just for testing generate a random order by klicking on a list item
let testElement = document.querySelector("#s0");
testElement.addEventListener("click", () => {
    let randRanks = []
    for (let i=0; i<12; i++) {
        randPos = Math.floor(Math.random() * (i + 1));
        randRanks.splice(randPos, 0, i);
    }
    scoreList.innerHTML = ""
    for (let i=0; i<12; i++) {
        randId = randRanks[i]
        scoreList.appendChild(scoreObjects[randId].htmlElement);
    }    
})
*/

/* testing single element (S3) */
let testElement = document.querySelector("#s3");
testElement.addEventListener("click", () => {
    scoreList.innerHTML = ""
    scoreList.appendChild(scoreObjects[3].htmlElement);
    for (let i=0; i<12; i++) {
        if (i !== 3) {
            scoreList.appendChild(scoreObjects[i].htmlElement);
        }
    }
})
