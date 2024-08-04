HOST = "localhost";
PORT = 2207;

const scoreList = document.querySelector(".score-list");

class BalloonScore {
    constructor(id) {
        this.id = id;
        this.points = 0;
        this.rank = id;
        this.htmlElement = document.querySelector(`#balloon${id}`);
    }
}

let daily_record = 0;
let season_record = 0;

// instantiate the 12 score objects
let balloonScores = [];
for (let id=1; id<13; id++) {
    let ballonScore = new BalloonScore(id);
    balloonScores.push(ballonScore);
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
        balloonScores[i].points = score_data[i]
    }
    // sort and rank the objects
    let balloonScoresSorted = balloonScores.slice().sort((score_a, score_b) => score_b.points - score_a.points);
    for (let i=0; i<12; i++) {
        balloonScoresSorted[i].rank = i+1;
    }
    for (let i=0; i<12; i++) {
        console.log(`ID: ${balloonScoresSorted[i].id}`);
        console.log(`Rank: ${balloonScoresSorted[i].rank}`);
        console.log(`Points: ${balloonScoresSorted[i].points}`);
    }
    
    // update frontend
    scoreList.innerHTML = "";
    for (let i=0; i<12; i++) {
        let balloon = balloonScoresSorted[i];
        updateHtmlElement(balloon);
        scoreList.appendChild(balloon.htmlElement)
    } 

    // updated highscore-records
    daily_record = score_data[12];
    season_record = score_data[13];
    document.querySelector("#tagesrekord").innerHTML = daily_record;
    document.querySelector("#jahresrekord").innerHTML = season_record;
};

socket.onerror = error => {
    console.error('WebSocket error:', error);
};

socket.onclose = event => {
    console.log('WebSocket connection closed.');
};


function updateHtmlElement(balloon) {
    // Structure of an balloonHtmlElement:
    //<div id="balloon1" class="balloon">
    //    <div id="id1" class="id">01</div>
    //    <div id="score1" class="score">001</div>
    //</div>

    balloon.htmlElement.innerHTML = "";
    
    let idDiv = document.createElement("div");
    idDiv.id = `id${balloon.rank}`;
    idDiv.classList.add("id");
    idDiv.innerHTML = balloon.id;

    let scoreDiv = document.createElement("div");
    scoreDiv.id = `score${balloon.rank}`
    scoreDiv.classList.add("score")
    scoreDiv.innerHTML = balloon.points

    balloon.htmlElement.appendChild(idDiv);
    balloon.htmlElement.appendChild(scoreDiv);
}


// just for testing ranking mechanism
/*
let testElement = document.querySelector("#balloon1");
testElement.addEventListener("click", () => {    
    //create artificial random balloon Scores
    for (let i=0; i<12; i++) {
        balloonScores[i].points = Math.floor(Math.random() * 1000);
    }
    
    // sort and rank the objects
    let balloonScoresSorted = balloonScores.slice().sort((score_a, score_b) => score_b.points - score_a.points);
    for (let i=0; i<12; i++) {
        balloonScoresSorted[i].rank = i+1;
    }

    for (let i=0; i<12; i++) {
        console.log(`ID: ${balloonScoresSorted[i].id}`);
        console.log(`Rank: ${balloonScoresSorted[i].rank}`);
        console.log(`Points: ${balloonScoresSorted[i].points}`);
    }

    // update frontend
    scoreList.innerHTML = "";
    for (let i=0; i<12; i++) {
        let balloon = balloonScoresSorted[i];
        updateHtmlElement(balloon);
        scoreList.appendChild(balloon.htmlElement)
    } 
});
*/
